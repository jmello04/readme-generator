import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.api.routes import generate, health
from app.core.config import settings
from app.core.logging import logger
from app.exceptions import AppError, app_error_handler

_STATIC = Path(__file__).parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("🚀  %s v%s | modelo: %s", settings.APP_NAME, settings.APP_VERSION, settings.MODEL)
    yield
    logger.info("📴  %s encerrado.", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Ferramenta web para geração automática de documentação técnica profissional.\n\n"
        "**Endpoints principais:**\n"
        "- `POST /generate` — Resposta completa em JSON\n"
        "- `POST /generate/stream` — Streaming em tempo real via SSE\n"
        "- `GET /health` — Status da aplicação"
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── Handlers de exceção personalizados ────────────────────────────────────────
app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]

# ── Middleware: CORS ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Middleware: Tempo de processamento + logging ───────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    if not request.url.path.startswith(("/docs", "/redoc", "/openapi")):
        logger.info(
            "%-6s %-30s → %d  (%.3fs)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed,
        )
    response.headers["X-Process-Time"] = f"{elapsed:.4f}s"
    return response


# ── Routers ────────────────────────────────────────────────────────────────────
app.include_router(health.router)
app.include_router(generate.router)


# ── Frontend ───────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index() -> HTMLResponse:
    return HTMLResponse((_STATIC / "index.html").read_text(encoding="utf-8"))
