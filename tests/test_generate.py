from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from app.exceptions import AIAuthError, AIRateLimitError
from app.main import app

_README_MOCK = "# FastAPI Boilerplate\n\nDocumentação gerada com sucesso para testes."


@pytest.mark.asyncio
async def test_generate_retorna_readme_com_sucesso(sample_payload):
    with patch("app.api.routes.generate.generate_readme", return_value=_README_MOCK):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/generate", json=sample_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["readme"] == _README_MOCK
    assert data["word_count"] > 0
    assert data["char_count"] == len(_README_MOCK)


@pytest.mark.asyncio
async def test_generate_campos_obrigatorios_ausentes():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/generate", json={"project_name": "Teste"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_descricao_muito_curta(sample_payload):
    payload = {**sample_payload, "description": "Curta"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/generate", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_project_type_invalido(sample_payload):
    payload = {**sample_payload, "project_type": "tipo-invalido"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/generate", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_trata_erro_generico(sample_payload):
    with patch("app.api.routes.generate.generate_readme", side_effect=Exception("Erro inesperado")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/generate", json=sample_payload)
    assert response.status_code == 500
    assert "Erro inesperado" in response.json()["detail"]


@pytest.mark.asyncio
async def test_generate_trata_erro_autenticacao(sample_payload):
    with patch("app.api.routes.generate.generate_readme", side_effect=AIAuthError("Chave inválida")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/generate", json=sample_payload)
    assert response.status_code == 401
    assert response.json()["status"] == "error"


@pytest.mark.asyncio
async def test_generate_trata_rate_limit(sample_payload):
    with patch("app.api.routes.generate.generate_readme", side_effect=AIRateLimitError("Rate limit")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/generate", json=sample_payload)
    assert response.status_code == 429
    assert response.json()["status"] == "error"


@pytest.mark.asyncio
async def test_generate_sem_campos_opcionais(minimal_payload):
    with patch("app.api.routes.generate.generate_readme", return_value=_README_MOCK):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/generate", json=minimal_payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_generate_stream_retorna_sse(sample_payload):
    async def mock_stream(data):
        for chunk in ["# ", "FastAPI", "\n\nConteúdo"]:
            yield chunk

    with patch("app.api.routes.generate.generate_readme_stream", new=mock_stream):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post("/generate/stream", json=sample_payload)

    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    body = response.text
    assert "data:" in body
    assert "[DONE]" in body
