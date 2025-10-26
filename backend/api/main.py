"""
SolarMail REST API - Main Application
Sprint 0.3.2: FastAPI REST API for AI Email Analysis

Run with:
    uvicorn main:app --reload
    
Or:
    python main.py
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time
import logging

from core.config import settings
from routes import analyze
from routes import status
from models.email_analysis import ErrorResponse


# Настройка логирования
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format=settings.log_format
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events для FastAPI
    """
    # Startup
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"📊 Debug mode: {settings.debug}")
    logger.info(f"🧠 AI Model: {settings.ai_model_name}")
    logger.info(f"💻 GPU enabled: {settings.ai_use_gpu}")
    
    yield
    
    # Shutdown
    logger.info(f"🛑 Shutting down {settings.app_name}")


# Создаем FastAPI приложение
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
    lifespan=lifespan
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware для измерения времени обработки запроса
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response


# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware для логирования запросов
    """
    logger.info(f"📨 {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"✅ {request.method} {request.url.path} - {response.status_code}")
    return response


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Обработчик ошибок валидации
    """
    logger.error(f"❌ Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "detail": str(exc.errors()),
            "timestamp": time.time()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Общий обработчик исключений
    """
    logger.error(f"❌ Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "detail": str(exc) if settings.debug else "Internal server error",
            "timestamp": time.time()
        }
    )


# Подключаем роутеры
app.include_router(
    analyze.router,
    prefix=settings.api_prefix
)

app.include_router(
    status.router,
    prefix=settings.api_prefix
)


# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """
    Корневой endpoint - редирект на документацию
    """
    return RedirectResponse(url=settings.docs_url)


@app.get(
    settings.api_prefix,
    summary="API Info",
    tags=["Root"]
)
async def api_info():
    """
    Информация об API
    
    ## Example Response:
    ```json
    {
      "name": "SolarMail AI API",
      "version": "0.3.2",
      "description": "REST API for AI-powered email analysis",
      "docs": "/docs",
      "endpoints": {
        "analyze": "/api/v1/analyze",
        "status": "/api/v1/status"
      }
    }
    ```
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "docs": settings.docs_url,
        "redoc": settings.redoc_url,
        "openapi": settings.openapi_url,
        "endpoints": {
            "analyze": f"{settings.api_prefix}/analyze",
            "batch_analyze": f"{settings.api_prefix}/analyze/batch",
            "model_info": f"{settings.api_prefix}/analyze/model-info",
            "health": f"{settings.api_prefix}/status",
            "detailed_status": f"{settings.api_prefix}/status/detailed",
            "ping": f"{settings.api_prefix}/status/ping"
        }
    }


# Запуск приложения
if __name__ == "__main__":
    import uvicorn
    
    logger.info("=" * 70)
    logger.info(f"🌞 {settings.app_name} v{settings.app_version}")
    logger.info("=" * 70)
    logger.info(f"📍 Server: http://{settings.host}:{settings.port}")
    logger.info(f"📚 Docs: http://{settings.host}:{settings.port}{settings.docs_url}")
    logger.info(f"🔄 API: http://{settings.host}:{settings.port}{settings.api_prefix}")
    logger.info("=" * 70)
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
