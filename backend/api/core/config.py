"""
SolarMail REST API - Configuration
Sprint 0.3.2: API Settings and Environment
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class APISettings(BaseSettings):
    """
    Настройки FastAPI приложения
    """
    
    # API Info
    app_name: str = "SolarMail AI API"
    app_version: str = "0.3.2"
    app_description: str = "REST API for AI-powered email analysis"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    reload: bool = True
    
    # CORS Settings
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # API Settings
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"
    
    # AI Model Settings
    ai_model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"
    ai_use_gpu: bool = False
    ai_fallback_to_mock: bool = True
    
    # Rate Limiting (будущее)
    rate_limit_enabled: bool = False
    rate_limit_calls: int = 100
    rate_limit_period: int = 60  # seconds
    
    # Authentication (будущее)
    auth_enabled: bool = False
    jwt_secret_key: Optional[str] = None
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Database (для будущих этапов)
    db_path: str = "../../core/sync/solar_api.db"
    
    class Config:
        env_prefix = "SOLARMAIL_"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = APISettings()


def get_settings() -> APISettings:
    """
    Dependency для получения настроек в endpoints
    """
    return settings


# Конфигурация для разработки
class DevelopmentSettings(APISettings):
    debug: bool = True
    reload: bool = True
    log_level: str = "DEBUG"


# Конфигурация для production
class ProductionSettings(APISettings):
    debug: bool = False
    reload: bool = False
    log_level: str = "WARNING"
    cors_origins: list = []  # Настроить для production


def get_settings_by_env(env: str = "development") -> APISettings:
    """
    Возвращает настройки в зависимости от окружения
    
    Args:
        env: 'development' или 'production'
    """
    if env == "production":
        return ProductionSettings()
    return DevelopmentSettings()


if __name__ == "__main__":
    # Тест настроек
    print("=" * 70)
    print("🔧 SolarMail API Configuration")
    print("=" * 70)
    
    settings = get_settings()
    
    print(f"\n📊 Application:")
    print(f"   Name: {settings.app_name}")
    print(f"   Version: {settings.app_version}")
    print(f"   Debug: {settings.debug}")
    
    print(f"\n🌐 Server:")
    print(f"   Host: {settings.host}")
    print(f"   Port: {settings.port}")
    print(f"   API Prefix: {settings.api_prefix}")
    
    print(f"\n🧠 AI Model:")
    print(f"   Model: {settings.ai_model_name}")
    print(f"   GPU: {settings.ai_use_gpu}")
    print(f"   Fallback: {settings.ai_fallback_to_mock}")
    
    print(f"\n🔐 Security:")
    print(f"   Auth Enabled: {settings.auth_enabled}")
    print(f"   Rate Limit: {settings.rate_limit_enabled}")
    
    print("\n" + "=" * 70)
