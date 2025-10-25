"""
SolarMail - AI Parser Transformer
ML-анализ писем на базе Hugging Face transformers
Sprint 0.3: Real neural network models for email analysis
"""

import json
import time
import warnings
from typing import Dict, List, Any, Optional, Tuple

# Suppress warnings from transformers
warnings.filterwarnings('ignore')

# Try to import transformers
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️  transformers not installed, using mock fallback")

# Fallback to mock parser if transformers unavailable
if not TRANSFORMERS_AVAILABLE:
    try:
        from ai_parser import AIParser as MockParser
        MOCK_AVAILABLE = True
    except ImportError:
        MOCK_AVAILABLE = False


class AIParserTransformer:
    """
    AI анализатор на базе transformer моделей
    
    Использует pre-trained модели от Hugging Face для:
    - Sentiment analysis (тональность)
    - Text classification (категоризация)
    - Zero-shot classification (гибкая категоризация)
    """
    
    def __init__(
        self,
        model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
        use_gpu: bool = False,
        fallback_to_mock: bool = True
    ):
        """
        Инициализация transformer анализатора
        
        Args:
            model_name: Название модели от Hugging Face
            use_gpu: Использовать GPU (если доступен)
            fallback_to_mock: Использовать mock при ошибке загрузки модели
        """
        self.model_name = model_name
        self.use_gpu = use_gpu and torch.cuda.is_available() if TRANSFORMERS_AVAILABLE else False
        self.fallback_to_mock = fallback_to_mock
        
        # Статус инициализации
        self.transformer_ready = False
        self.mock_parser = None
        
        # Pipelines для разных задач
        self.sentiment_pipeline = None
        self.zero_shot_pipeline = None
        
        # Инициализируем модели
        self._init_models()
        
        # Категории для zero-shot classification
        self.categories = [
            "work and business",
            "documents and invoices", 
            "tasks and assignments",
            "personal and social",
            "news and updates",
            "spam and promotions"
        ]
        
        # Маппинг категорий на наши стандартные
        self.category_mapping = {
            "work and business": "Work",
            "documents and invoices": "Docs",
            "tasks and assignments": "Tasks",
            "personal and social": "People",
            "news and updates": "News",
            "spam and promotions": "Spam"
        }
    
    def _init_models(self):
        """Инициализация transformer моделей"""
        if not TRANSFORMERS_AVAILABLE:
            print("⚠️  transformers library not available")
            self._init_fallback()
            return
        
        try:
            print(f"🧠 Загрузка transformer модели: {self.model_name}")
            
            # Определяем device
            device = 0 if self.use_gpu else -1
            
            # Sentiment analysis pipeline
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=device
            )
            
            # Zero-shot classification для категорий
            try:
                self.zero_shot_pipeline = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=device
                )
                print("✅ Zero-shot classification загружен")
            except Exception as e:
                print(f"⚠️  Zero-shot недоступен: {e}")
                self.zero_shot_pipeline = None
            
            self.transformer_ready = True
            print(f"✅ Transformer модели готовы (GPU: {self.use_gpu})")
            
        except Exception as e:
            print(f"❌ Ошибка загрузки transformer: {e}")
            self._init_fallback()
    
    def _init_fallback(self):
        """Инициализация fallback на mock parser"""
        if self.fallback_to_mock and MOCK_AVAILABLE:
            print("🔄 Переключение на mock parser")
            self.mock_parser = MockParser(model_name="mock-fallback")
        else:
            print("❌ Fallback недоступен")
    
    def analyze_email(self, subject: str, body: str) -> Dict[str, Any]:
        """
        Анализирует письмо с помощью transformer моделей
        
        Args:
            subject: Тема письма
            body: Тело письма
        
        Returns:
            Словарь с AI-метаданными (совместимый с Sprint 0.2)
        """
        start_time = time.time()
        
        # Если transformer недоступен, используем fallback
        if not self.transformer_ready:
            if self.mock_parser:
                result = self.mock_parser.analyze_email(subject, body)
                result['ai_model'] = f"{self.model_name} (mock-fallback)"
                return result
            else:
                return self._generate_empty_result()
        
        # Объединяем тему и тело для анализа
        full_text = f"{subject or ''} {body or ''}"
        
        # Ограничиваем длину текста (BERT max 512 tokens)
        full_text = full_text[:2000]  # примерно 500 tokens
        
        # Анализируем тональность
        sentiment, sentiment_score = self._analyze_sentiment_transformer(full_text)
        
        # Анализируем категорию
        category, category_confidence = self._analyze_category_transformer(full_text)
        
        # Определяем приоритет (эвристика + sentiment)
        priority, priority_score = self._analyze_priority_hybrid(full_text, sentiment_score)
        
        # Извлекаем сущности (используем базовые regex паттерны)
        entities = self._extract_entities(subject or '', body or '')
        
        # Извлекаем ключевые слова
        keywords = self._extract_keywords(full_text)
        
        # Вычисляем время обработки
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            'sentiment': sentiment,
            'sentiment_score': sentiment_score,
            'priority': priority,
            'priority_score': priority_score,
            'category': category,
            'category_confidence': category_confidence,
            'entities_json': json.dumps(entities, ensure_ascii=False),
            'keywords_json': json.dumps(keywords, ensure_ascii=False),
            'ai_model': self.model_name,
            'processing_time_ms': processing_time_ms
        }
    
    def _analyze_sentiment_transformer(self, text: str) -> Tuple[str, float]:
        """
        Анализ тональности с помощью transformer
        
        Returns:
            Tuple (sentiment, score)
        """
        if not text.strip():
            return 'neutral', 0.5
        
        try:
            result = self.sentiment_pipeline(text)[0]
            label = result['label'].lower()
            score = result['score']
            
            # Маппинг POSITIVE/NEGATIVE на наши категории
            if label == 'positive':
                return 'positive', score
            elif label == 'negative':
                return 'negative', 1.0 - score  # инвертируем score для negative
            else:
                return 'neutral', 0.5
                
        except Exception as e:
            print(f"⚠️  Ошибка sentiment analysis: {e}")
            return 'neutral', 0.5
    
    def _analyze_category_transformer(self, text: str) -> Tuple[str, float]:
        """
        Анализ категории с помощью zero-shot classification
        
        Returns:
            Tuple (category, confidence)
        """
        if not self.zero_shot_pipeline or not text.strip():
            return 'General', 0.5
        
        try:
            result = self.zero_shot_pipeline(
                text,
                candidate_labels=self.categories,
                multi_label=False
            )
            
            # Получаем лучшую категорию
            best_category_raw = result['labels'][0]
            confidence = result['scores'][0]
            
            # Маппим на наши стандартные категории
            category = self.category_mapping.get(best_category_raw, 'General')
            
            return category, confidence
            
        except Exception as e:
            print(f"⚠️  Ошибка category analysis: {e}")
            return 'General', 0.5
    
    def _analyze_priority_hybrid(self, text: str, sentiment_score: float) -> Tuple[str, float]:
        """
        Гибридный анализ приоритета (ключевые слова + sentiment)
        
        Returns:
            Tuple (priority, score)
        """
        text_lower = text.lower()
        
        # Ключевые слова высокого приоритета
        high_priority_words = [
            'urgent', 'срочно', 'важно', 'critical', 'asap',
            'deadline', 'дедлайн', 'emergency', 'immediately'
        ]
        
        # Ключевые слова среднего приоритета
        medium_priority_words = [
            'важный', 'нужно', 'требуется', 'необходимо',
            'action required', 'please review'
        ]
        
        # Считаем совпадения
        high_count = sum(1 for word in high_priority_words if word in text_lower)
        medium_count = sum(1 for word in medium_priority_words if word in text_lower)
        
        # Учитываем негативную тональность (проблемы = высокий приоритет)
        negative_boost = 0.2 if sentiment_score < 0.4 else 0.0
        
        if high_count > 0:
            score = min(0.7 + (high_count * 0.1) + negative_boost, 1.0)
            return 'high', score
        elif medium_count > 0:
            score = min(0.4 + (medium_count * 0.1) + negative_boost, 0.7)
            return 'medium', score
        else:
            return 'low', 0.3
    
    def _extract_entities(self, subject: str, body: str) -> Dict[str, List[str]]:
        """
        Извлечение сущностей (базовые regex паттерны)
        
        В будущем можно интегрировать NER модели
        """
        import re
        
        text = f"{subject} {body}"
        
        entities = {
            'emails': [],
            'dates': [],
            'urls': [],
            'persons': []
        }
        
        # Email адреса
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities['emails'] = list(set(re.findall(email_pattern, text)))[:10]
        
        # Даты
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}\.\d{2}\.\d{4}',
            r'\d{1,2}/\d{1,2}/\d{4}'
        ]
        for pattern in date_patterns:
            entities['dates'].extend(re.findall(pattern, text))
        entities['dates'] = list(set(entities['dates']))[:10]
        
        # URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        entities['urls'] = list(set(re.findall(url_pattern, text)))[:10]
        
        return entities
    
    def _extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """
        Извлечение ключевых слов (простая эвристика)
        
        В будущем можно использовать TF-IDF или KeyBERT
        """
        import re
        
        # Стоп-слова
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'been',
            'в', 'и', 'на', 'с', 'по', 'для', 'от', 'к', 'из', 'это', 'быть'
        }
        
        # Извлекаем слова
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Фильтруем и подсчитываем
        word_freq = {}
        for word in words:
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Топ-10 слов
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords_list = [word for word, freq in top_keywords]
        
        return {
            'keywords': keywords_list,
            'topics': []  # В будущем можно добавить topic modeling
        }
    
    def _generate_empty_result(self) -> Dict[str, Any]:
        """Генерирует пустой результат при недоступности моделей"""
        return {
            'sentiment': 'neutral',
            'sentiment_score': 0.5,
            'priority': 'low',
            'priority_score': 0.3,
            'category': 'General',
            'category_confidence': 0.5,
            'entities_json': json.dumps({'emails': [], 'dates': [], 'urls': [], 'persons': []}, ensure_ascii=False),
            'keywords_json': json.dumps({'keywords': [], 'topics': []}, ensure_ascii=False),
            'ai_model': f"{self.model_name} (unavailable)",
            'processing_time_ms': 0
        }
    
    def batch_analyze(self, emails: List[Dict]) -> List[Dict]:
        """
        Пакетный анализ писем
        
        Args:
            emails: Список словарей с полями 'subject' и 'body_preview'
        
        Returns:
            Список словарей с AI-метаданными
        """
        results = []
        
        for email in emails:
            subject = email.get('subject', '')
            body = email.get('body_preview', '')
            
            meta = self.analyze_email(subject, body)
            results.append(meta)
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Информация о загруженных моделях
        
        Returns:
            Словарь с информацией о моделях
        """
        return {
            'transformer_ready': self.transformer_ready,
            'transformers_available': TRANSFORMERS_AVAILABLE,
            'model_name': self.model_name,
            'gpu_enabled': self.use_gpu,
            'sentiment_pipeline': self.sentiment_pipeline is not None,
            'zero_shot_pipeline': self.zero_shot_pipeline is not None,
            'mock_fallback': self.mock_parser is not None,
            'version': '0.3.0',
            'type': 'transformer-ml' if self.transformer_ready else 'mock-fallback'
        }


def demo_transformer():
    """Демонстрация работы transformer анализатора"""
    print("=" * 70)
    print("🧠 SolarMail AI Parser Transformer - Demo")
    print("=" * 70)
    
    # Инициализируем анализатор
    parser = AIParserTransformer(fallback_to_mock=True)
    
    # Показываем информацию о моделях
    model_info = parser.get_model_info()
    print(f"\n📊 Model Info:")
    print(f"   Transformer Ready: {'✅' if model_info['transformer_ready'] else '❌'}")
    print(f"   Model: {model_info['model_name']}")
    print(f"   GPU: {'✅' if model_info['gpu_enabled'] else '❌'}")
    print(f"   Type: {model_info['type']}")
    
    # Тестовые письма
    test_emails = [
        {
            'subject': 'Urgent: Critical bug in production',
            'body': 'We have a critical issue in production that needs immediate attention. The payment system is down and customers cannot complete purchases.'
        },
        {
            'subject': 'Thank you for the amazing work!',
            'body': 'I wanted to express my gratitude for the excellent job you did on the project. Everything exceeded our expectations!'
        },
        {
            'subject': 'Invoice #12345 - Payment Due',
            'body': 'Please find attached the invoice for services rendered. Payment is due by end of month.'
        },
        {
            'subject': 'Срочно: требуется ваше решение',
            'body': 'Добрый день! Нам необходимо принять решение по дедлайну проекта SolarMail. Прошу срочно ответить.'
        }
    ]
    
    print("\n📧 Анализ тестовых писем:\n")
    
    for i, email in enumerate(test_emails, 1):
        print(f"{i}. Тема: {email['subject']}")
        
        meta = parser.analyze_email(email['subject'], email['body'])
        
        print(f"   🎯 Приоритет: {meta['priority']} (score: {meta['priority_score']:.2f})")
        print(f"   📁 Категория: {meta['category']} (confidence: {meta['category_confidence']:.2f})")
        print(f"   😊 Тональность: {meta['sentiment']} (score: {meta['sentiment_score']:.2f})")
        print(f"   🤖 Модель: {meta['ai_model']}")
        print(f"   ⏱️  Время: {meta['processing_time_ms']} ms")
        print()
    
    print("=" * 70)


if __name__ == "__main__":
    demo_transformer()
