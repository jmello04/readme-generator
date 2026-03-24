from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Sistema"])


@router.get(
    "/health",
    summary="Status da aplicação",
    description="Retorna o status atual da API e informações de configuração.",
)
async def health() -> dict:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "model": settings.MODEL,
    }
