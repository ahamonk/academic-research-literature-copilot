from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    groq_api_key: str | None = None
    groq_model: str = "llama-3.3-70b-versatile"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()