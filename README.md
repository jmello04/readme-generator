<div align="center">

# 📄 README Generator

[![CI](https://github.com/jmello04/readme-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/jmello04/readme-generator/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat-square&logo=fastapi&logoColor=white)
![Anthropic](https://img.shields.io/badge/Anthropic_SDK-0.39+-CC785C?style=flat-square&logo=anthropic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/Testes-Pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white)
![Ruff](https://img.shields.io/badge/Lint-Ruff-FCC21B?style=flat-square&logo=ruff&logoColor=black)
![MIT License](https://img.shields.io/badge/Licença-MIT-22c55e?style=flat-square)

**Ferramenta web que transforma a descrição do seu projeto em documentação técnica completa e profissional em segundos — com preview em tempo real via streaming.**

[Começar agora](#-como-instalar-e-rodar) · [API Reference](#-api-reference) · [Guia de Contribuição](CONTRIBUTING.md)

</div>

---

## 📋 Sobre o Projeto

O **README Generator** é uma aplicação web full-stack que resolve um problema comum no desenvolvimento de software: criar documentação técnica profissional consome tempo e exige experiência com Markdown, badges e boas práticas de documentação.

Com uma interface moderna de **dois painéis** — formulário à esquerda, preview ao vivo à direita — você preenche as informações básicas do projeto e acompanha o README sendo gerado **palavra por palavra em tempo real** via streaming SSE. O resultado inclui badges de tecnologia, tabela de stack, exemplos de código, estrutura de pastas e todas as seções que um README de qualidade precisa ter.

### Por que este projeto se destaca

- **Arquitetura limpa**: separação de responsabilidades em camadas (models, services, routes, core)
- **Streaming real**: SSE com `AsyncAnthropic`, sem polling nem timeouts
- **Tratamento de erros tipado**: exceptions customizadas (`AIAuthError`, `AIRateLimitError`) com handlers globais no FastAPI
- **Observabilidade**: logging centralizado e header `X-Process-Time` em todas as respostas
- **CI/CD completo**: pipeline com lint (Ruff) → testes (pytest + coverage) → build Docker
- **Testável**: mocks precisos com `unittest.mock`; sem chamadas reais à API nos testes

---

## ✨ Funcionalidades

- **⚡ Streaming em tempo real** — Acompanhe o README sendo escrito via Server-Sent Events
- **📑 Preview duplo** — Visualização renderizada (HTML + highlight.js) e Markdown puro
- **📋 Copiar com um clique** — Copia o Markdown completo para a área de transferência
- **⬇️ Download .md** — Baixa o arquivo com o nome do projeto
- **🏷️ Stack chips** — Tags visuais aparecem conforme você digita as tecnologias
- **📊 Estatísticas** — Contador de palavras, caracteres e tempo estimado de leitura
- **⌨️ Atalho de teclado** — `Ctrl+Enter` para gerar sem tirar as mãos do teclado
- **🐳 Suporte a Docker** — Seção de instalação com docker-compose gerada automaticamente
- **🔌 API REST documentada** — Swagger UI em `/docs` e ReDoc em `/redoc`
- **✅ Testes automatizados** — Suite pytest com 11 casos de teste e cobertura de código

---

## 🛠️ Stack Utilizada

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.11+ | Linguagem principal |
| FastAPI | 0.104+ | Framework web ASGI |
| Anthropic SDK | 0.39+ | Geração de conteúdo via API |
| Pydantic v2 | 2.x | Validação de dados e schemas |
| pydantic-settings | 2.x | Configuração via variáveis de ambiente |
| Uvicorn | 0.24+ | Servidor ASGI de alta performance |
| Tailwind CSS | CDN | Estilização da interface |
| marked.js | 9.1+ | Renderização de Markdown no browser |
| highlight.js | 11.9+ | Syntax highlighting no preview |
| pytest + pytest-asyncio | 7.4+ | Testes automatizados async |
| Ruff | 0.4+ | Lint e formatação de código |
| Docker | 20+ | Containerização |

---

## 🚀 Como Instalar e Rodar

### Pré-requisitos

- **Python 3.11+**
- **pip**
- Uma chave de API válida da **Anthropic** → [console.anthropic.com](https://console.anthropic.com)
- **Docker e Docker Compose** *(opcional)*

---

### Instalação sem Docker

**1. Clone o repositório**
```bash
git clone https://github.com/jmello04/readme-generator.git
cd readme-generator
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**
```bash
cp .env.example .env
```

Edite o `.env` e insira sua chave:
```env
ANTHROPIC_API_KEY=sk-ant-...
MODEL=claude-opus-4-6
MAX_TOKENS=4096
```

**5. Inicie o servidor**
```bash
python main.py
# ou
make dev
```

Acesse: **http://localhost:8000**
Swagger UI: **http://localhost:8000/docs**

---

### Instalação com Docker

**1. Configure o `.env`** *(mesmo passo acima)*

**2. Suba os containers**
```bash
docker-compose up --build
# ou
make docker-up
```

Acesse: **http://localhost:8000**

**Parar os containers:**
```bash
docker-compose down
# ou
make docker-down
```

---

## 📖 API Reference

### `POST /generate`
Retorna o README completo em JSON.

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "FastAPI Boilerplate",
    "description": "Boilerplate production-ready com FastAPI, JWT e PostgreSQL.",
    "stack": "Python, FastAPI, PostgreSQL, Redis",
    "project_type": "api",
    "has_docker": true,
    "has_tests": true,
    "has_cicd": false,
    "author": "João Mello",
    "contact": "jmello04@github.com"
  }'
```

**Resposta (`200 OK`):**
```json
{
  "readme": "# FastAPI Boilerplate\n\n...",
  "status": "success",
  "word_count": 842,
  "char_count": 5231
}
```

---

### `POST /generate/stream`
Versão com streaming SSE. Os chunks chegam progressivamente.

```bash
curl -N -X POST http://localhost:8000/generate/stream \
  -H "Content-Type: application/json" \
  -d '{ ... mesmo payload ... }'
```

**Resposta (SSE):**
```
data: {"content": "# FastAPI"}
data: {"content": " Boilerplate\n\n"}
data: {"content": "..."}
data: [DONE]
```

**Erros no stream:**
```
data: {"error": "Chave de API inválida ou não autorizada."}
```

---

### `GET /health`
Verifica o status da aplicação.

```bash
curl http://localhost:8000/health
```

**Resposta:**
```json
{
  "status": "ok",
  "app": "README Generator",
  "version": "1.0.0",
  "model": "claude-opus-4-6"
}
```

---

### Campos do Payload

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `project_name` | `string` | ✅ | Nome do projeto (1-100 chars) |
| `description` | `string` | ✅ | Descrição (10-1000 chars) |
| `stack` | `string` | ✅ | Tecnologias separadas por vírgula |
| `project_type` | `enum` | ✅ | `api` \| `cli` \| `scraper` \| `library` |
| `has_docker` | `boolean` | ❌ | Padrão: `false` |
| `has_tests` | `boolean` | ❌ | Padrão: `false` |
| `has_cicd` | `boolean` | ❌ | Padrão: `false` |
| `author` | `string` | ❌ | Nome do autor |
| `contact` | `string` | ❌ | E-mail ou link de contato |

---

## 📁 Estrutura de Pastas

```
readme-generator/
├── .github/
│   └── workflows/
│       └── ci.yml                # Pipeline: lint → testes → build Docker
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── generate.py       # POST /generate e /generate/stream
│   │       └── health.py         # GET /health
│   ├── core/
│   │   ├── config.py             # Settings via pydantic-settings
│   │   └── logging.py            # Logging centralizado
│   ├── models/
│   │   └── schemas.py            # ReadmeRequest e ReadmeResponse (Pydantic v2)
│   ├── services/
│   │   └── ai_service.py         # Geração sync + streaming async
│   ├── static/
│   │   └── index.html            # SPA: Tailwind CSS + marked.js + SSE
│   └── main.py                   # FastAPI app, middleware, exception handlers
├── tests/
│   ├── conftest.py               # Fixtures compartilhadas
│   ├── test_generate.py          # 9 casos de teste dos endpoints de geração
│   └── test_health.py            # 3 casos de teste do health check
├── .env.example                  # Modelo de variáveis de ambiente
├── .gitignore
├── CONTRIBUTING.md               # Guia de contribuição
├── docker-compose.yml
├── Dockerfile
├── LICENSE                       # MIT License
├── main.py                       # Entry point (python main.py)
├── Makefile                      # Atalhos: make dev, test, lint, docker-up
├── pyproject.toml                # Metadados, ruff, pytest, coverage
├── README.md
└── requirements.txt
```

---

## 🧪 Executando os Testes

```bash
# Todos os testes
make test

# Com relatório de cobertura
make test-cov

# Teste específico
pytest tests/test_generate.py -v -k "test_generate_retorna"
```

**Verificação de estilo:**
```bash
make lint    # ruff check . --fix
make format  # ruff format .
```

---

## 🤝 Como Contribuir

1. **Fork** o repositório no GitHub
2. **Clone** seu fork: `git clone https://github.com/seu-usuario/readme-generator.git`
3. **Crie uma branch**: `git checkout -b feature/minha-melhoria`
4. **Desenvolva** e adicione testes
5. **Verifique**: `make test && make lint`
6. **Commit** seguindo [Conventional Commits](https://www.conventionalcommits.org/): `git commit -m "feat: adiciona exportação PDF"`
7. **Push**: `git push origin feature/minha-melhoria`
8. **Abra um Pull Request** com descrição detalhada

Leia o [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

<div align="center">

Desenvolvido por **João Mello** · [GitHub @jmello04](https://github.com/jmello04)

</div>
