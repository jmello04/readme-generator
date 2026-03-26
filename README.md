<div align="center">

# README Generator

[![CI](https://github.com/jmello04/readme-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/jmello04/readme-generator/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)

**Ferramenta web para geracao automatizada de documentacao tecnica com preview ao vivo via Server-Sent Events.**

</div>

---

## Sobre o Projeto

Criar um README profissional consome tempo e exige consistencia: badges corretos, estrutura de secoes,
exemplos de codigo realistas, tabelas de stack. Qualquer detalhe fora do padrao prejudica a
credibilidade do projeto.

O **README Generator** resolve isso com uma interface web de dois paineis: a esquerda um formulario
com os metadados do projeto; a direita o documento sendo construido palavra por palavra em tempo real
via streaming SSE. O resultado final inclui todas as secoes de um README de qualidade e pode ser
copiado ou baixado com um unico clique.

### Destaques tecnicos

- **Arquitetura em camadas** - separacao clara entre modelos, servicos, rotas e configuracao
- **Streaming real via SSE** - sem polling, sem timeouts artificiais
- **Tratamento de erros tipado** - excecoes customizadas com handlers globais no FastAPI
- **Observabilidade** - logging centralizado e header X-Process-Time em todas as respostas
- **CI/CD completo** - pipeline com lint (Ruff), testes (pytest) e build Docker
- **Testes sem dependencias externas** - mocks precisos com unittest.mock

---

## Funcionalidades

- Streaming em tempo real via Server-Sent Events
- Preview duplo: HTML renderizado e Markdown puro lado a lado
- Copiar com um clique para a area de transferencia
- Download do arquivo .md com o nome do projeto
- Stack chips visuais gerados conforme voce digita
- Contador de palavras, caracteres e tempo de leitura
- Atalho Ctrl+Enter para gerar sem tirar as maos do teclado
- API REST documentada via Swagger UI em /docs e ReDoc em /redoc
- Suite de 11 testes automatizados com cobertura de codigo

---

## Arquitetura

O servico de geracao isola completamente o acesso a API externa. As rotas nao conhecem detalhes
de autenticacao nem do protocolo de streaming; apenas consomem o gerador assincrono exposto.

---

## Stack

| Tecnologia | Versao | Motivo |
|---|---|---|
| Python | 3.11+ | Linguagem principal |
| FastAPI | 0.104+ | Framework ASGI com streaming nativo e tipagem |
| Pydantic v2 | 2.x | Validacao de entrada com erros descritivos |
| pydantic-settings | 2.x | Configuracao 12-factor via variaveis de ambiente |
| Uvicorn | 0.24+ | Servidor ASGI de alta performance |
| Tailwind CSS | CDN | Estilizacao da interface sem build step |
| marked.js | 9.1+ | Renderizacao de Markdown no browser |
| highlight.js | 11.9+ | Syntax highlighting no preview |
| pytest + pytest-asyncio | 7.4+ | Testes assincronos com mocks |
| Ruff | 0.4+ | Lint e formatacao em um unico binario |
| Docker | 20+ | Containerizacao reproduzivel |

---

## Como Instalar e Rodar

### Pre-requisitos

- Python 3.11+
- pip
- Docker e Docker Compose (opcional)

### Sem Docker

```bash
git clone https://github.com/jmello04/readme-generator.git
cd readme-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python main.py
```

Acesse: **http://localhost:8000** | Swagger: **http://localhost:8000/docs**

### Com Docker

```bash
cp .env.example .env
docker-compose up --build
```

---

## API Reference

### POST /generate

Retorna o README completo em uma unica resposta JSON.

Campos do payload:

| Campo | Tipo | Obrigatorio | Descricao |
|---|---|---|---|
| project_name | string | Sim | Nome do projeto (1-100 chars) |
| description | string | Sim | Descricao (10-1000 chars) |
| stack | string | Sim | Tecnologias separadas por virgula |
| project_type | enum | Sim | api, cli, scraper ou library |
| has_docker | boolean | Nao | Padrao: false |
| has_tests | boolean | Nao | Padrao: false |
| has_cicd | boolean | Nao | Padrao: false |
| author | string | Nao | Nome do autor |
| contact | string | Nao | E-mail ou link de contato |

### POST /generate/stream

Versao SSE. Os chunks chegam progressivamente no formato `data: {"content": "..."}`.
O stream termina com `data: [DONE]`.

### GET /health

Retorna o status atual da aplicacao e versao configurada.

---

## Variaveis de Ambiente

```bash
cp .env.example .env
```

| Variavel | Padrao | Descricao |
|---|---|---|
| ANTHROPIC_API_KEY | - | Chave de acesso a API de geracao de texto |
| MODEL | claude-opus-4-6 | Identificador do modelo utilizado |
| MAX_TOKENS | 4096 | Limite maximo de tokens por geracao |
| APP_HOST | 0.0.0.0 | Endereco de escuta do servidor |
| APP_PORT | 8000 | Porta do servidor |
| DEBUG | false | Modo de depuracao |

---

## Testes

```bash
make test        # Todos os testes
make test-cov    # Com relatorio de cobertura
make lint        # ruff check . --fix
make format      # ruff format .
```

---

## Estrutura

```
readme-generator/
+-- .github/workflows/ci.yml
+-- app/
|   +-- api/routes/
|   |   +-- generate.py           (POST /generate e /generate/stream)
|   |   +-- health.py             (GET /health)
|   +-- core/
|   |   +-- config.py
|   |   +-- logging.py
|   +-- models/schemas.py
|   +-- services/
|   |   +-- generation_service.py (geracao sync + streaming async)
|   +-- static/index.html         (interface web: Tailwind + marked.js + SSE)
|   +-- main.py
+-- tests/
|   +-- conftest.py
|   +-- test_generate.py
|   +-- test_health.py
+-- .env.example
+-- docker-compose.yml
+-- Dockerfile
+-- LICENSE
+-- main.py
+-- Makefile
+-- pyproject.toml
+-- requirements.txt
```

---

## Licenca

Distribuido sob a licenca **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais informacoes.

---

<div align="center">
Desenvolvido por **Joao Mello** | [GitHub @jmello04](https://github.com/jmello04)
</div>
