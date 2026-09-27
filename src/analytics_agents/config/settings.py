from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Agentic Data Analytics"
    environment: str = "development"

    GROQ_API_KEY: str | None = None

    databricks_server_hostname: str | None = None
    databricks_http_path: str | None = None
    databricks_access_token: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()