"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration object populated via environment variables or a .env file.

    Attributes:
        APP_NAME: Human-readable application name shown in health responses and logs.
        APP_VERSION: Semantic version string of the application.
        ANTHROPIC_API_KEY: Secret key used to authenticate with the generation API.
        MODEL: Model identifier passed to the generation API on each request.
        MAX_TOKENS: Upper bound on the number of tokens the API may generate.
    """

    APP_NAME: str = "README Generator"
    APP_VERSION: str = "1.0.0"
    ANTHROPIC_API_KEY: str = ""
    MODEL: str = "claude-opus-4-6"
    MAX_TOKENS: int = 4096

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
