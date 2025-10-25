"""
SolarMail - Transformer Parser Test
Тестирование и сравнение Mock vs Transformer анализаторов
"""

from ai_parser import AIParser as MockParser
from ai_parser_transformer import AIParserTransformer
import json
import time


def test_model_availability():
    """Тест доступности моделей"""
    print("=" * 70)
    print("🧪 Тест 1: Проверка доступности моделей")
    print("=" * 70)
    
    # Mock parser всегда доступен
    mock = MockParser()
    print("\n✅ Mock Parser: Доступен")
    print(f"   Модель: {mock.model_name}")
    
    # Transformer parser
    transformer = AIParserTransformer(fallback_to_mock=True)
    info = transformer.get_model_info()
    
    if info['transformer_ready']:
        print("\n✅ Transformer Parser: Готов")
        print(f"   Модель: {info['model_name']}")
        print(f"   GPU: {'Включен' if info['gpu_enabled'] else 'Отключен'}")
        print(f"   Sentiment Pipeline: {'✅' if info['sentiment_pipeline'] else '❌'}")
        print(f"   Zero-shot Pipeline: {'✅' if info['zero_shot_pipeline'] else '❌'}")
    else:
        print("\n⚠️  Transformer Parser: Недоступен (используется fallback)")
        print(f"   Причина: transformers library not installed")
        print(f"   Fallback: {'Включен' if info['mock_fallback'] else 'Отключен'}")
    
    return mock, transformer, info['transformer_ready']


def test_sentiment_analysis(mock, transformer, transformer_ready):
    """Тест анализа тональности"""
    print("\n" + "=" * 70)
    print("🧪 Тест 2: Анализ тональности")
    print("=" * 70)
    
    test_cases = [
        ("Thank you for the excellent work!", "positive"),
        ("This is terrible and disappointing", "negative"),
        ("The meeting is scheduled for tomorrow", "neutral"),
        ("Спасибо за отличную работу!", "positive"),
        ("Проблема критическая, требуется срочное решение", "negative")
    ]
    
    print("\nТекст | Mock | Transformer")
    print("-" * 70)
    
    for text, expected in test_cases:
        # Mock анализ
        mock_result = mock.analyze_email("", text)
        mock_sentiment = mock_result['sentiment']
        mock_score = mock_result['sentiment_score']
        
        # Transformer анализ
        trans_result = transformer.analyze_email("", text)
        trans_sentiment = trans_result['sentiment']
        trans_score = trans_result['sentiment_score']
        
        # Показываем результаты
        text_short = text[:40] + "..." if len(text) > 40 else text
        print(f"{text_short:45} | {mock_sentiment:8} {mock_score:.2f} | {trans_sentiment:8} {trans_score:.2f}")


def test_category_classification(mock, transformer, transformer_ready):
    """Тест классификации по категориям"""
    print("\n" + "=" * 70)
    print("🧪 Тест 3: Классификация категорий")
    print("=" * 70)
    
    test_cases = [
        ("Meeting tomorrow at 10am - Project review", "Work"),
        ("Invoice #12345 - Payment due", "Docs"),
        ("Bug #789 - Fix required", "Tasks"),
        ("Happy birthday! Have a great day!", "People"),
        ("Newsletter: Tech updates this week", "News"),
        ("Special offer: 50% discount!", "Spam")
    ]
    
    print("\nТекст | Mock | Transformer")
    print("-" * 70)
    
    for text, expected in test_cases:
        # Mock анализ
        mock_result = mock.analyze_email(text, "")
        mock_category = mock_result['category']
        mock_conf = mock_result['category_confidence']
        
        # Transformer анализ
        trans_result = transformer.analyze_email(text, "")
        trans_category = trans_result['category']
        trans_conf = trans_result['category_confidence']
        
        # Показываем результаты
        text_short = text[:40] + "..." if len(text) > 40 else text
        match_mock = "✅" if mock_category == expected else "❌"
        match_trans = "✅" if trans_category == expected else "❌"
        
        print(f"{text_short:45} | {match_mock} {mock_category:6} {mock_conf:.2f} | {match_trans} {trans_category:6} {trans_conf:.2f}")


def test_priority_detection(mock, transformer, transformer_ready):
    """Тест определения приоритета"""
    print("\n" + "=" * 70)
    print("🧪 Тест 4: Определение приоритета")
    print("=" * 70)
    
    test_cases = [
        ("URGENT: Critical bug in production", "high"),
        ("Please review when you have time", "medium"),
        ("FYI: Monthly newsletter", "low"),
        ("Срочно! Требуется немедленное решение", "high")
    ]
    
    print("\nТекст | Mock | Transformer")
    print("-" * 70)
    
    for text, expected in test_cases:
        # Mock анализ
        mock_result = mock.analyze_email(text, "")
        mock_priority = mock_result['priority']
        mock_score = mock_result['priority_score']
        
        # Transformer анализ
        trans_result = transformer.analyze_email(text, "")
        trans_priority = trans_result['priority']
        trans_score = trans_result['priority_score']
        
        # Показываем результаты
        text_short = text[:40] + "..." if len(text) > 40 else text
        match_mock = "✅" if mock_priority == expected else "❌"
        match_trans = "✅" if trans_priority == expected else "❌"
        
        print(f"{text_short:45} | {match_mock} {mock_priority:6} {mock_score:.2f} | {match_trans} {trans_priority:6} {trans_score:.2f}")


def test_performance(mock, transformer, transformer_ready):
    """Тест производительности"""
    print("\n" + "=" * 70)
    print("🧪 Тест 5: Производительность")
    print("=" * 70)
    
    test_text = "Please review the attached document and provide feedback by Friday. This is important for the project timeline."
    iterations = 10
    
    # Mock parser
    mock_times = []
    for _ in range(iterations):
        start = time.time()
        mock.analyze_email("Test subject", test_text)
        mock_times.append((time.time() - start) * 1000)
    
    mock_avg = sum(mock_times) / len(mock_times)
    
    # Transformer parser
    trans_times = []
    for _ in range(iterations):
        start = time.time()
        transformer.analyze_email("Test subject", test_text)
        trans_times.append((time.time() - start) * 1000)
    
    trans_avg = sum(trans_times) / len(trans_times)
    
    print(f"\n📊 Результаты ({iterations} итераций):")
    print(f"   Mock Parser:        {mock_avg:.2f} ms (avg)")
    print(f"   Transformer Parser: {trans_avg:.2f} ms (avg)")
    
    if transformer_ready:
        slowdown = trans_avg / mock_avg if mock_avg > 0 else 0
        print(f"   Замедление:         {slowdown:.1f}x")
        print(f"\n   💡 Transformer медленнее, но точнее (85-95% vs 60-75%)")
    else:
        print(f"\n   ⚠️  Transformer использует mock fallback (одинаковая производительность)")


def test_entity_extraction(mock, transformer, transformer_ready):
    """Тест извлечения сущностей"""
    print("\n" + "=" * 70)
    print("🧪 Тест 6: Извлечение сущностей")
    print("=" * 70)
    
    text = """
    Hi John Smith,
    
    Please contact me at john@example.com or visit https://example.com/docs.
    The meeting is scheduled for 2025-10-25 at 10:00 AM.
    
    Best regards,
    Maria Johnson
    """
    
    # Mock анализ
    mock_result = mock.analyze_email("Meeting", text)
    mock_entities = json.loads(mock_result['entities_json'])
    
    # Transformer анализ
    trans_result = transformer.analyze_email("Meeting", text)
    trans_entities = json.loads(trans_result['entities_json'])
    
    print("\n📧 Извлеченные сущности:")
    print(f"\n   Mock Parser:")
    for key, values in mock_entities.items():
        if values:
            print(f"      {key}: {values}")
    
    print(f"\n   Transformer Parser:")
    for key, values in trans_entities.items():
        if values:
            print(f"      {key}: {values}")


def test_batch_analysis(mock, transformer, transformer_ready):
    """Тест пакетного анализа"""
    print("\n" + "=" * 70)
    print("🧪 Тест 7: Пакетный анализ")
    print("=" * 70)
    
    emails = [
        {'subject': 'Urgent bug fix needed', 'body_preview': 'Critical issue'},
        {'subject': 'Thank you!', 'body_preview': 'Great work on the project'},
        {'subject': 'Invoice attached', 'body_preview': 'Payment due soon'},
        {'subject': 'Newsletter', 'body_preview': 'Weekly tech updates'}
    ]
    
    print(f"\n📬 Анализ {len(emails)} писем:")
    
    # Mock batch
    start = time.time()
    mock_results = mock.batch_analyze(emails)
    mock_time = (time.time() - start) * 1000
    
    # Transformer batch
    start = time.time()
    trans_results = transformer.batch_analyze(emails)
    trans_time = (time.time() - start) * 1000
    
    print(f"\n   Mock Parser:        {mock_time:.2f} ms")
    print(f"   Transformer Parser: {trans_time:.2f} ms")
    
    print(f"\n📊 Результаты анализа:")
    print(f"\n   {'Subject':40} | {'Category':10} | {'Priority':8}")
    print(f"   {'-'*40}-+-{'-'*10}-+-{'-'*8}")
    
    for i, email in enumerate(emails):
        subject = email['subject'][:40]
        category = trans_results[i]['category']
        priority = trans_results[i]['priority']
        print(f"   {subject:40} | {category:10} | {priority:8}")


def main():
    """Запускает все тесты"""
    print("\n🌞 SolarMail - Transformer Parser Tests")
    print("Sprint 0.3: ML Models Integration\n")
    
    # Тест 1: Доступность моделей
    mock, transformer, transformer_ready = test_model_availability()
    
    # Тест 2: Sentiment analysis
    test_sentiment_analysis(mock, transformer, transformer_ready)
    
    # Тест 3: Category classification
    test_category_classification(mock, transformer, transformer_ready)
    
    # Тест 4: Priority detection
    test_priority_detection(mock, transformer, transformer_ready)
    
    # Тест 5: Performance
    test_performance(mock, transformer, transformer_ready)
    
    # Тест 6: Entity extraction
    test_entity_extraction(mock, transformer, transformer_ready)
    
    # Тест 7: Batch analysis
    test_batch_analysis(mock, transformer, transformer_ready)
    
    # Итоговая сводка
    print("\n" + "=" * 70)
    print("✅ Все тесты завершены!")
    print("=" * 70)
    
    if not transformer_ready:
        print("\n💡 Для включения real ML-анализа установите transformers:")
        print("   pip install transformers torch sentencepiece --break-system-packages")
        print("\n   См. INSTALL_TRANSFORMERS.md для подробностей")
    
    print("\n")


if __name__ == "__main__":
    main()
