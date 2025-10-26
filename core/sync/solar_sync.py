"""
SolarMail - IMAP Sync Core
Ядро синхронизации почты с IMAP серверами
"""

from imap_tools import MailBox, AND
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import sys
import os

# Добавляем путь к модулям проекта
sys.path.append(os.path.dirname(__file__))

from core.sync.db_manager import DatabaseManager
from core.sync.ai_parser import AIParser
import config


class SolarSync:
    """Основной класс синхронизации писем через IMAP"""
    
    def __init__(self, enable_ai: bool = False):
        """
        Инициализация SolarSync
        
        Args:
            enable_ai: Включить AI-анализ писем (по умолчанию выключен)
        """
        self.db = DatabaseManager()
        self.imap_host = config.IMAP_HOST
        self.email = config.EMAIL
        self.password = config.PASSWORD
        self.sync_days = 3  # Синхронизация за последние 3 дня
        self.enable_ai = enable_ai
        
        # Инициализируем AI parser если включен
        if self.enable_ai:
            self.ai_parser = AIParser()
        
        # Инициализируем sync_status если его нет
        self.db.init_sync_status(self.email, self.sync_days)
        
    def connect(self) -> MailBox:
        """
        Подключается к IMAP серверу
        
        Returns:
            Объект MailBox для работы с почтой
        """
        try:
            mailbox = MailBox(self.imap_host)
            mailbox.login(self.email, self.password)
            print(f"✅ Подключено к {self.imap_host} как {self.email}")
            return mailbox
        except Exception as e:
            print(f"❌ Ошибка подключения к IMAP: {e}")
            raise
    
    def fetch_emails(self, mailbox: MailBox, days: int = 3) -> List[Dict]:
        """
        Получает письма за последние N дней
        
        Args:
            mailbox: Объект MailBox
            days: Количество дней для синхронизации
        
        Returns:
            Список словарей с данными писем
        """
        # Вычисляем дату начала синхронизации
        since_date = datetime.now() - timedelta(days=days)
        
        emails_data = []
        
        try:
            # Выбираем папку INBOX
            mailbox.folder.set('INBOX')
            
            # Получаем письма за последние N дней
            messages = mailbox.fetch(
                criteria=AND(date_gte=since_date.date()),
                mark_seen=False  # Не помечаем письма как прочитанные
            )
            
            print(f"📥 Загрузка писем с {since_date.strftime('%Y-%m-%d')}...")
            
            for msg in messages:
                # Извлекаем первые 200 символов текста письма
                body_text = msg.text or msg.html or ""
                body_preview = body_text[:200].replace('\n', ' ').strip()
                
                email_data = {
                    'uid': msg.uid,
                    'sender': msg.from_ or "Unknown",
                    'subject': msg.subject or "(No Subject)",
                    'date': msg.date.isoformat() if msg.date else datetime.now().isoformat(),
                    'body_preview': body_preview
                }
                
                emails_data.append(email_data)
            
            print(f"✅ Получено {len(emails_data)} писем")
            
        except Exception as e:
            print(f"❌ Ошибка при получении писем: {e}")
            raise
        
        return emails_data
    
    def sync_to_database(self, emails: List[Dict]) -> Dict[str, int]:
        """
        Синхронизирует письма в базу данных
        
        Args:
            emails: Список словарей с данными писем
        
        Returns:
            Словарь со статистикой синхронизации
        """
        stats = {
            'new': 0,
            'skipped': 0,
            'total': len(emails)
        }
        
        for email in emails:
            if self.db.insert_email(email):
                stats['new'] += 1
            else:
                stats['skipped'] += 1
        
        return stats
    
    # ==================== Sprint 0.2: Smart Cache Methods ====================
    
    def get_last_sync_date(self) -> Optional[str]:
        """
        Получает дату последней синхронизации для текущего аккаунта
        
        Returns:
            ISO дата последней синхронизации или None
        """
        return self.db.get_last_sync_date(self.email)
    
    def fetch_emails_smart(self, mailbox: MailBox, since_date: Optional[datetime] = None) -> List[Dict]:
        """
        Получает письма с учетом smart cache (только новые)
        
        Args:
            mailbox: Объект MailBox
            since_date: Дата начала синхронизации (если None, используется last_sync_date или sync_days)
        
        Returns:
            Список словарей с данными писем
        """
        # Если дата не указана, пытаемся получить last_sync_date
        if since_date is None:
            last_sync = self.get_last_sync_date()
            
            if last_sync:
                # Парсим ISO дату и добавляем 1 секунду чтобы не загружать уже синхронизированное письмо
                since_date = datetime.fromisoformat(last_sync.replace('Z', '+00:00'))
                since_date = since_date + timedelta(seconds=1)
                print(f"🔄 Smart Cache: синхронизация с {since_date.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                # Первая синхронизация - берем за последние N дней
                since_date = datetime.now() - timedelta(days=self.sync_days)
                print(f"📥 Первая синхронизация: последние {self.sync_days} дней")
        
        emails_data = []
        
        try:
            # Выбираем папку INBOX
            mailbox.folder.set('INBOX')
            
            # Получаем письма новее указанной даты
            messages = mailbox.fetch(
                criteria=AND(date_gte=since_date.date()),
                mark_seen=False
            )
            
            for msg in messages:
                # Извлекаем первые 200 символов текста письма
                body_text = msg.text or msg.html or ""
                body_preview = body_text[:200].replace('\n', ' ').strip()
                
                email_data = {
                    'uid': msg.uid,
                    'sender': msg.from_ or "Unknown",
                    'subject': msg.subject or "(No Subject)",
                    'date': msg.date.isoformat() if msg.date else datetime.now().isoformat(),
                    'body_preview': body_preview
                }
                
                emails_data.append(email_data)
            
            print(f"✅ Получено {len(emails_data)} писем")
            
        except Exception as e:
            print(f"❌ Ошибка при получении писем: {e}")
            raise
        
        return emails_data
    
    def analyze_emails_with_ai(self, emails: List[Dict]) -> int:
        """
        Анализирует письма с помощью AI и сохраняет метаданные
        
        Args:
            emails: Список писем из базы данных (должны иметь поле 'id')
        
        Returns:
            Количество проанализированных писем
        """
        if not self.enable_ai or not emails:
            return 0
        
        print("\n🧠 AI-анализ писем...")
        analyzed_count = 0
        
        for email in emails:
            # Проверяем, есть ли уже метаданные
            existing_meta = self.db.get_email_meta(email['id'])
            if existing_meta:
                continue  # Пропускаем уже проанализированные
            
            # Анализируем письмо
            meta_data = self.ai_parser.analyze_email(
                email.get('subject', ''),
                email.get('body_preview', '')
            )
            
            # Сохраняем метаданные
            if self.db.insert_email_meta(email['id'], meta_data):
                analyzed_count += 1
        
        print(f"✅ Проанализировано: {analyzed_count} писем")
        return analyzed_count
    
    def smart_sync(self):
        """
        Запускает умную синхронизацию с использованием cache и AI
        Sprint 0.2 feature
        """
        print("🚀 SolarSync - Smart Sync запущен...")
        print(f"📧 Email: {self.email}")
        if self.enable_ai:
            print(f"🧠 AI-анализ: включен")
        print("-" * 50)
        
        sync_start_time = datetime.now()
        
        try:
            # Подключаемся к IMAP
            mailbox = self.connect()
            
            # Получаем письма с учетом smart cache
            emails = self.fetch_emails_smart(mailbox)
            
            # Закрываем соединение
            mailbox.logout()
            print("🔌 Отключено от IMAP сервера")
            
            # Синхронизируем в базу данных
            print("\n💾 Синхронизация с локальным кэшем...")
            stats = self.sync_to_database(emails)
            
            # Если были добавлены новые письма и включен AI
            if stats['new'] > 0 and self.enable_ai:
                # Получаем только что добавленные письма для анализа
                recent_emails = self.db.get_all_emails(limit=stats['new'])
                self.analyze_emails_with_ai(recent_emails)
            
            # Обновляем sync_status
            last_sync_date = sync_start_time.isoformat()
            self.db.update_sync_status(
                self.email,
                last_sync_date,
                stats,
                success=True
            )
            
            # Выводим статистику
            print("-" * 50)
            print(f"📊 Статистика синхронизации:")
            print(f"   • Всего обработано: {stats['total']}")
            print(f"   • Новых писем: {stats['new']}")
            print(f"   • Пропущено (дубли): {stats['skipped']}")
            print(f"   • Всего в кэше: {self.db.get_emails_count()}")
            
            # Получаем общий статус синхронизации
            sync_status = self.db.get_sync_status(self.email)
            if sync_status:
                print(f"   • Всего синхронизировано: {sync_status['total_emails_synced']}")
            
            print("-" * 50)
            print("✅ Smart Sync завершен успешно!")
            
        except Exception as e:
            print(f"\n❌ Smart Sync прерван с ошибкой: {e}")
            
            # Записываем ошибку в sync_status
            self.db.update_sync_status(
                self.email,
                datetime.now().isoformat(),
                {'total': 0, 'new': 0, 'skipped': 0},
                success=False,
                error_message=str(e)
            )
            raise
    
    def run(self):
        """
        Запускает полный цикл синхронизации
        """
        print("🚀 SolarSync - запуск синхронизации...")
        print(f"📧 Email: {self.email}")
        print(f"🔄 Период синхронизации: последние {self.sync_days} дней")
        print("-" * 50)
        
        try:
            # Подключаемся к IMAP
            mailbox = self.connect()
            
            # Получаем письма
            emails = self.fetch_emails(mailbox, self.sync_days)
            
            # Закрываем соединение
            mailbox.logout()
            print("🔌 Отключено от IMAP сервера")
            
            # Синхронизируем в базу данных
            print("\n💾 Синхронизация с локальным кэшем...")
            stats = self.sync_to_database(emails)
            
            # Выводим статистику
            print("-" * 50)
            print(f"📊 Статистика синхронизации:")
            print(f"   • Всего обработано: {stats['total']}")
            print(f"   • Новых писем: {stats['new']}")
            print(f"   • Пропущено (дубли): {stats['skipped']}")
            print(f"   • Всего в кэше: {self.db.get_emails_count()}")
            print("-" * 50)
            print("✅ Синхронизация завершена успешно!")
            
        except Exception as e:
            print(f"\n❌ Синхронизация прервана с ошибкой: {e}")
            raise
    
    def get_cached_emails(self, limit: int = 10) -> List[Dict]:
        """
        Получает письма из локального кэша
        
        Args:
            limit: Количество писем для получения
        
        Returns:
            Список писем из базы данных
        """
        return self.db.get_all_emails(limit)


def main():
    """Точка входа для тестирования"""
    sync = SolarSync()
    sync.run()


if __name__ == "__main__":
    main()
