import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def fix_database_uri(uri: str | None) -> str:
    """Ensure PostgreSQL URI starts with postgresql:// instead of legacy postgres://."""
    if not uri:
        return "sqlite:///communication_coach.db"
    if uri.startswith("postgres://"):
        return uri.replace("postgres://", "postgresql://", 1)
    return uri


class Config:
    """Base application configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-secret-key-12345")
    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = fix_database_uri(os.getenv("DATABASE_URL"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
    }

    # JWT Authentication
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-key-12345")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_DAYS", "30"))
    )
    JWT_HEADER_TYPE = "Bearer"
    JWT_HEADER_NAME = "Authorization"

    # AI Service (OpenAI)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "mock-dev-key")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    AI_MOCK_FALLBACK = os.getenv("AI_MOCK_FALLBACK", "True").lower() in ("true", "1", "yes")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True


class TestingConfig(Config):
    """Testing environment configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}
    AI_MOCK_FALLBACK = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development").lower()
    return config_by_name.get(env, DevelopmentConfig)
