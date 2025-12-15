import os
import secrets
from typing import List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    APP_NAME: str = "University Management System"
    ENV: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")

    # JWT / Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    BCRYPT_ROUNDS: int = int(os.getenv("BCRYPT_ROUNDS"))

    # Redis (optional) - for refresh tokens / token blacklist / rate limiting
    REDIS_URL: str = os.getenv("REDIS_URL")

    # CORS
    CORS_ORIGINS: List[str] | None = None

    # Pagination / defaults
    DEFAULT_PAGE_SIZE: int = int(25)
    MAX_PAGE_SIZE: int = int(200)

    # Logging
    LOG_LEVEL: str = "INFO"

    # Feature flags
    ENABLE_TOKEN_BLACKLIST: bool = False
    ENABLE_AUDIT_LOGS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False

    @field_validator("SECRET_KEY", mode="before")
    @classmethod
    def ensure_secret_key(cls, v):
        if v:
            return v
        # generate a secure random key if not set (useful for local dev only)
        return secrets.token_urlsafe(32)

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_cors(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

settings = Settings()
