"""Generation endpoints.

Exposes two routes for README generation: a standard JSON response and a
Server-Sent Events streaming variant for real-time preview.
"""

import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.core.logging import logger
from app.exceptions import AppError
from app.models.schemas import ReadmeRequest, ReadmeResponse
from app.services.generation_service import generate_readme, generate_readme_stream

router = APIRouter(tags=["README"])


@router.post(
    "/generate",
    response_model=ReadmeResponse,
    summary="Gera um README completo",
    description=(
        "Recebe as informações do projeto e retorna o README completo em Markdown. "
        "Para uma resposta em tempo real, utilize o endpoint `/generate/stream`."
    ),
)
async def generate(request: ReadmeRequest) -> ReadmeResponse:
    """Generate a complete README and return it as a JSON response.

    Args:
        request: Project metadata validated by :class:`ReadmeRequest`.

    Returns:
        A :class:`ReadmeResponse` containing the Markdown content,
        word count and character count.

    Raises:
        AppError: Propagated directly for known error conditions
            (auth failure, rate limit, service error).
        HTTPException: Raised with status 500 for unexpected failures.
    """
    logger.info("POST /generate — projeto: '%s'", request.project_name)
    try:
        readme = generate_readme(request.model_dump())
        return ReadmeResponse(
            readme=readme,
            status="success",
            word_count=len(readme.split()),
            char_count=len(readme),
        )
    except AppError:
        raise
    except Exception as exc:
        logger.exception("Erro inesperado em POST /generate")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post(
    "/generate/stream",
    summary="Gera um README com streaming em tempo real",
    description=(
        "Versão com streaming (SSE) do endpoint de geração. "
        "Os chunks chegam progressivamente no formato `data: {content: '...'}`. "
        "O stream termina com `data: [DONE]`."
    ),
)
async def generate_stream(request: ReadmeRequest) -> StreamingResponse:
    """Generate a README and stream the output via Server-Sent Events.

    Each text chunk is delivered as an SSE frame in the format
    ``data: {"content": "..."}\n\n``.  The stream is terminated with
    ``data: [DONE]\n\n``.  Errors are delivered as
    ``data: {"error": "..."}\n\n`` instead of raising an HTTP exception
    so that the client can handle them within the open stream.

    Args:
        request: Project metadata validated by :class:`ReadmeRequest`.

    Returns:
        A :class:`StreamingResponse` with ``text/event-stream`` media type.
    """
    logger.info("POST /generate/stream — projeto: '%s'", request.project_name)

    async def event_generator():
        try:
            async for chunk in generate_readme_stream(request.model_dump()):
                payload = json.dumps({"content": chunk}, ensure_ascii=False)
                yield f"data: {payload}\n\n"
            yield "data: [DONE]\n\n"
        except AppError as exc:
            logger.warning("AppError no streaming: %s", exc.message)
            error_payload = json.dumps({"error": exc.message}, ensure_ascii=False)
            yield f"data: {error_payload}\n\n"
        except Exception as exc:
            logger.exception("Erro inesperado em POST /generate/stream")
            error_payload = json.dumps({"error": str(exc)}, ensure_ascii=False)
            yield f"data: {error_payload}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
