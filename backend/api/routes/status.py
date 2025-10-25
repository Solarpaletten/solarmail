"""
SolarMail REST API - Status Routes
Sprint 0.3.2: Health checks and system status
"""

from fastapi import APIRouter, Depends
import time
import psutil
import platform
from datetime import datetime

from models.email_analysis import HealthResponse
from core.config import get_settings, APISettings


# Создаем router
router = APIRouter(
    prefix="/status",
    tags=["System Status"]
)


# Время старта приложения
_start_time = time.time()


@router.get(
    "",
    response_model=HealthResponse,
    summary="Health Check",
    description="Проверка работоспособности API"
)
async def health_check(
    settings: APISettings = Depends(get_settings)
) -> HealthResponse:
    """
    ## Health Check
    
    Возвращает статус API и информацию о системе.
    
    ### Example Response:
    ```json
    {
      "status": "ok",
      "version": "0.3.2",
      "uptime_seconds": 123.45,
      "ai_model_ready": true,
      "timestamp": "2025-10-25T12:00:00"
    }
    ```
    """
    uptime = time.time() - _start_time
    
    # Проверяем доступность AI модели
    ai_model_ready = True
    try:
        from routes.analyze import _ai_parser
        if _ai_parser is not None:
            model_info = _ai_parser.get_model_info()
            ai_model_ready = model_info.get('transformer_ready', False) or model_info.get('mock_fallback', False)
    except:
        ai_model_ready = False
    
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        uptime_seconds=round(uptime, 2),
        ai_model_ready=ai_model_ready,
        timestamp=datetime.now()
    )


@router.get(
    "/detailed",
    summary="Detailed Status",
    description="Детальная информация о системе"
)
async def detailed_status(
    settings: APISettings = Depends(get_settings)
) -> dict:
    """
    ## Детальный статус системы
    
    Возвращает подробную информацию о:
    - Системных ресурсах (CPU, RAM)
    - Конфигурации API
    - Статусе AI модели
    
    ### Example Response:
    ```json
    {
      "api": {
        "name": "SolarMail AI API",
        "version": "0.3.2",
        "uptime_seconds": 123.45
      },
      "system": {
        "platform": "Darwin",
        "cpu_percent": 45.2,
        "memory_percent": 67.8
      },
      "ai": {
        "model_ready": true,
        "model_name": "distilbert-base-uncased-finetuned-sst-2-english"
      }
    }
    ```
    """
    uptime = time.time() - _start_time
    
    # Системная информация
    system_info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "cpu_count": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "memory_available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
        "memory_percent": psutil.virtual_memory().percent
    }
    
    # AI модель информация
    ai_info = {
        "model_ready": False,
        "model_name": settings.ai_model_name,
        "gpu_enabled": settings.ai_use_gpu,
        "fallback_enabled": settings.ai_fallback_to_mock
    }
    
    try:
        from routes.analyze import _ai_parser
        if _ai_parser is not None:
            model_info = _ai_parser.get_model_info()
            ai_info.update({
                "model_ready": True,
                "type": model_info.get('type'),
                "transformer_ready": model_info.get('transformer_ready'),
                "sentiment_pipeline": model_info.get('sentiment_pipeline'),
                "zero_shot_pipeline": model_info.get('zero_shot_pipeline')
            })
    except:
        pass
    
    return {
        "api": {
            "name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug,
            "uptime_seconds": round(uptime, 2)
        },
        "system": system_info,
        "ai": ai_info,
        "timestamp": datetime.now().isoformat()
    }


@router.get(
    "/ping",
    summary="Ping",
    description="Простая проверка доступности"
)
async def ping() -> dict:
    """
    ## Ping
    
    Простейшая проверка работоспособности API.
    
    ### Example Response:
    ```json
    {
      "message": "pong",
      "timestamp": "2025-10-25T12:00:00"
    }
    ```
    """
    return {
        "message": "pong",
        "timestamp": datetime.now().isoformat()
    }
