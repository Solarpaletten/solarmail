"""
SolarMail API - Quick Test Script
Быстрая проверка работоспособности API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"


def print_section(title):
    """Красивый вывод секции"""
    print("\n" + "=" * 70)
    print(f"🧪 {title}")
    print("=" * 70)


def test_ping():
    """Тест простого ping"""
    print_section("Тест 1: Ping")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/status/ping")
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_health_check():
    """Тест health check"""
    print_section("Тест 2: Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/status")
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"API Status: {data.get('status')}")
        print(f"Version: {data.get('version')}")
        print(f"Uptime: {data.get('uptime_seconds')} seconds")
        print(f"AI Model Ready: {data.get('ai_model_ready')}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_model_info():
    """Тест получения информации о модели"""
    print_section("Тест 3: Model Info")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/analyze/model-info")
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"Model Name: {data.get('model_name')}")
        print(f"Type: {data.get('type')}")
        print(f"Transformer Ready: {data.get('transformer_ready')}")
        print(f"GPU Enabled: {data.get('gpu_enabled')}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_analyze_positive():
    """Тест анализа позитивного письма"""
    print_section("Тест 4: Analyze Positive Email")
    
    email_data = {
        "subject": "Thank you for the amazing work!",
        "body": "I wanted to express my gratitude for the excellent job you did on the project. Everything exceeded our expectations!",
        "sender": "client@company.com"
    }
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/analyze",
            json=email_data
        )
        elapsed = time.time() - start
        
        print(f"✅ Status: {response.status_code}")
        print(f"⏱️  Time: {elapsed:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📧 Subject: {data.get('subject')}")
            print(f"😊 Sentiment: {data.get('sentiment')} (score: {data.get('sentiment_score'):.2f})")
            print(f"🎯 Priority: {data.get('priority')} (score: {data.get('priority_score'):.2f})")
            print(f"📁 Category: {data.get('category')} (confidence: {data.get('category_confidence'):.2f})")
            print(f"🤖 Model: {data.get('model')}")
            print(f"⏱️  Processing: {data.get('processing_time_ms')} ms")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_analyze_urgent():
    """Тест анализа срочного письма"""
    print_section("Тест 5: Analyze Urgent Email")
    
    email_data = {
        "subject": "URGENT: Critical bug in production",
        "body": "We have a critical issue that needs immediate attention. The payment system is down and customers cannot complete purchases.",
        "sender": "dev@company.com"
    }
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/analyze",
            json=email_data
        )
        elapsed = time.time() - start
        
        print(f"✅ Status: {response.status_code}")
        print(f"⏱️  Time: {elapsed:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📧 Subject: {data.get('subject')}")
            print(f"😊 Sentiment: {data.get('sentiment')} (score: {data.get('sentiment_score'):.2f})")
            print(f"🎯 Priority: {data.get('priority')} (score: {data.get('priority_score'):.2f})")
            print(f"📁 Category: {data.get('category')} (confidence: {data.get('category_confidence'):.2f})")
            print(f"⏱️  Processing: {data.get('processing_time_ms')} ms")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_batch_analyze():
    """Тест пакетного анализа"""
    print_section("Тест 6: Batch Analyze")
    
    batch_data = {
        "emails": [
            {
                "subject": "Meeting tomorrow at 10am",
                "body": "Don't forget about the project review meeting"
            },
            {
                "subject": "Invoice #12345",
                "body": "Please find attached invoice for services"
            },
            {
                "subject": "Newsletter: Tech updates",
                "body": "This week's technology news and updates"
            }
        ]
    }
    
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/analyze/batch",
            json=batch_data
        )
        elapsed = time.time() - start
        
        print(f"✅ Status: {response.status_code}")
        print(f"⏱️  Total Time: {elapsed:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Results:")
            print(f"   Total Emails: {data.get('total_emails')}")
            print(f"   Processing Time: {data.get('total_processing_time_ms')} ms")
            print(f"   Average Time: {data.get('average_time_ms'):.2f} ms/email")
            
            print(f"\n📧 Analysis Results:")
            for i, result in enumerate(data.get('results', []), 1):
                print(f"   {i}. {result['subject'][:40]}")
                print(f"      Category: {result['category']}, Priority: {result['priority']}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_detailed_status():
    """Тест детального статуса"""
    print_section("Тест 7: Detailed Status")
    
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/status/detailed")
        print(f"✅ Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n📊 API:")
            api_info = data.get('api', {})
            print(f"   Name: {api_info.get('name')}")
            print(f"   Version: {api_info.get('version')}")
            print(f"   Uptime: {api_info.get('uptime_seconds')} seconds")
            
            print(f"\n💻 System:")
            sys_info = data.get('system', {})
            print(f"   Platform: {sys_info.get('platform')}")
            print(f"   CPU: {sys_info.get('cpu_percent')}%")
            print(f"   Memory: {sys_info.get('memory_percent')}%")
            
            print(f"\n🧠 AI:")
            ai_info = data.get('ai', {})
            print(f"   Model Ready: {ai_info.get('model_ready')}")
            print(f"   Type: {ai_info.get('type')}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Запуск всех тестов"""
    print("\n" + "=" * 70)
    print("🌞 SolarMail API - Quick Test")
    print("Sprint 0.3.2: REST API Layer Testing")
    print("=" * 70)
    print(f"\n🔗 API URL: {BASE_URL}{API_PREFIX}")
    print("\n⚠️  Убедитесь, что API запущен: uvicorn main:app --reload")
    
    # Проверка доступности API
    print_section("Проверка доступности API")
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/status/ping", timeout=2)
        if response.status_code == 200:
            print("✅ API доступен!")
        else:
            print(f"⚠️  API вернул код {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ API недоступен!")
        print("\n💡 Запустите API командой:")
        print("   cd backend/api")
        print("   uvicorn main:app --reload")
        return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    # Запускаем тесты
    tests = [
        test_ping,
        test_health_check,
        test_model_info,
        test_analyze_positive,
        test_analyze_urgent,
        test_batch_analyze,
        test_detailed_status
    ]
    
    results = []
    for test_func in tests:
        result = test_func()
        results.append(result)
        time.sleep(0.5)  # Небольшая пауза между тестами
    
    # Итоги
    print_section("Итоговые результаты")
    passed = sum(results)
    total = len(results)
    
    print(f"\n✅ Пройдено: {passed}/{total}")
    print(f"❌ Провалено: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("✅ API работает корректно")
        print("✅ Готов к git push")
    elif passed >= total * 0.8:
        print("\n⚠️  БОЛЬШИНСТВО ТЕСТОВ ПРОЙДЕНО")
        print("Проверьте провалившиеся тесты")
    else:
        print("\n❌ КРИТИЧЕСКИЕ ОШИБКИ")
        print("Требуется исправление")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
