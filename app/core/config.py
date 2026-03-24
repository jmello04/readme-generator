from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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
