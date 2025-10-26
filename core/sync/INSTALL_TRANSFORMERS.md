# 🧠 Установка AI Transformers для SolarMail

## Sprint 0.3: ML Models Integration

---

## 📋 Системные требования

### Минимальные:
- Python 3.11+
- 4 GB RAM
- 2 GB свободного места на диске

### Рекомендуемые:
- Python 3.11+
- 8 GB RAM
- NVIDIA GPU с CUDA (опционально, для ускорения)
- 5 GB свободного места на диске

---

## 🔧 Установка зависимостей

### Вариант 1: CPU only (без GPU)

```bash
# Устанавливаем transformers и torch (CPU версия)
pip install transformers torch sentencepiece --break-system-packages

# Или из requirements.txt
pip install -r requirements.txt --break-system-packages
```

### Вариант 2: С поддержкой GPU (CUDA)

```bash
# Установка torch с CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 --break-system-packages

# Затем transformers
pip install transformers sentencepiece --break-system-packages
```

---

## 📦 Загрузка моделей

### Автоматическая загрузка (рекомендуется)

При первом запуске модели загрузятся автоматически:

```python
from ai_parser_transformer import AIParserTransformer

# Модели загрузятся из Hugging Face Hub
parser = AIParserTransformer()
```

**Модели, которые будут загружены:**
1. `distilbert-base-uncased-finetuned-sst-2-english` (~260 MB)
   - Sentiment analysis
2. `facebook/bart-large-mnli` (~1.6 GB)
   - Zero-shot classification для категорий

**Общий размер:** ~1.9 GB

### Ручная загрузка (опционально)

```python
from transformers import pipeline

# Загрузить sentiment model
sentiment = pipeline("sentiment-analysis", 
                     model="distilbert-base-uncased-finetuned-sst-2-english")

# Загрузить zero-shot model
zero_shot = pipeline("zero-shot-classification",
                     model="facebook/bart-large-mnli")
```

---

## ✅ Проверка установки

### Тест 1: Проверка базовой работы

```bash
cd /core/sync
python ai_parser_transformer.py
```

**Ожидаемый результат (с установленными моделями):**

```
🧠 Загрузка transformer модели: distilbert-base-uncased-finetuned-sst-2-english
✅ Zero-shot classification загружен
✅ Transformer модели готовы (GPU: ❌)

📊 Model Info:
   Transformer Ready: ✅
   Model: distilbert-base-uncased-finetuned-sst-2-english
   Type: transformer-ml
```

**Если модели НЕ установлены:**

```
⚠️  transformers not installed, using mock fallback
🔄 Переключение на mock parser
Type: mock-fallback
```

### Тест 2: Проверка анализа письма

```python
from ai_parser_transformer import AIParserTransformer

parser = AIParserTransformer()

# Получаем информацию о модели
info = parser.get_model_info()
print(f"Transformer Ready: {info['transformer_ready']}")
print(f"Type: {info['type']}")

# Анализируем письмо
result = parser.analyze_email(
    subject="Great work!",
    body="Thank you for the excellent job!"
)

print(f"Sentiment: {result['sentiment']}")
print(f"Score: {result['sentiment_score']:.2f}")
```

---

## 🚀 Использование

### Базовое использование

```python
from ai_parser_transformer import AIParserTransformer

# Инициализация (автоматически загрузит модели)
parser = AIParserTransformer()

# Анализ письма
meta = parser.analyze_email(
    subject="Urgent: Bug in production",
    body="We have a critical issue..."
)

print(f"Priority: {meta['priority']}")      # high
print(f"Category: {meta['category']}")      # Work
print(f"Sentiment: {meta['sentiment']}")    # negative
```

### С GPU (если доступен)

```python
# Включить GPU
parser = AIParserTransformer(use_gpu=True)

# Проверить, используется ли GPU
info = parser.get_model_info()
print(f"GPU Enabled: {info['gpu_enabled']}")
```

### Пакетный анализ

```python
emails = [
    {'subject': 'Meeting tomorrow', 'body_preview': '...'},
    {'subject': 'Invoice #123', 'body_preview': '...'}
]

# Анализ всех писем
results = parser.batch_analyze(emails)

for result in results:
    print(f"{result['subject']}: {result['category']}")
```

### Интеграция с SolarSync

```python
from solar_sync import SolarSync
from ai_parser_transformer import AIParserTransformer

# Создаем sync с transformer parser
sync = SolarSync()
sync.ai_parser = AIParserTransformer()
sync.enable_ai = True

# Запускаем умную синхронизацию с ML-анализом
sync.smart_sync()
```

---

## 🔍 Устранение неполадок

### Проблема: ModuleNotFoundError: No module named 'transformers'

**Решение:**
```bash
pip install transformers torch sentencepiece --break-system-packages
```

### Проблема: "CUDA out of memory"

**Решение 1:** Используйте CPU mode
```python
parser = AIParserTransformer(use_gpu=False)
```

**Решение 2:** Используйте меньшую модель
```python
parser = AIParserTransformer(
    model_name="distilbert-base-uncased"  # меньше памяти
)
```

### Проблема: Медленная загрузка моделей

**Причина:** Модели загружаются из интернета при первом запуске

**Решение:** Дождитесь завершения загрузки. Последующие запуски будут быстрыми (модели кэшируются).

**Где хранятся модели:**
- Linux/Mac: `~/.cache/huggingface/`
- Windows: `C:\Users\<username>\.cache\huggingface\`

### Проблема: ImportError: cannot import name 'pipeline'

**Решение:** Обновите transformers
```bash
pip install --upgrade transformers --break-system-packages
```

---

## 📊 Сравнение производительности

| Режим | Скорость (мс/письмо) | Точность | Память |
|-------|---------------------|----------|---------|
| Mock (Sprint 0.2) | 0-2 ms | 60-75% | ~5 MB |
| Transformer CPU | 50-200 ms | 85-95% | ~2 GB |
| Transformer GPU | 10-50 ms | 85-95% | ~3 GB VRAM |

---

## 🎯 Рекомендуемые модели

### Sentiment Analysis
- `distilbert-base-uncased-finetuned-sst-2-english` ✅ (используется по умолчанию)
- `cardiffnlp/twitter-roberta-base-sentiment`
- `nlptown/bert-base-multilingual-uncased-sentiment`

### Zero-shot Classification
- `facebook/bart-large-mnli` ✅ (используется по умолчанию)
- `joeddav/xlm-roberta-large-xnli`
- `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`

---

## 🔜 Будущие улучшения (Sprint 0.4+)

- Fine-tuning на email корпусах
- Поддержка мультиязычных моделей
- NER (Named Entity Recognition) для извлечения сущностей
- Custom модели для email-специфичных задач
- Кэширование результатов анализа

---

## 📚 Дополнительные ресурсы

- [Hugging Face Documentation](https://huggingface.co/docs/transformers)
- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)

---

**Создано командой SolarMail** 🌞
Sprint 0.3: AI Transformers Integration
