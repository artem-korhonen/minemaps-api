from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60

    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_ENDPOINT_URL: str
    S3_BUCKET_NAME: str
    S3_PUBLIC_URL: str

    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
