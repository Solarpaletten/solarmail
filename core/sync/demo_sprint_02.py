"""
SolarMail - Sprint 0.2 Demo
Демонстрация AI-анализа и Smart Cache
"""

from solar_sync import SolarSync
from db_manager import DatabaseManager
from ai_parser import AIParser
import json


def demo_ai_analysis():
    """Демонстрация AI-анализа писем"""
    print("=" * 70)
    print("🧠 Sprint 0.2 Demo: AI-анализ писем")
    print("=" * 70)
    
    db = DatabaseManager("demo_sprint_02.db")
    parser = AIParser()
    
    # Получаем последние письма из кэша
    emails = db.get_all_emails(limit=5)
    
    if not emails:
        print("\n⚠️  Нет писем в кэше для анализа.")
        print("   Сначала запустите синхронизацию с IMAP или используйте test_db.py")
        return
    
    print(f"\n📧 Анализируем {len(emails)} писем из кэша...\n")
    
    for i, email in enumerate(emails, 1):
        print(f"{i}. От: {email['sender']}")
        print(f"   Тема: {email['subject']}")
        print(f"   Дата: {email['date']}")
        
        # Проверяем, есть ли уже AI-метаданные
        existing_meta = db.get_email_meta(email['id'])
        
        if existing_meta:
            print(f"   ✅ AI-метаданные уже существуют")
            meta = existing_meta
        else:
            # Анализируем письмо
            meta = parser.analyze_email(
                email['subject'],
                email.get('body_preview', '')
            )
            # Сохраняем метаданные
            db.insert_email_meta(email['id'], meta)
            print(f"   🧠 AI-анализ выполнен")
        
        # Показываем результаты анализа
        print(f"   🎯 Приоритет: {meta['priority']} (score: {meta.get('priority_score', 0):.2f})")
        print(f"   📁 Категория: {meta['category']} (confidence: {meta.get('category_confidence', 0):.2f})")
        print(f"   😊 Тональность: {meta['sentiment']} (score: {meta.get('sentiment_score', 0):.2f})")
        
        # Показываем сущности
        if isinstance(meta.get('entities_json'), str):
            entities = json.loads(meta['entities_json'])
        else:
            entities = meta.get('entities_json', {})
        
        if any(entities.values()):
            entity_summary = ', '.join([f"{k}={len(v)}" for k, v in entities.items() if v])
            print(f"   🔍 Сущности: {entity_summary}")
        
        # Показываем ключевые слова
        if isinstance(meta.get('keywords_json'), str):
            keywords = json.loads(meta['keywords_json'])
        else:
            keywords = meta.get('keywords_json', {})
        
        if keywords.get('keywords'):
            print(f"   🏷️  Ключевые слова: {', '.join(keywords['keywords'][:5])}")
        
        print()


def demo_smart_cache():
    """Демонстрация Smart Cache"""
    print("=" * 70)
    print("🔄 Sprint 0.2 Demo: Smart Cache")
    print("=" * 70)
    
    db = DatabaseManager("demo_sprint_02.db")
    
    # Показываем статус синхронизации
    print("\n📊 Статус синхронизации:\n")
    
    statuses = db.get_all_sync_statuses()
    
    if not statuses:
        print("   ⚠️  Нет данных о синхронизации.")
        print("   Запустите smart_sync() для создания записей.")
        return
    
    for status in statuses:
        print(f"📧 Аккаунт: {status['account_email']}")
        print(f"   Последняя синхронизация: {status.get('last_sync_date', 'Никогда')}")
        print(f"   Успешность: {'✅ Да' if status.get('last_sync_success') else '❌ Нет'}")
        print(f"   Всего синхронизировано: {status.get('total_emails_synced', 0)} писем")
        print(f"   Последняя партия: {status.get('last_batch_count', 0)} писем")
        print(f"   Период синхронизации: {status.get('sync_days', 3)} дней")
        
        if status.get('last_error_message'):
            print(f"   ⚠️  Последняя ошибка: {status['last_error_message']}")
        
        print(f"   Создано: {status.get('created_at', 'N/A')}")
        print(f"   Обновлено: {status.get('updated_at', 'N/A')}")
        print()


def demo_category_filter():
    """Демонстрация фильтрации по категориям"""
    print("=" * 70)
    print("📁 Sprint 0.2 Demo: Фильтрация по категориям")
    print("=" * 70)
    
    db = DatabaseManager("demo_sprint_02.db")
    
    categories = ['Work', 'Docs', 'Tasks', 'People', 'News', 'Spam']
    
    print("\n📊 Распределение писем по категориям:\n")
    
    for category in categories:
        emails = db.get_emails_by_category(category, limit=100)
        count = len(emails)
        
        if count > 0:
            print(f"   📁 {category}: {count} писем")
            
            # Показываем примеры
            if emails:
                print(f"      Примеры:")
                for email in emails[:2]:
                    print(f"      • {email.get('subject', '(No Subject)')[:50]}")
    
    print("\n" + "=" * 70)


def demo_priority_filter():
    """Демонстрация фильтрации по приоритету"""
    print("=" * 70)
    print("🎯 Sprint 0.2 Demo: Фильтрация по приоритету")
    print("=" * 70)
    
    db = DatabaseManager("demo_sprint_02.db")
    
    priorities = ['high', 'medium', 'low']
    
    print("\n📊 Распределение писем по приоритету:\n")
    
    for priority in priorities:
        emails = db.get_emails_by_priority(priority, limit=100)
        count = len(emails)
        
        if count > 0:
            emoji = '🔴' if priority == 'high' else '🟡' if priority == 'medium' else '🟢'
            print(f"   {emoji} {priority.capitalize()}: {count} писем")
            
            # Показываем примеры высокого приоритета
            if priority == 'high' and emails:
                print(f"      Примеры:")
                for email in emails[:3]:
                    print(f"      • {email.get('subject', '(No Subject)')[:50]}")
                    print(f"        Score: {email.get('priority_score', 0):.2f}")
    
    print("\n" + "=" * 70)


def demo_full_integration():
    """Полная демонстрация интеграции"""
    print("=" * 70)
    print("🚀 Sprint 0.2 Demo: Полная интеграция AI + Smart Cache")
    print("=" * 70)
    
    print("\n📝 Демонстрация использования SolarSync с AI:\n")
    
    code_example = """
# Пример 1: Базовая синхронизация (без AI)
from solar_sync import SolarSync

sync = SolarSync()
sync.run()

# Пример 2: Smart Sync (без AI)
sync = SolarSync()
sync.smart_sync()  # Загрузит только новые письма

# Пример 3: Smart Sync с AI-анализом
sync = SolarSync(enable_ai=True)
sync.smart_sync()  # Загрузит + проанализирует новые письма

# Пример 4: Получение проанализированных писем
emails = sync.db.get_emails_with_meta(limit=10)
for email in emails:
    print(f"Тема: {email['subject']}")
    print(f"Категория: {email['category']}")
    print(f"Приоритет: {email['priority']}")

# Пример 5: Фильтрация по категориям
work_emails = sync.db.get_emails_by_category('Work', limit=20)
high_priority = sync.db.get_emails_by_priority('high', limit=10)
"""
    
    print(code_example)
    print("=" * 70)


def main():
    """Главная функция демо"""
    import sys
    
    if len(sys.argv) > 1:
        demo_type = sys.argv[1]
        
        if demo_type == '--ai':
            demo_ai_analysis()
        elif demo_type == '--cache':
            demo_smart_cache()
        elif demo_type == '--categories':
            demo_category_filter()
        elif demo_type == '--priority':
            demo_priority_filter()
        elif demo_type == '--integration':
            demo_full_integration()
        else:
            print(f"❌ Неизвестный тип демо: {demo_type}")
            print_usage()
    else:
        # Показываем все демо по очереди
        demo_full_integration()
        print("\n" * 2)
        demo_ai_analysis()
        print("\n" * 2)
        demo_smart_cache()
        print("\n" * 2)
        demo_category_filter()
        print("\n" * 2)
        demo_priority_filter()


def print_usage():
    """Показывает использование"""
    print("""
📖 Использование:
    python demo_sprint_02.py                  # Все демо
    python demo_sprint_02.py --ai            # Только AI-анализ
    python demo_sprint_02.py --cache         # Только Smart Cache
    python demo_sprint_02.py --categories    # Фильтрация по категориям
    python demo_sprint_02.py --priority      # Фильтрация по приоритету
    python demo_sprint_02.py --integration   # Примеры интеграции
    """)


if __name__ == "__main__":
    main()
