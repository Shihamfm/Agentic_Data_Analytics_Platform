from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Agentic Data Analytics"
    environment: str = "development"

    # LLM
    llm_provider: str = "groq"
    llm_model: str = "openai/gpt-oss-120b"
    groq_api_key: str | None = None


    # POSTGRES
    postgres_host: str | None = None
    postgres_port: str | None = None
    postgres_database: str | None = None
    postgres_user: str | None = None
    postgres_password: str | None = None
    postgres_sslmode: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()