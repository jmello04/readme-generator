"""Pydantic schemas for the generation API."""

from typing import Literal

from pydantic import BaseModel, Field

ProjectType = Literal["api", "cli", "scraper", "library"]


class ReadmeRequest(BaseModel):
    """Input payload for README generation endpoints.

    Attributes:
        project_name: Short display name of the project (1–100 chars).
        description: Human-readable summary of what the project does
            (10–1000 chars).
        stack: Comma-separated list of technologies used.
        project_type: Category that best describes the project.
        has_docker: Whether the project ships Docker / Compose support.
        has_tests: Whether the project includes automated tests.
        has_cicd: Whether the project has a CI/CD pipeline.
        author: Optional name of the primary author.
        contact: Optional e-mail or profile URL for the author.
    """

    project_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nome do projeto",
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Descrição resumida do projeto",
    )
    stack: str = Field(
        ...,
        min_length=1,
        max_length=300,
        description="Tecnologias utilizadas, separadas por vírgula",
    )
    project_type: ProjectType = Field(
        ...,
        description="Tipo do projeto: api | cli | scraper | library",
    )
    has_docker: bool = Field(default=False, description="O projeto possui Docker?")
    has_tests: bool = Field(default=False, description="O projeto possui testes automatizados?")
    has_cicd: bool = Field(default=False, description="O projeto possui pipeline CI/CD?")
    author: str | None = Field(default=None, max_length=100, description="Nome do autor")
    contact: str | None = Field(
        default=None,
        max_length=200,
        description="E-mail ou link de contato",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "project_name": "FastAPI Boilerplate",
                "description": "Um boilerplate production-ready com FastAPI, JWT e PostgreSQL.",
                "stack": "Python, FastAPI, PostgreSQL, Redis, Docker",
                "project_type": "api",
                "has_docker": True,
                "has_tests": True,
                "has_cicd": True,
                "author": "João Mello",
                "contact": "jmello04@github.com",
            }
        }
    }


class ReadmeResponse(BaseModel):
    """Response payload returned by the generation endpoints.

    Attributes:
        readme: Full README content in Markdown format.
        status: Operation status string, always ``"success"`` on happy path.
        word_count: Number of words in the generated README.
        char_count: Number of characters in the generated README.
    """

    readme: str = Field(..., description="Conteúdo do README gerado em Markdown")
    status: str = Field(default="success", description="Status da operação")
    word_count: int = Field(..., description="Total de palavras no README gerado")
    char_count: int = Field(..., description="Total de caracteres no README gerado")
