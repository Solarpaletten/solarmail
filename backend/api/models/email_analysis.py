"""
SolarMail REST API - Pydantic Models
Sprint 0.3.2: Request/Response schemas for email analysis
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, List, Any
from datetime import datetime


class EmailAnalysisRequest(BaseModel):
    """
    Запрос на анализ письма
    
    Example:
        {
            "subject": "Urgent: Critical bug in production",
            "body": "We have a critical issue...",
            "sender": "user@example.com"
        }
    """
    subject: str = Field(
        ...,
        description="Тема письма",
        min_length=1,
        max_length=500,
        examples=["Urgent: Critical bug in production"]
    )
    
    body: str = Field(
        default="",
        description="Тело письма",
        max_length=10000,
        examples=["We have a critical issue that needs immediate attention."]
    )
    
    sender: Optional[str] = Field(
        default=None,
        description="Email отправителя",
        examples=["user@example.com"]
    )
    
    @field_validator('subject')
    @classmethod
    def subject_not_empty(cls, v: str) -> str:
        """Проверка, что subject не пустой"""
        if not v.strip():
            raise ValueError('Subject cannot be empty')
        return v.strip()
    
    @field_validator('body')
    @classmethod
    def body_cleanup(cls, v: str) -> str:
        """Очистка body от лишних пробелов"""
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Thank you for the amazing work!",
                "body": "I wanted to express my gratitude for the excellent job you did on the project.",
                "sender": "client@company.com"
            }
        }


class EmailAnalysisResponse(BaseModel):
    """
    Ответ с результатами AI-анализа
    
    Example:
        {
            "subject": "Urgent: Critical bug",
            "sentiment": "negative",
            "sentiment_score": 0.15,
            "priority": "high",
            "priority_score": 0.95,
            "category": "Work",
            "category_confidence": 0.91,
            "model": "distilbert-base-uncased-finetuned-sst-2-english",
            "processing_time_ms": 1850
        }
    """
    subject: str = Field(
        ...,
        description="Тема письма"
    )
    
    sentiment: str = Field(
        ...,
        description="Тональность: positive, negative, neutral",
        examples=["positive", "negative", "neutral"]
    )
    
    sentiment_score: float = Field(
        ...,
        description="Уверенность в тональности (0.0 - 1.0)",
        ge=0.0,
        le=1.0
    )
    
    priority: str = Field(
        ...,
        description="Приоритет: high, medium, low",
        examples=["high", "medium", "low"]
    )
    
    priority_score: float = Field(
        ...,
        description="Уверенность в приоритете (0.0 - 1.0)",
        ge=0.0,
        le=1.0
    )
    
    category: str = Field(
        ...,
        description="Категория письма",
        examples=["Work", "Docs", "Tasks", "People", "News", "Spam", "General"]
    )
    
    category_confidence: float = Field(
        ...,
        description="Уверенность в категории (0.0 - 1.0)",
        ge=0.0,
        le=1.0
    )
    
    entities: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="Извлеченные сущности (emails, dates, urls, persons)"
    )
    
    keywords: Optional[Dict[str, List[str]]] = Field(
        default=None,
        description="Ключевые слова и топики"
    )
    
    model: str = Field(
        ...,
        description="Название использованной ML-модели"
    )
    
    processing_time_ms: int = Field(
        ...,
        description="Время обработки в миллисекундах",
        ge=0
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Время анализа"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "subject": "Thank you for the amazing work!",
                "sentiment": "positive",
                "sentiment_score": 0.95,
                "priority": "low",
                "priority_score": 0.30,
                "category": "Work",
                "category_confidence": 0.85,
                "entities": {
                    "emails": ["client@company.com"],
                    "dates": ["2025-10-25"],
                    "urls": [],
                    "persons": []
                },
                "keywords": {
                    "keywords": ["work", "project", "gratitude"],
                    "topics": []
                },
                "model": "distilbert-base-uncased-finetuned-sst-2-english",
                "processing_time_ms": 1850,
                "timestamp": "2025-10-25T12:00:00"
            }
        }


class BatchEmailAnalysisRequest(BaseModel):
    """
    Запрос на пакетный анализ писем
    """
    emails: List[EmailAnalysisRequest] = Field(
        ...,
        description="Список писем для анализа",
        min_length=1,
        max_length=100
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "emails": [
                    {
                        "subject": "Meeting tomorrow",
                        "body": "Don't forget about the meeting",
                        "sender": "manager@company.com"
                    },
                    {
                        "subject": "Invoice #123",
                        "body": "Please find attached",
                        "sender": "billing@company.com"
                    }
                ]
            }
        }


class BatchEmailAnalysisResponse(BaseModel):
    """
    Ответ с результатами пакетного анализа
    """
    results: List[EmailAnalysisResponse] = Field(
        ...,
        description="Результаты анализа для каждого письма"
    )
    
    total_emails: int = Field(
        ...,
        description="Всего писем обработано"
    )
    
    total_processing_time_ms: int = Field(
        ...,
        description="Общее время обработки"
    )
    
    average_time_ms: float = Field(
        ...,
        description="Среднее время на письмо"
    )


class ErrorResponse(BaseModel):
    """
    Ответ с ошибкой
    """
    error: str = Field(
        ...,
        description="Тип ошибки"
    )
    
    detail: str = Field(
        ...,
        description="Детали ошибки"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Время ошибки"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "detail": "Subject cannot be empty",
                "timestamp": "2025-10-25T12:00:00"
            }
        }


class HealthResponse(BaseModel):
    """
    Ответ health check
    """
    status: str = Field(
        ...,
        description="Статус API",
        examples=["ok", "error"]
    )
    
    version: str = Field(
        ...,
        description="Версия API"
    )
    
    uptime_seconds: float = Field(
        ...,
        description="Время работы в секундах"
    )
    
    ai_model_ready: bool = Field(
        ...,
        description="Готовность AI модели"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Текущее время"
    )


if __name__ == "__main__":
    # Тест моделей
    print("=" * 70)
    print("🔍 Testing Pydantic Models")
    print("=" * 70)
    
    # Тест EmailAnalysisRequest
    request = EmailAnalysisRequest(
        subject="Test email",
        body="This is a test",
        sender="test@example.com"
    )
    
    print("\n📧 EmailAnalysisRequest:")
    print(request.model_dump_json(indent=2))
    
    # Тест EmailAnalysisResponse
    response = EmailAnalysisResponse(
        subject="Test email",
        sentiment="positive",
        sentiment_score=0.85,
        priority="high",
        priority_score=0.90,
        category="Work",
        category_confidence=0.88,
        model="test-model",
        processing_time_ms=100
    )
    
    print("\n✅ EmailAnalysisResponse:")
    print(response.model_dump_json(indent=2))
    
    print("\n" + "=" * 70)
