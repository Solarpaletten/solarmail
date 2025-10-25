"""
SolarMail REST API - Analyze Routes
Sprint 0.3.2: AI Email Analysis Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import sys
import os
import json
import time

# Добавляем путь к core/sync для импорта AIParserTransformer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../core/sync'))

try:
    from ai_parser_transformer import AIParserTransformer
    TRANSFORMER_AVAILABLE = True
except ImportError:
    TRANSFORMER_AVAILABLE = False
    print("⚠️  AIParserTransformer not available")

from models.email_analysis import (
    EmailAnalysisRequest,
    EmailAnalysisResponse,
    BatchEmailAnalysisRequest,
    BatchEmailAnalysisResponse,
    ErrorResponse
)
from core.config import get_settings, APISettings


# Создаем router
router = APIRouter(
    prefix="/analyze",
    tags=["AI Analysis"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        422: {"model": ErrorResponse, "description": "Validation Error"}
    }
)


# Глобальный экземпляр анализатора (инициализируется при старте)
_ai_parser: AIParserTransformer = None


def get_ai_parser(settings: APISettings = Depends(get_settings)) -> AIParserTransformer:
    """
    Dependency для получения AI parser
    Инициализируется один раз при первом запросе
    """
    global _ai_parser
    
    if _ai_parser is None:
        if not TRANSFORMER_AVAILABLE:
            raise HTTPException(
                status_code=500,
                detail="AIParserTransformer module not available"
            )
        
        try:
            _ai_parser = AIParserTransformer(
                model_name=settings.ai_model_name,
                use_gpu=settings.ai_use_gpu,
                fallback_to_mock=settings.ai_fallback_to_mock
            )
            print(f"✅ AIParserTransformer initialized: {_ai_parser.get_model_info()['type']}")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize AIParserTransformer: {str(e)}"
            )
    
    return _ai_parser


@router.post(
    "",
    response_model=EmailAnalysisResponse,
    summary="Analyze Email",
    description="Анализирует письмо с помощью AI и возвращает sentiment, priority, category",
    response_description="Результаты AI-анализа"
)
async def analyze_email(
    request: EmailAnalysisRequest,
    ai_parser: AIParserTransformer = Depends(get_ai_parser)
) -> EmailAnalysisResponse:
    """
    ## Анализ письма с помощью AI
    
    Использует ML-модели для определения:
    - **Sentiment** (positive/negative/neutral)
    - **Priority** (high/medium/low)
    - **Category** (Work/Docs/Tasks/People/News/Spam/General)
    - **Entities** (emails, dates, urls, persons)
    - **Keywords** (ключевые слова и топики)
    
    ### Example Request:
    ```json
    {
      "subject": "Urgent: Critical bug in production",
      "body": "We have a critical issue that needs immediate attention.",
      "sender": "dev@company.com"
    }
    ```
    
    ### Example Response:
    ```json
    {
      "subject": "Urgent: Critical bug in production",
      "sentiment": "negative",
      "sentiment_score": 0.15,
      "priority": "high",
      "priority_score": 0.95,
      "category": "Work",
      "category_confidence": 0.91,
      "model": "distilbert-base-uncased-finetuned-sst-2-english",
      "processing_time_ms": 1850
    }
    ```
    """
    try:
        # Выполняем AI-анализ
        analysis_result = ai_parser.analyze_email(
            subject=request.subject,
            body=request.body
        )
        
        # Парсим JSON из результата
        entities = json.loads(analysis_result.get('entities_json', '{}'))
        keywords = json.loads(analysis_result.get('keywords_json', '{}'))
        
        # Формируем ответ
        response = EmailAnalysisResponse(
            subject=request.subject,
            sentiment=analysis_result['sentiment'],
            sentiment_score=analysis_result['sentiment_score'],
            priority=analysis_result['priority'],
            priority_score=analysis_result['priority_score'],
            category=analysis_result['category'],
            category_confidence=analysis_result['category_confidence'],
            entities=entities if entities else None,
            keywords=keywords if keywords else None,
            model=analysis_result['ai_model'],
            processing_time_ms=analysis_result['processing_time_ms']
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )


@router.post(
    "/batch",
    response_model=BatchEmailAnalysisResponse,
    summary="Batch Analyze Emails",
    description="Анализирует несколько писем одновременно",
    response_description="Результаты пакетного анализа"
)
async def batch_analyze_emails(
    request: BatchEmailAnalysisRequest,
    ai_parser: AIParserTransformer = Depends(get_ai_parser)
) -> BatchEmailAnalysisResponse:
    """
    ## Пакетный анализ писем
    
    Анализирует до 100 писем за один запрос.
    
    ### Example Request:
    ```json
    {
      "emails": [
        {
          "subject": "Meeting tomorrow",
          "body": "Don't forget about the meeting at 10am"
        },
        {
          "subject": "Invoice #123",
          "body": "Please find attached invoice"
        }
      ]
    }
    ```
    """
    try:
        start_time = time.time()
        results = []
        
        # Анализируем каждое письмо
        for email_request in request.emails:
            analysis_result = ai_parser.analyze_email(
                subject=email_request.subject,
                body=email_request.body
            )
            
            # Парсим JSON
            entities = json.loads(analysis_result.get('entities_json', '{}'))
            keywords = json.loads(analysis_result.get('keywords_json', '{}'))
            
            # Формируем ответ для письма
            email_response = EmailAnalysisResponse(
                subject=email_request.subject,
                sentiment=analysis_result['sentiment'],
                sentiment_score=analysis_result['sentiment_score'],
                priority=analysis_result['priority'],
                priority_score=analysis_result['priority_score'],
                category=analysis_result['category'],
                category_confidence=analysis_result['category_confidence'],
                entities=entities if entities else None,
                keywords=keywords if keywords else None,
                model=analysis_result['ai_model'],
                processing_time_ms=analysis_result['processing_time_ms']
            )
            
            results.append(email_response)
        
        # Вычисляем общее время
        total_time_ms = int((time.time() - start_time) * 1000)
        avg_time_ms = total_time_ms / len(results) if results else 0
        
        # Формируем итоговый ответ
        batch_response = BatchEmailAnalysisResponse(
            results=results,
            total_emails=len(results),
            total_processing_time_ms=total_time_ms,
            average_time_ms=avg_time_ms
        )
        
        return batch_response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch analysis failed: {str(e)}"
        )


@router.get(
    "/model-info",
    summary="Get Model Info",
    description="Информация о загруженной AI модели"
)
async def get_model_info(
    ai_parser: AIParserTransformer = Depends(get_ai_parser)
) -> dict:
    """
    ## Информация о ML модели
    
    Возвращает детали загруженной модели:
    - Название модели
    - Тип (transformer-ml или mock-fallback)
    - Статус GPU
    - Доступность pipelines
    
    ### Example Response:
    ```json
    {
      "transformer_ready": true,
      "model_name": "distilbert-base-uncased-finetuned-sst-2-english",
      "gpu_enabled": false,
      "type": "transformer-ml",
      "version": "0.3.0"
    }
    ```
    """
    try:
        model_info = ai_parser.get_model_info()
        return model_info
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get model info: {str(e)}"
        )
