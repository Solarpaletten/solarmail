"""
SolarMail - Database Test Script
Тестирование базы данных без реального IMAP подключения
"""

from core.sync.db_manager import DatabaseManager
from datetime import datetime, timedelta
import random


def generate_test_emails(count: int = 10):
    """Генерирует тестовые письма для проверки работы БД"""
    
    senders = [
        "alice@example.com",
        "bob@company.com",
        "charlie@mail.ru",
        "diana@outlook.com",
        "edward@gmail.com"
    ]
    
    subjects = [
        "Важное обновление проекта",
        "Встреча завтра в 10:00",
        "Отчет за квартал",
        "Re: Вопрос по документации",
        "Приглашение на вебинар",
        "Новые возможности платформы",
        "Подтверждение регистрации",
        "Weekly Newsletter #42",
        "Срочно: требуется ваше решение",
        "Спасибо за покупку!"
    ]
    
    emails = []
    
    for i in range(count):
        # Генерируем случайную дату за последние 3 дня
        days_ago = random.randint(0, 3)
        email_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        email = {
            'uid': f"test_uid_{i}_{random.randint(1000, 9999)}",
            'sender': random.choice(senders),
            'subject': random.choice(subjects),
            'date': email_date.isoformat(),
            'body_preview': f"Это тестовое письмо #{i+1}. Содержимое письма для проверки работы базы данных и синхронизации."
        }
        
        emails.append(email)
    
    return emails


def test_database():
    """Тестирует работу базы данных"""
    
    print("=" * 60)
    print("🧪 SolarMail - Тест базы данных")
    print("=" * 60)
    
    # Создаем менеджер БД
    db = DatabaseManager("test_solar_cache.db")
    
    print("\n1️⃣ Очистка тестовой БД...")
    db.clear_database()
    print(f"   Писем в БД: {db.get_emails_count()}")
    
    # Генерируем тестовые письма
    print("\n2️⃣ Генерация 15 тестовых писем...")
    test_emails = generate_test_emails(15)
    print(f"   Сгенерировано: {len(test_emails)} писем")
    
    # Добавляем письма в БД
    print("\n3️⃣ Добавление писем в базу данных...")
    new_count = 0
    duplicate_count = 0
    
    for email in test_emails:
        if db.insert_email(email):
            new_count += 1
        else:
            duplicate_count += 1
    
    print(f"   ✅ Добавлено: {new_count}")
    print(f"   ⏭️ Пропущено (дубли): {duplicate_count}")
    print(f"   📊 Всего в БД: {db.get_emails_count()}")
    
    # Тестируем дубликаты
    print("\n4️⃣ Тест защиты от дубликатов...")
    duplicate_email = test_emails[0]  # Пытаемся добавить первое письмо снова
    if not db.insert_email(duplicate_email):
        print("   ✅ Дубликат успешно отклонен")
    else:
        print("   ❌ ОШИБКА: дубликат был добавлен!")
    
    # Проверяем существование письма
    print("\n5️⃣ Проверка существования письма...")
    test_uid = test_emails[0]['uid']
    if db.email_exists(test_uid):
        print(f"   ✅ Письмо с UID {test_uid} найдено")
    else:
        print(f"   ❌ ОШИБКА: письмо не найдено!")
    
    # Получаем последние 5 писем
    print("\n6️⃣ Получение последних 5 писем из БД...")
    recent_emails = db.get_all_emails(limit=5)
    
    for i, email in enumerate(recent_emails, 1):
        print(f"\n   {i}. От: {email['sender']}")
        print(f"      Тема: {email['subject']}")
        print(f"      Дата: {email['date'][:19]}")
        print(f"      UID: {email['uid']}")
    
    # Итоговая статистика
    print("\n" + "=" * 60)
    print("✅ Тест успешно завершен!")
    print(f"📊 Итого писем в тестовой БД: {db.get_emails_count()}")
    print("=" * 60)
    print(f"\n💾 Тестовая БД сохранена: test_solar_cache.db")
    print("   Вы можете открыть её любым SQLite клиентом для проверки")


if __name__ == "__main__":
    test_database()
