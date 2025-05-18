from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Email configuration
    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    # JWT/Auth configuration
    SECRET_KEY: str = "dev-secret-key"  # override in .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Optional: Database configuration
    DATABASE_URL: str = "sqlite:///./devlog.db"

    class Config:
        env_file = ".env"
        extra = "forbid"  # prevents undeclared env vars (safe)


settings = Settings()
