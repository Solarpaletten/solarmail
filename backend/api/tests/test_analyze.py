"""
SolarMail REST API - Analyze Endpoint Tests
Sprint 0.3.2: Testing AI analysis endpoints
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Добавляем путь к API
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app


# Test client
client = TestClient(app)


class TestAnalyzeEndpoint:
    """Тесты для /api/v1/analyze endpoint"""
    
    def test_analyze_simple_email(self):
        """Тест анализа простого письма"""
        response = client.post(
            "/api/v1/analyze",
            json={
                "subject": "Thank you!",
                "body": "Great work on the project"
            }
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "sentiment" in data
        assert "priority" in data
        assert "category" in data
        assert "model" in data
        assert data["sentiment"] in ["positive", "negative", "neutral"]
        assert data["priority"] in ["high", "medium", "low"]
    
    def test_analyze_urgent_email(self):
        """Тест анализа срочного письма"""
        response = client.post(
            "/api/v1/analyze",
            json={
                "subject": "URGENT: Critical bug",
                "body": "We have a critical issue in production"
            }
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert data["priority"] == "high"
        assert data["sentiment"] == "negative"
    
    def test_analyze_with_sender(self):
        """Тест анализа письма с отправителем"""
        response = client.post(
            "/api/v1/analyze",
            json={
                "subject": "Meeting tomorrow",
                "body": "Don't forget",
                "sender": "boss@company.com"
            }
        )
        
        assert response.status_code == 200
    
    def test_analyze_empty_subject(self):
        """Тест с пустой темой (должна быть ошибка)"""
        response = client.post(
            "/api/v1/analyze",
            json={
                "subject": "",
                "body": "Some content"
            }
        )
        
        assert response.status_code == 422
    
    def test_analyze_missing_subject(self):
        """Тест без темы (должна быть ошибка)"""
        response = client.post(
            "/api/v1/analyze",
            json={
                "body": "Some content"
            }
        )
        
        assert response.status_code == 422
    
    def test_analyze_long_email(self):
        """Тест анализа длинного письма"""
        long_body = "This is a test email. " * 100
        
        response = client.post(
            "/api/v1/analyze",
            json={
                "subject": "Long email test",
                "body": long_body
            }
        )
        
        assert response.status_code == 200
    
    def test_analyze_response_structure(self):
        """Тест структуры ответа"""
        response = client.post(
            "/api/v1/analyze",
            json={
                "subject": "Test",
                "body": "Test content"
            }
        )
        
        assert response.status_code == 200
        
        data = response.json()
        
        # Проверяем обязательные поля
        required_fields = [
            "subject", "sentiment", "sentiment_score",
            "priority", "priority_score",
            "category", "category_confidence",
            "model", "processing_time_ms", "timestamp"
        ]
        
        for field in required_fields:
            assert field in data, f"Missing field: {field}"
        
        # Проверяем типы
        assert isinstance(data["sentiment_score"], float)
        assert isinstance(data["priority_score"], float)
        assert isinstance(data["category_confidence"], float)
        assert isinstance(data["processing_time_ms"], int)
        
        # Проверяем диапазоны
        assert 0.0 <= data["sentiment_score"] <= 1.0
        assert 0.0 <= data["priority_score"] <= 1.0
        assert 0.0 <= data["category_confidence"] <= 1.0


class TestBatchAnalyzeEndpoint:
    """Тесты для /api/v1/analyze/batch endpoint"""
    
    def test_batch_analyze_two_emails(self):
        """Тест пакетного анализа 2 писем"""
        response = client.post(
            "/api/v1/analyze/batch",
            json={
                "emails": [
                    {
                        "subject": "Meeting tomorrow",
                        "body": "Don't forget"
                    },
                    {
                        "subject": "Invoice #123",
                        "body": "Payment due"
                    }
                ]
            }
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "results" in data
        assert "total_emails" in data
        assert "total_processing_time_ms" in data
        assert "average_time_ms" in data
        
        assert len(data["results"]) == 2
        assert data["total_emails"] == 2
    
    def test_batch_analyze_empty_list(self):
        """Тест с пустым списком (должна быть ошибка)"""
        response = client.post(
            "/api/v1/analyze/batch",
            json={
                "emails": []
            }
        )
        
        assert response.status_code == 422
    
    def test_batch_analyze_single_email(self):
        """Тест пакетного анализа 1 письма"""
        response = client.post(
            "/api/v1/analyze/batch",
            json={
                "emails": [
                    {
                        "subject": "Test",
                        "body": "Test content"
                    }
                ]
            }
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["results"]) == 1
        assert data["total_emails"] == 1


class TestModelInfoEndpoint:
    """Тесты для /api/v1/analyze/model-info endpoint"""
    
    def test_get_model_info(self):
        """Тест получения информации о модели"""
        response = client.get("/api/v1/analyze/model-info")
        
        assert response.status_code == 200
        
        data = response.json()
        assert "model_name" in data
        assert "type" in data
        
        # Тип должен быть либо transformer-ml либо mock-fallback
        assert data["type"] in ["transformer-ml", "mock-fallback"]


def test_api_info():
    """Тест корневого endpoint API"""
    response = client.get("/api/v1")
    
    assert response.status_code == 200
    
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data


def test_root_redirect():
    """Тест редиректа с корня"""
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307  # Redirect
    assert response.headers["location"] == "/docs"


if __name__ == "__main__":
    # Запуск тестов
    pytest.main([__file__, "-v"])
