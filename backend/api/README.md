# 🌞 SolarMail REST API

**Sprint 0.3.2: FastAPI REST API for AI Email Analysis**

---

## 📋 Описание

REST API для AI-анализа электронных писем с использованием ML-моделей (DistilBERT, BART).

### Возможности:
- ✅ AI-анализ писем (sentiment, priority, category)
- ✅ Пакетный анализ (до 100 писем)
- ✅ Health checks и system status
- ✅ Автоматическая документация (Swagger UI)
- ✅ CORS support
- ✅ Логирование запросов
- ✅ Валидация с Pydantic v2

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
cd backend/api

# Установить FastAPI и зависимости
pip install -r requirements.txt

# Установить AI зависимости (если еще не установлены)
pip install transformers torch sentencepiece
```

### 2. Запуск сервера

**Способ 1: Через uvicorn (рекомендуется)**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Способ 2: Через Python**
```bash
python -m backend.api.main
```

**Способ 3: Напрямую**
```bash
python main.py
```

### 3. Открыть документацию

После запуска откройте в браузере:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Info**: http://localhost:8000/api/v1

---

## 📡 Endpoints

### 🧠 AI Analysis

#### `POST /api/v1/analyze`
Анализ одного письма

**Request:**
```json
{
  "subject": "Urgent: Critical bug in production",
  "body": "We have a critical issue that needs immediate attention.",
  "sender": "dev@company.com"
}
```

**Response:**
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
  "processing_time_ms": 1850,
  "timestamp": "2025-10-25T12:00:00"
}
```

#### `POST /api/v1/analyze/batch`
Пакетный анализ писем

**Request:**
```json
{
  "emails": [
    {
      "subject": "Meeting tomorrow",
      "body": "Don't forget about the meeting"
    },
    {
      "subject": "Invoice #123",
      "body": "Please find attached"
    }
  ]
}
```

**Response:**
```json
{
  "results": [...],
  "total_emails": 2,
  "total_processing_time_ms": 3500,
  "average_time_ms": 1750
}
```

#### `GET /api/v1/analyze/model-info`
Информация о ML модели

**Response:**
```json
{
  "transformer_ready": true,
  "model_name": "distilbert-base-uncased-finetuned-sst-2-english",
  "gpu_enabled": false,
  "type": "transformer-ml"
}
```

---

### 📊 System Status

#### `GET /api/v1/status`
Health check

**Response:**
```json
{
  "status": "ok",
  "version": "0.3.2",
  "uptime_seconds": 123.45,
  "ai_model_ready": true,
  "timestamp": "2025-10-25T12:00:00"
}
```

#### `GET /api/v1/status/detailed`
Детальный статус системы

**Response:**
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
    "type": "transformer-ml"
  }
}
```

#### `GET /api/v1/status/ping`
Простая проверка доступности

**Response:**
```json
{
  "message": "pong",
  "timestamp": "2025-10-25T12:00:00"
}
```

---

## 🧪 Тестирование

### cURL примеры

**Analyze email:**
```bash
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Thank you!",
    "body": "Great work on the project"
  }'
```

**Health check:**
```bash
curl "http://localhost:8000/api/v1/status"
```

**Model info:**
```bash
curl "http://localhost:8000/api/v1/analyze/model-info"
```

### Python примеры

```python
import requests

# Анализ письма
response = requests.post(
    "http://localhost:8000/api/v1/analyze",
    json={
        "subject": "Urgent: Bug in production",
        "body": "We have a critical issue..."
    }
)

result = response.json()
print(f"Sentiment: {result['sentiment']}")
print(f"Priority: {result['priority']}")
print(f"Category: {result['category']}")
```

---

## ⚙️ Конфигурация

### Переменные окружения

Можно настроить через переменные окружения с префиксом `SOLARMAIL_`:

```bash
# API настройки
export SOLARMAIL_HOST="0.0.0.0"
export SOLARMAIL_PORT=8000
export SOLARMAIL_DEBUG=true

# AI модель
export SOLARMAIL_AI_MODEL_NAME="distilbert-base-uncased-finetuned-sst-2-english"
export SOLARMAIL_AI_USE_GPU=false
export SOLARMAIL_AI_FALLBACK_TO_MOCK=true

# Логирование
export SOLARMAIL_LOG_LEVEL="INFO"
```

### Файл конфигурации

Редактировать `backend/api/core/config.py`:

```python
class APISettings(BaseSettings):
    app_name: str = "SolarMail AI API"
    port: int = 8000
    debug: bool = True
    # ...
```

---

## 📦 Структура проекта

```
backend/api/
├── main.py                 # FastAPI приложение
├── requirements.txt        # Зависимости
├── README.md              # Эта документация
├── core/
│   ├── __init__.py
│   └── config.py          # Конфигурация
├── models/
│   ├── __init__.py
│   └── email_analysis.py  # Pydantic модели
├── routes/
│   ├── __init__.py
│   ├── analyze.py         # AI analysis endpoints
│   └── status.py          # Health check endpoints
└── tests/
    ├── __init__.py
    ├── test_analyze.py
    └── test_status.py
```

---

## 🔧 Development

### Запуск в dev режиме

```bash
# С auto-reload
uvicorn main:app --reload --log-level debug

# Указать порт
uvicorn main:app --reload --port 8080
```

### Логи

По умолчанию логи выводятся в консоль. Формат:
```
2025-10-25 12:00:00 - uvicorn - INFO - Started server
2025-10-25 12:00:05 - backend.api.main - INFO - 📨 POST /api/v1/analyze
2025-10-25 12:00:06 - backend.api.main - INFO - ✅ POST /api/v1/analyze - 200
```

---

## 📈 Performance

### Время обработки

| Операция | Время (CPU) | Время (GPU) |
|----------|-------------|-------------|
| Analyze single email | 1-4 sec | 0.5-2 sec |
| Batch 10 emails | 10-40 sec | 5-20 sec |
| Health check | <10 ms | <10 ms |

### Rate Limiting

В текущей версии не включен. Будет добавлен в следующем спринте.

---

## 🔜 Roadmap (Sprint 0.3.3+)

- [ ] JWT аутентификация
- [ ] API keys
- [ ] Rate limiting
- [ ] Кэширование результатов
- [ ] WebSocket support для real-time анализа
- [ ] Prometheus metrics
- [ ] Docker контейнер

---

## 🐛 Troubleshooting

### Проблема: ModuleNotFoundError: No module named 'ai_parser_transformer'

**Решение:**
```bash
# Проверить, что core/sync в PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/../../core/sync"

# Или установить как пакет
cd ../../core/sync
pip install -e .
```

### Проблема: Port 8000 already in use

**Решение:**
```bash
# Использовать другой порт
uvicorn main:app --port 8001

# Или убить процесс на порту 8000
lsof -ti:8000 | xargs kill -9
```

### Проблема: AI model loading slow

**Причина:** Первая загрузка моделей (~1.9 GB) занимает 2-3 минуты

**Решение:** 
- Дождаться завершения загрузки
- Модели кэшируются в `~/.cache/huggingface/`
- Последующие запуски будут быстрыми

---

## 📚 Документация

- **API Docs**: http://localhost:8000/docs
- **Sprint 0.3.2 Summary**: `../../core/sync/SPRINT_0.3.2_SUMMARY.md`
- **ML Models**: `../../core/sync/INSTALL_TRANSFORMERS.md`

---

## 👥 Команда

- **Leanid** - Architect
- **Dashka** - Senior Engineer
- **Claude** - AI Engineer

---

**Создано командой SolarMail** 🌞  
**Версия:** 0.3.2  
**Дата:** 25 октября 2025
