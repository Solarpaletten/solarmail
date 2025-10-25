"""
SolarMail - Demo Script
Демонстрационный скрипт для тестирования синхронизации
"""

from solar_sync import SolarSync
from db_manager import DatabaseManager


def demo_sync():
    """Демонстрация полного цикла синхронизации"""
    print("=" * 60)
    print("🌞 SolarMail - Demo синхронизации")
    print("=" * 60)
    
    # Создаем экземпляр SolarSync
    sync = SolarSync()
    
    # Запускаем синхронизацию
    try:
        sync.run()
    except Exception as e:
        print(f"\n⚠️ Примечание: Для работы необходимо настроить config.py")
        print(f"   с правильными учетными данными IMAP")
        return
    
    # Показываем последние 5 писем из кэша
    print("\n" + "=" * 60)
    print("📬 Последние 5 писем из локального кэша:")
    print("=" * 60)
    
    emails = sync.get_cached_emails(limit=5)
    
    for i, email in enumerate(emails, 1):
        print(f"\n{i}. От: {email['sender']}")
        print(f"   Тема: {email['subject']}")
        print(f"   Дата: {email['date']}")
        print(f"   Превью: {email['body_preview'][:80]}...")


def demo_database():
    """Демонстрация работы с базой данных"""
    print("=" * 60)
    print("💾 SolarMail - Demo работы с БД")
    print("=" * 60)
    
    db = DatabaseManager()
    
    # Статистика
    count = db.get_emails_count()
    print(f"\n📊 Всего писем в кэше: {count}")
    
    if count > 0:
        print("\n📋 Примеры писем:")
        emails = db.get_all_emails(limit=3)
        
        for email in emails:
            print(f"\n  • {email['subject']}")
            print(f"    От: {email['sender']}")
            print(f"    UID: {email['uid']}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--db-only":
        # Только демо базы данных
        demo_database()
    else:
        # Полная синхронизация
        demo_sync()
