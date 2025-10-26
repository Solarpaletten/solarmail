"""
SolarMail - Quick Pre-Push Test
Быстрая проверка перед git push
"""

import sys
import traceback

print("=" * 70)
print("🧪 ПРЕДВАРИТЕЛЬНОЕ ТЕСТИРОВАНИЕ SolarMail v0.3.1")
print("=" * 70)

test_results = []

# ============================================================================
# ТЕСТ 1: Импорты модулей
# ============================================================================
print("\n1️⃣  Тест импортов модулей...")

try:
    from ai_parser import AIParser
    print("   ✅ ai_parser.py")
    test_results.append(("Import ai_parser", True, "OK"))
except Exception as e:
    print(f"   ❌ ai_parser.py: {e}")
    test_results.append(("Import ai_parser", False, str(e)))

try:
    from ai_parser_transformer import AIParserTransformer
    print("   ✅ ai_parser_transformer.py")
    test_results.append(("Import ai_parser_transformer", True, "OK"))
except Exception as e:
    print(f"   ❌ ai_parser_transformer.py: {e}")
    test_results.append(("Import ai_parser_transformer", False, str(e)))

try:
    from db_manager import DatabaseManager
    print("   ✅ db_manager.py")
    test_results.append(("Import db_manager", True, "OK"))
except Exception as e:
    print(f"   ❌ db_manager.py: {e}")
    test_results.append(("Import db_manager", False, str(e)))

try:
    from solar_sync import SolarSync
    print("   ✅ solar_sync.py")
    test_results.append(("Import solar_sync", True, "OK"))
except Exception as e:
    print(f"   ❌ solar_sync.py: {e}")
    test_results.append(("Import solar_sync", False, str(e)))

# ============================================================================
# ТЕСТ 2: AI Parser Mock
# ============================================================================
print("\n2️⃣  Тест Mock AI Parser (Sprint 0.2)...")

try:
    parser = AIParser()
    result = parser.analyze_email(
        "Urgent: Critical issue",
        "We have a problem that needs attention"
    )
    
    assert 'sentiment' in result
    assert 'priority' in result
    assert 'category' in result
    assert result['priority'] == 'high'
    
    print(f"   ✅ Анализ работает")
    print(f"      Priority: {result['priority']}, Category: {result['category']}")
    test_results.append(("Mock AI Parser", True, "OK"))
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    test_results.append(("Mock AI Parser", False, str(e)))

# ============================================================================
# ТЕСТ 3: Transformer Parser
# ============================================================================
print("\n3️⃣  Тест Transformer AI Parser (Sprint 0.3)...")

try:
    parser_trans = AIParserTransformer(fallback_to_mock=True)
    info = parser_trans.get_model_info()
    
    print(f"   Transformer Ready: {info['transformer_ready']}")
    print(f"   Type: {info['type']}")
    
    result = parser_trans.analyze_email(
        "Thank you for great work",
        "Excellent job on the project"
    )
    
    assert 'sentiment' in result
    assert result['sentiment'] == 'positive'
    
    print(f"   ✅ Анализ работает (fallback: {not info['transformer_ready']})")
    print(f"      Sentiment: {result['sentiment']}, Score: {result['sentiment_score']:.2f}")
    test_results.append(("Transformer AI Parser", True, f"Type: {info['type']}"))
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    test_results.append(("Transformer AI Parser", False, str(e)))

# ============================================================================
# ТЕСТ 4: База данных
# ============================================================================
print("\n4️⃣  Тест базы данных...")

try:
    db = DatabaseManager("test_quick.db")
    
    # Проверяем таблицы
    count = db.get_emails_count()
    print(f"   ✅ База инициализирована")
    print(f"      Писем в БД: {count}")
    
    # Тестовое письмо
    test_email = {
        'uid': 'test_quick_001',
        'sender': 'test@example.com',
        'subject': 'Test email',
        'date': '2025-10-25T12:00:00',
        'body_preview': 'Test content'
    }
    
    if db.insert_email(test_email):
        print(f"   ✅ Вставка письма работает")
    
    # Тест AI метаданных
    emails = db.get_all_emails(limit=1)
    if emails:
        meta = {
            'sentiment': 'positive',
            'sentiment_score': 0.8,
            'priority': 'medium',
            'priority_score': 0.6,
            'category': 'Work',
            'category_confidence': 0.9,
            'entities_json': '{}',
            'keywords_json': '{}',
            'ai_model': 'test',
            'processing_time_ms': 10
        }
        
        if db.insert_email_meta(emails[0]['id'], meta):
            print(f"   ✅ AI метаданные работают")
    
    test_results.append(("Database", True, "OK"))
    
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    test_results.append(("Database", False, str(e)))

# ============================================================================
# ТЕСТ 5: Совместимость API
# ============================================================================
print("\n5️⃣  Тест совместимости API...")

try:
    # Mock parser
    mock = AIParser()
    mock_result = mock.analyze_email("Test", "Test body")
    
    # Transformer parser
    trans = AIParserTransformer()
    trans_result = trans.analyze_email("Test", "Test body")
    
    # Проверяем одинаковые ключи
    mock_keys = set(mock_result.keys())
    trans_keys = set(trans_result.keys())
    
    if mock_keys == trans_keys:
        print(f"   ✅ API совместим между Mock и Transformer")
        print(f"      Ключей в результате: {len(mock_keys)}")
        test_results.append(("API Compatibility", True, "OK"))
    else:
        missing = mock_keys - trans_keys or trans_keys - mock_keys
        print(f"   ⚠️  Различия в ключах: {missing}")
        test_results.append(("API Compatibility", False, f"Different keys: {missing}"))
    
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    test_results.append(("API Compatibility", False, str(e)))

# ============================================================================
# ТЕСТ 6: Requirements
# ============================================================================
print("\n6️⃣  Тест requirements.txt...")

try:
    with open('requirements.txt', 'r') as f:
        content = f.read()
        
    # Проверяем наличие ключевых зависимостей
    required = ['imap-tools', 'transformers', 'torch']
    found = []
    
    for req in required:
        if req in content:
            found.append(req)
            print(f"   ✅ {req}")
    
    if len(found) == len(required):
        test_results.append(("Requirements", True, "All dependencies present"))
    else:
        missing = set(required) - set(found)
        test_results.append(("Requirements", False, f"Missing: {missing}"))
    
except Exception as e:
    print(f"   ❌ Ошибка: {e}")
    test_results.append(("Requirements", False, str(e)))

# ============================================================================
# ИТОГОВАЯ СВОДКА
# ============================================================================
print("\n" + "=" * 70)
print("📊 ИТОГОВАЯ СВОДКА")
print("=" * 70)

passed = sum(1 for _, success, _ in test_results if success)
total = len(test_results)

print(f"\n✅ Пройдено: {passed}/{total}")
print(f"❌ Провалено: {total - passed}/{total}")

print("\n📋 Детали:\n")
for name, success, details in test_results:
    status = "✅" if success else "❌"
    print(f"   {status} {name:30} - {details}")

# Финальная оценка
print("\n" + "=" * 70)
if passed == total:
    print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! Готов к git push")
    print("=" * 70)
    sys.exit(0)
elif passed >= total * 0.8:
    print("⚠️  БОЛЬШИНСТВО ТЕСТОВ ПРОЙДЕНО. Проверьте ошибки перед push")
    print("=" * 70)
    sys.exit(0)
else:
    print("❌ КРИТИЧЕСКИЕ ОШИБКИ. Не рекомендуется push")
    print("=" * 70)
    sys.exit(1)
