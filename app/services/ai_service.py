from collections.abc import AsyncGenerator

import anthropic

from app.core.config import settings
from app.core.logging import logger
from app.exceptions import AIAuthError, AIRateLimitError, AIServiceError

_SYSTEM_PROMPT = """\
Você é um especialista em documentação técnica de software open source.
Sua missão é criar READMEs completos, profissionais e visualmente atrativos no formato Markdown.
Utilize badges do shields.io, emojis nos títulos de seção, tabelas e blocos de código relevantes.
Retorne APENAS o conteúdo Markdown, sem texto introdutório, explicações ou qualquer outra saída adicional.\
"""


def _build_prompt(data: dict) -> str:
    recursos: list[str] = []
    if data.get("has_docker"):
        recursos.append("Docker e docker-compose")
    if data.get("has_tests"):
        recursos.append("Testes automatizados")
    if data.get("has_cicd"):
        recursos.append("Pipeline CI/CD")
    recursos_str = ", ".join(recursos) if recursos else "Nenhum recurso adicional informado"

    return f"""\
Crie um README.md profissional e completo para o seguinte projeto de software:

---

**Nome do Projeto:** {data["project_name"]}
**Descrição:** {data["description"]}
**Stack / Tecnologias:** {data["stack"]}
**Tipo de Projeto:** {data["project_type"]}
**Recursos disponíveis:** {recursos_str}
**Autor:** {data.get("author") or "N/A"}
**Contato:** {data.get("contact") or "N/A"}

---

O README deve conter, OBRIGATORIAMENTE e nesta ordem, as seguintes seções:

1. **Cabeçalho** — Título centralizado com badges do shields.io para cada tecnologia da stack, \
licença MIT e status do build (se CI/CD habilitado). Use `<div align="center">` para centralizar.

2. **Sobre o Projeto** — Descrição detalhada e persuasiva: o que o projeto faz e qual problema resolve.

3. **✨ Funcionalidades** — Lista com marcadores das funcionalidades principais.

4. **🛠️ Stack Utilizada** — Tabela Markdown: Tecnologia | Versão | Finalidade.

5. **🚀 Como Instalar e Rodar**
   - Pré-requisitos (o que deve estar instalado)
   - Instalação **sem Docker** (passo a passo com comandos em blocos de código)
   - Instalação **com Docker** (somente se has_docker for verdadeiro)

6. **📖 Exemplos de Uso** — Blocos de código reais e realistas para o tipo "{data["project_type"]}".

7. **📁 Estrutura de Pastas** — Árvore de diretórios em bloco de código com comentários.

8. **🤝 Como Contribuir** — Fork → clone → branch → commit → pull request.

9. **📄 Licença** — MIT License com nome "{data.get("author") or "N/A"}" \
e contato "{data.get("contact") or "N/A"}".

---

Diretrizes obrigatórias:
- Use badges reais do shields.io (`https://img.shields.io/badge/...`)
- Todos os títulos de seção devem ter emojis
- Exemplos de código devem ser realistas e específicos para o tipo "{data["project_type"]}"
- Escreva todo o conteúdo em **português do Brasil**
- O resultado deve parecer escrito por um desenvolvedor sênior experiente\
"""


def generate_readme(data: dict) -> str:
    logger.info("Gerando README para: '%s'", data.get("project_name"))
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    try:
        message = client.messages.create(
            model=settings.MODEL,
            max_tokens=settings.MAX_TOKENS,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _build_prompt(data)}],
        )
        result: str = message.content[0].text
        logger.info(
            "README gerado com sucesso: %d palavras, %d chars",
            len(result.split()),
            len(result),
        )
        return result
    except anthropic.AuthenticationError as exc:
        raise AIAuthError("Chave de API inválida ou não autorizada. Verifique o arquivo .env.") from exc
    except anthropic.RateLimitError as exc:
        raise AIRateLimitError("Limite de requisições atingido. Aguarde alguns instantes.") from exc
    except anthropic.APIError as exc:
        raise AIServiceError(f"Erro na API externa: {exc.message}") from exc


async def generate_readme_stream(data: dict) -> AsyncGenerator[str, None]:
    logger.info("Iniciando streaming para: '%s'", data.get("project_name"))
    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    try:
        async with client.messages.stream(
            model=settings.MODEL,
            max_tokens=settings.MAX_TOKENS,
            system=_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": _build_prompt(data)}],
        ) as stream:
            async for chunk in stream.text_stream:
                yield chunk
    except anthropic.AuthenticationError as exc:
        raise AIAuthError("Chave de API inválida ou não autorizada.") from exc
    except anthropic.RateLimitError as exc:
        raise AIRateLimitError("Limite de requisições atingido.") from exc
    except anthropic.APIError as exc:
        raise AIServiceError(f"Erro na API externa: {exc.message}") from exc
