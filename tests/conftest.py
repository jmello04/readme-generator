import pytest


@pytest.fixture
def sample_payload() -> dict:
    return {
        "project_name": "FastAPI Boilerplate",
        "description": "Um boilerplate moderno e production-ready com FastAPI, JWT e PostgreSQL.",
        "stack": "Python, FastAPI, PostgreSQL, Redis, Docker",
        "project_type": "api",
        "has_docker": True,
        "has_tests": True,
        "has_cicd": True,
        "author": "João Mello",
        "contact": "jmello04@github.com",
    }


@pytest.fixture
def minimal_payload() -> dict:
    return {
        "project_name": "Meu Projeto",
        "description": "Descrição completa do projeto para fins de teste automatizado.",
        "stack": "Python",
        "project_type": "cli",
    }
