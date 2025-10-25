# 🌞 SolarMail - Sprint 0.2: AI Parser & Smart Cache

**AI-powered email intelligence + умный кэш-контроль**

## 🎯 Что нового

### ✨ AI Parser
- Тональность (positive/neutral/negative)
- Приоритет (high/medium/low)
- Категория (Work/Docs/Tasks/People/News/Spam)
- Извлечение сущностей и ключевых слов

### 🔄 Smart Cache
- Загрузка только новых писем
- Отслеживание last_sync_date
- Статистика синхронизации

### 📊 Новые таблицы
- `email_meta` - AI-метаданные
- `sync_status` - история синхронизации

## 💻 Быстрый старт

```python
from solar_sync import SolarSync

# Smart Sync с AI
sync = SolarSync(enable_ai=True)
sync.smart_sync()

# Получить письма с метаданными
emails = sync.db.get_emails_with_meta(limit=10)

# Фильтрация
urgent = sync.db.get_emails_by_priority('high')
work = sync.db.get_emails_by_category('Work')
```

## 🗄️ Структура БД

### Таблица email_meta
| Поле | Тип | Описание |
|------|-----|----------|
| email_id | INTEGER | FK к emails.id |
| sentiment | TEXT | positive/neutral/negative |
| priority | TEXT | high/medium/low |
| category | TEXT | Work/Docs/Tasks/etc |
| entities_json | TEXT | Извлеченные сущности |
| keywords_json | TEXT | Ключевые слова |

### Таблица sync_status  
| Поле | Тип | Описание |
|------|-----|----------|
| account_email | TEXT | Email аккаунта |
| last_sync_date | TEXT | Дата синхронизации |
| total_emails_synced | INTEGER | Всего синхронизировано |

## 🧠 AI Parser

```python
from ai_parser import AIParser

parser = AIParser()
meta = parser.analyze_email(subject, body)

# Результат:
{
    "sentiment": "positive",
    "priority": "high", 
    "category": "Work",
    "entities_json": "{...}",
    "keywords_json": "{...}"
}
```

## 🔄 Smart Cache

```python
# Первая синхронизация - последние 3 дня
sync.smart_sync()  # Загрузит 500 писем

# Вторая синхронизация - только новые
sync.smart_sync()  # Загрузит 5 новых (экономия 99%)
```

## 📊 Новые методы

### DatabaseManager
- `insert_email_meta(email_id, meta)`
- `get_email_meta(email_id)`
- `get_emails_with_meta(limit)`
- `get_emails_by_category(category)`
- `get_emails_by_priority(priority)`
- `get_last_sync_date(account)`
- `update_sync_status(account, date, stats)`

### SolarSync
- `smart_sync()` - умная синхронизация
- `analyze_emails_with_ai(emails)` - AI-анализ

## 🧪 Тестирование

```bash
# AI Parser demo
python ai_parser.py

# Sprint 0.2 demos
python demo_sprint_02.py
python demo_sprint_02.py --ai
python demo_sprint_02.py --categories
```

## 📈 Производительность

### AI Parser (Mock)
- Скорость: 0-2 мс/письмо
- Точность: 60-75% (эвристика)

### Smart Cache
- Экономия трафика: 90-99% после первой синхронизации

## 🔜 Sprint 0.3 Roadmap

- ML-модели (transformers)
- Расширенная аналитика
- Мультиаккаунт
- REST API

---

**Создано командой SolarMail** 🌞
Leanid (архитектор) | Dashka (senyor) | Claude (AI)


file
