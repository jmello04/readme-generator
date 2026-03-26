"""Custom exception hierarchy and FastAPI exception handler."""

from fastapi import Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for all application-level errors.

    Subclasses must set :attr:`status_code` to the appropriate HTTP status
    code.  The :func:`app_error_handler` function maps every :class:`AppError`
    to a JSON response automatically.

    Attributes:
        status_code: HTTP status code returned to the client.
        message: Human-readable error description.
    """

    status_code: int = 500

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class GenerationServiceError(AppError):
    """Raised when the external generation API returns an unexpected error.

    Attributes:
        status_code: Always ``500``.
    """

    status_code = 500


class AIServiceError(AppError):
    """Alias kept for backwards compatibility with existing error handling.

    Prefer :class:`GenerationServiceError` for new code.

    Attributes:
        status_code: Always ``500``.
    """

    status_code = 500


class AIAuthError(AppError):
    """Raised when the API key is invalid or the request is unauthorised.

    Attributes:
        status_code: Always ``401``.
    """

    status_code = 401


class AIRateLimitError(AppError):
    """Raised when the API rate limit has been exceeded.

    Attributes:
        status_code: Always ``429``.
    """

    status_code = 429


async def app_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for all :class:`AppError` subclasses.

    Registered via :meth:`fastapi.FastAPI.add_exception_handler` so that
    every known application error is serialised consistently without
    requiring try/except blocks in every route.

    Args:
        request: The incoming HTTP request (provided by FastAPI).
        exc: The raised exception instance.

    Returns:
        A :class:`JSONResponse` with the appropriate HTTP status code and a
        body of ``{"detail": "<message>", "status": "error"}``.
    """
    if isinstance(exc, AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "status": "error"},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno inesperado.", "status": "error"},
    )
