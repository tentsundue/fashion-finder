from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Database
    DB_URL: str
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int

    # AWS
    S3_BUCKET: str | None = None
    AWS_REGION: str | None = None

    # ML
    CLIP_MODEL_NAME: str = "ViT-B-32"


settings = Settings()