from typing import Literal

from pydantic import BaseModel, Field

ProjectType = Literal["api", "cli", "scraper", "library"]


class ReadmeRequest(BaseModel):
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
    readme: str = Field(..., description="Conteúdo do README gerado em Markdown")
    status: str = Field(default="success", description="Status da operação")
    word_count: int = Field(..., description="Total de palavras no README gerado")
    char_count: int = Field(..., description="Total de caracteres no README gerado")
