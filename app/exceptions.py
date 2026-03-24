from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Classe base para erros da aplicação."""

    status_code: int = 500

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class AIServiceError(AppError):
    """Erro genérico no serviço de geração de conteúdo."""

    status_code = 500


class AIAuthError(AppError):
    """Chave de API inválida ou sem permissão."""

    status_code = 401


class AIRateLimitError(AppError):
    """Limite de requisições atingido."""

    status_code = 429


async def app_error_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "status": "error"},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno inesperado.", "status": "error"},
    )
