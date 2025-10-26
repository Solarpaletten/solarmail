"""
SolarMail - AI Parser Module
Интеллектуальный анализ писем: тональность, приоритет, категория, сущности
Sprint 0.2: Mock-анализ на основе эвристики и ключевых слов
"""

import re
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime


class AIParser:
    """Интеллектуальный анализатор писем"""
    
    def __init__(self, model_name: str = "dashka-solar-mini"):
        """
        Инициализация AI Parser
        
        Args:
            model_name: Название модели для анализа
        """
        self.model_name = model_name
        
        # Ключевые слова для определения приоритета
        self.priority_keywords = {
            'high': [
                'urgent', 'срочно', 'важно', 'critical', 'asap', 
                'deadline', 'дедлайн', 'emergency', 'immediately',
                'требуется немедленно', 'прошу срочно'
            ],
            'medium': [
                'важный', 'нужно', 'требуется', 'необходимо',
                'please review', 'action required', 'обратите внимание'
            ]
        }
        
        # Ключевые слова для определения категории
        self.category_keywords = {
            'Work': [
                'meeting', 'встреча', 'project', 'проект', 'task', 'задача',
                'deadline', 'дедлайн', 'report', 'отчет', 'presentation',
                'презентация', 'conference', 'конференция', 'sprint',
                'review', 'ревью', 'merge', 'deploy', 'code', 'код'
            ],
            'Docs': [
                'invoice', 'счет', 'contract', 'договор', 'agreement',
                'document', 'документ', 'pdf', 'file', 'файл',
                'attachment', 'вложение', 'scan', 'скан'
            ],
            'Tasks': [
                'todo', 'делать', 'task', 'задание', 'action item',
                'assign', 'назначено', 'complete', 'завершить',
                'issue', 'тикет', 'bug', 'баг', 'fix', 'исправить'
            ],
            'People': [
                'birthday', 'день рождения', 'congratulations', 'поздравляем',
                'welcome', 'добро пожаловать', 'hello', 'привет',
                'thanks', 'спасибо', 'thank you', 'regards'
            ],
            'News': [
                'newsletter', 'новости', 'update', 'обновление',
                'announcement', 'объявление', 'release', 'релиз',
                'version', 'версия', 'changelog'
            ],
            'Spam': [
                'unsubscribe', 'отписаться', 'discount', 'скидка',
                'offer', 'предложение', 'win', 'выиграть', 'prize',
                'click here', 'нажмите здесь', 'free', 'бесплатно'
            ]
        }
        
        # Ключевые слова для определения тональности
        self.sentiment_keywords = {
            'positive': [
                'thanks', 'спасибо', 'great', 'отлично', 'excellent',
                'прекрасно', 'good', 'хорошо', 'perfect', 'идеально',
                'love', 'нравится', 'amazing', 'потрясающе', 'wonderful',
                'appreciate', 'ценю', 'congratulations', 'поздравляю'
            ],
            'negative': [
                'problem', 'проблема', 'issue', 'ошибка', 'error',
                'failed', 'провалено', 'wrong', 'неправильно', 'bad',
                'плохо', 'terrible', 'ужасно', 'disappointed', 'разочарован',
                'complaint', 'жалоба', 'urgent', 'срочно', 'critical'
            ]
        }
        
    def analyze_email(self, subject: str, body: str) -> Dict[str, Any]:
        """
        Анализирует письмо и возвращает JSON-структуру метаданных
        
        Args:
            subject: Тема письма
            body: Тело письма (может быть preview)
        
        Returns:
            Словарь с AI-метаданными
        """
        start_time = time.time()
        
        # Объединяем тему и тело для анализа
        full_text = f"{subject or ''} {body or ''}".lower()
        
        # Анализируем приоритет
        priority, priority_score = self._analyze_priority(full_text)
        
        # Анализируем категорию
        category, category_confidence = self._analyze_category(full_text)
        
        # Анализируем тональность
        sentiment, sentiment_score = self._analyze_sentiment(full_text)
        
        # Извлекаем сущности
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
    
    def _analyze_priority(self, text: str) -> tuple[str, float]:
        """
        Определяет приоритет письма
        
        Returns:
            Tuple (priority, score)
        """
        high_count = sum(1 for kw in self.priority_keywords['high'] if kw in text)
        medium_count = sum(1 for kw in self.priority_keywords['medium'] if kw in text)
        
        if high_count > 0:
            score = min(0.7 + (high_count * 0.1), 1.0)
            return 'high', score
        elif medium_count > 0:
            score = min(0.4 + (medium_count * 0.1), 0.7)
            return 'medium', score
        else:
            return 'low', 0.3
    
    def _analyze_category(self, text: str) -> tuple[str, float]:
        """
        Определяет категорию письма
        
        Returns:
            Tuple (category, confidence)
        """
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                category_scores[category] = score
        
        if not category_scores:
            return 'General', 0.5
        
        # Находим категорию с максимальным скором
        best_category = max(category_scores, key=category_scores.get)
        max_score = category_scores[best_category]
        
        # Нормализуем confidence (0.5 - 1.0)
        confidence = min(0.5 + (max_score * 0.15), 1.0)
        
        return best_category, confidence
    
    def _analyze_sentiment(self, text: str) -> tuple[str, float]:
        """
        Определяет тональность письма
        
        Returns:
            Tuple (sentiment, score)
        """
        positive_count = sum(1 for kw in self.sentiment_keywords['positive'] if kw in text)
        negative_count = sum(1 for kw in self.sentiment_keywords['negative'] if kw in text)
        
        # Вычисляем баланс
        total = positive_count + negative_count
        
        if total == 0:
            return 'neutral', 0.5
        
        if positive_count > negative_count:
            score = min(0.5 + (positive_count * 0.1), 1.0)
            return 'positive', score
        elif negative_count > positive_count:
            score = max(0.5 - (negative_count * 0.1), 0.0)
            return 'negative', score
        else:
            return 'neutral', 0.5
    
    def _extract_entities(self, subject: str, body: str) -> Dict[str, List[str]]:
        """
        Извлекает сущности из письма (эмейлы, даты, имена)
        
        Returns:
            Словарь с типами сущностей
        """
        text = f"{subject} {body}"
        
        entities = {
            'emails': [],
            'dates': [],
            'urls': [],
            'persons': []
        }
        
        # Извлекаем email адреса
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        entities['emails'] = list(set(re.findall(email_pattern, text)))
        
        # Извлекаем даты (простые форматы)
        date_patterns = [
            r'\d{4}-\d{2}-\d{2}',  # 2025-10-25
            r'\d{2}\.\d{2}\.\d{4}',  # 25.10.2025
            r'\d{1,2}/\d{1,2}/\d{4}'  # 10/25/2025
        ]
        for pattern in date_patterns:
            entities['dates'].extend(re.findall(pattern, text))
        
        # Извлекаем URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        entities['urls'] = list(set(re.findall(url_pattern, text)))
        
        # Извлекаем имена (капитализированные слова, простая эвристика)
        # Ищем слова с большой буквы, которые идут подряд (имя + фамилия)
        name_pattern = r'\b[A-ZА-ЯЁ][a-zа-яё]+(?:\s+[A-ZА-ЯЁ][a-zа-яё]+)\b'
        potential_names = re.findall(name_pattern, text)
        # Фильтруем частые ложные срабатывания
        stop_words = {'Subject', 'From', 'To', 'Date', 'Best Regards', 'Thank You'}
        entities['persons'] = [name for name in potential_names if name not in stop_words][:5]
        
        # Ограничиваем количество сущностей
        for key in entities:
            entities[key] = entities[key][:10]
        
        return entities
    
    def _extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """
        Извлекает ключевые слова из текста
        
        Returns:
            Словарь с ключевыми словами
        """
        # Удаляем стоп-слова и извлекаем значимые слова
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'been',
            'в', 'и', 'на', 'с', 'по', 'для', 'от', 'к', 'из', 'это', 'быть'
        }
        
        # Разбиваем на слова и фильтруем
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Подсчитываем частоту слов (исключая стоп-слова и короткие)
        word_freq = {}
        for word in words:
            if len(word) > 3 and word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Берем топ-10 наиболее частых слов
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        keywords_list = [word for word, freq in top_keywords]
        
        return {
            'keywords': keywords_list,
            'topics': self._infer_topics(keywords_list)
        }
    
    def _infer_topics(self, keywords: List[str]) -> List[str]:
        """
        Определяет темы на основе ключевых слов
        
        Returns:
            Список тем
        """
        topic_mapping = {
            'development': ['code', 'develop', 'git', 'branch', 'deploy', 'test'],
            'разработка': ['код', 'разработка', 'git', 'ветка', 'деплой', 'тест'],
            'management': ['project', 'meeting', 'deadline', 'plan', 'sprint'],
            'менеджмент': ['проект', 'встреча', 'дедлайн', 'план', 'спринт'],
            'finance': ['invoice', 'payment', 'budget', 'cost', 'price'],
            'финансы': ['счет', 'оплата', 'бюджет', 'стоимость', 'цена']
        }
        
        topics = []
        for topic, topic_keywords in topic_mapping.items():
            if any(kw in keywords for kw in topic_keywords):
                topics.append(topic)
        
        return topics[:3]  # Максимум 3 темы
    
    def batch_analyze(self, emails: List[Dict]) -> List[Dict]:
        """
        Пакетный анализ писем для ускорения обработки
        
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
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Возвращает статистику анализатора
        
        Returns:
            Словарь со статистикой
        """
        return {
            'model_name': self.model_name,
            'version': '0.2.0',
            'type': 'mock-heuristic',
            'categories': list(self.category_keywords.keys()),
            'priority_levels': ['high', 'medium', 'low'],
            'sentiment_types': ['positive', 'neutral', 'negative']
        }


def demo_analysis():
    """Демонстрация работы AI Parser"""
    print("=" * 60)
    print("🧠 SolarMail AI Parser - Demo")
    print("=" * 60)
    
    parser = AIParser()
    
    # Тестовые письма
    test_emails = [
        {
            'subject': 'Срочно: требуется ваше решение по проекту',
            'body': 'Добрый день! Нам необходимо принять решение по дедлайну проекта SolarMail. Прошу срочно ответить.'
        },
        {
            'subject': 'Спасибо за отличную работу!',
            'body': 'Хочу поблагодарить команду за прекрасную работу над проектом. Всё сделано на высшем уровне!'
        },
        {
            'subject': 'Invoice #12345 for October',
            'body': 'Please find attached the invoice for services rendered in October. Payment due by end of month.'
        },
        {
            'subject': 'Newsletter: Weekly Tech Updates',
            'body': 'Check out this week\'s top tech news and updates from the industry. New AI models released!'
        }
    ]
    
    print("\n📧 Анализ тестовых писем:\n")
    
    for i, email in enumerate(test_emails, 1):
        print(f"{i}. Тема: {email['subject']}")
        
        meta = parser.analyze_email(email['subject'], email['body'])
        
        print(f"   🎯 Приоритет: {meta['priority']} (score: {meta['priority_score']:.2f})")
        print(f"   📁 Категория: {meta['category']} (confidence: {meta['category_confidence']:.2f})")
        print(f"   😊 Тональность: {meta['sentiment']} (score: {meta['sentiment_score']:.2f})")
        print(f"   ⏱️  Время обработки: {meta['processing_time_ms']} ms")
        
        # Показываем entities
        entities = json.loads(meta['entities_json'])
        if any(entities.values()):
            print(f"   🔍 Сущности: {', '.join([f'{k}={len(v)}' for k, v in entities.items() if v])}")
        
        # Показываем keywords
        keywords = json.loads(meta['keywords_json'])
        if keywords['keywords']:
            print(f"   🏷️  Ключевые слова: {', '.join(keywords['keywords'][:5])}")
        
        print()
    
    # Статистика парсера
    print("=" * 60)
    stats = parser.get_stats()
    print(f"📊 Статистика парсера:")
    print(f"   Модель: {stats['model_name']}")
    print(f"   Версия: {stats['version']}")
    print(f"   Тип: {stats['type']}")
    print(f"   Категории: {', '.join(stats['categories'])}")
    print("=" * 60)


if __name__ == "__main__":
    demo_analysis()
