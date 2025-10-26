"""
SolarMail - Database Manager
Управление локальным кэш-хранилищем SQLite для синхронизации писем
"""

import sqlite3
import json
from typing import List, Dict, Optional, Any
from datetime import datetime


class DatabaseManager:
    """Менеджер базы данных для хранения синхронизированных писем"""
    
    def __init__(self, db_path: str = "solar_cache.db"):
        """
        Инициализация менеджера БД
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Создает подключение к БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
        return conn
    
    def init_database(self):
        """Инициализирует базу данных и создает таблицы"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Создаем таблицу emails
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uid TEXT UNIQUE NOT NULL,
                sender TEXT NOT NULL,
                subject TEXT,
                date TEXT NOT NULL,
                body_preview TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создаем индекс на uid для быстрого поиска
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uid ON emails(uid)
        """)
        
        # Создаем индекс на date для сортировки
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_date ON emails(date)
        """)
        
        # ==================== Sprint 0.2: AI & Smart Cache ====================
        
        # Создаем таблицу email_meta для AI-метаданных
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS email_meta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_id INTEGER NOT NULL,
                
                sentiment TEXT,
                sentiment_score REAL,
                priority TEXT,
                priority_score REAL,
                category TEXT,
                category_confidence REAL,
                
                entities_json TEXT,
                keywords_json TEXT,
                
                analyzed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                ai_model TEXT,
                processing_time_ms INTEGER,
                
                FOREIGN KEY (email_id) REFERENCES emails(id) ON DELETE CASCADE
            )
        """)
        
        # Индексы для email_meta
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_email_meta_email_id ON email_meta(email_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_email_meta_category ON email_meta(category)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_email_meta_priority ON email_meta(priority)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_email_meta_sentiment ON email_meta(sentiment)
        """)
        
        # Создаем таблицу sync_status для умного кэша
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_email TEXT UNIQUE NOT NULL,
                
                last_sync_date TEXT,
                last_sync_success INTEGER DEFAULT 0,
                last_error_message TEXT,
                
                total_emails_synced INTEGER DEFAULT 0,
                last_batch_count INTEGER DEFAULT 0,
                
                sync_enabled INTEGER DEFAULT 1,
                sync_days INTEGER DEFAULT 3,
                
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Индексы для sync_status
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sync_status_email ON sync_status(account_email)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sync_status_last_sync ON sync_status(last_sync_date)
        """)
        
        conn.commit()
        conn.close()
        print(f"✅ База данных инициализирована: {self.db_path}")
        print(f"   📊 Таблицы: emails, email_meta, sync_status")
    
    def insert_email(self, data: Dict) -> bool:
        """
        Вставляет письмо в базу данных
        
        Args:
            data: Словарь с данными письма (uid, sender, subject, date, body_preview)
        
        Returns:
            True если письмо добавлено, False если уже существует
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO emails (uid, sender, subject, date, body_preview)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data.get('uid'),
                data.get('sender'),
                data.get('subject'),
                data.get('date'),
                data.get('body_preview')
            ))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Письмо с таким UID уже существует
            conn.close()
            return False
        except Exception as e:
            print(f"❌ Ошибка при вставке письма: {e}")
            conn.close()
            return False
    
    def get_all_emails(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Получает все письма из базы данных
        
        Args:
            limit: Ограничение количества писем (опционально)
        
        Returns:
            Список словарей с данными писем
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM emails ORDER BY date DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        # Преобразуем Row объекты в словари
        emails = [dict(row) for row in rows]
        return emails
    
    def email_exists(self, uid: str) -> bool:
        """
        Проверяет существование письма по UID
        
        Args:
            uid: UID письма
        
        Returns:
            True если письмо существует, иначе False
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM emails WHERE uid = ?", (uid,))
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def get_emails_count(self) -> int:
        """Возвращает общее количество писем в базе"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM emails")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def clear_database(self):
        """Очищает все письма из базы данных"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM emails")
        conn.commit()
        conn.close()
        print("🗑️ База данных очищена")
    
    # ==================== Sprint 0.2: AI Meta Methods ====================
    
    def insert_email_meta(self, email_id: int, meta_data: Dict[str, Any]) -> bool:
        """
        Вставляет AI-метаданные для письма
        
        Args:
            email_id: ID письма в таблице emails
            meta_data: Словарь с AI-метаданными
        
        Returns:
            True если метаданные добавлены успешно
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO email_meta (
                    email_id, sentiment, sentiment_score, priority, priority_score,
                    category, category_confidence, entities_json, keywords_json,
                    ai_model, processing_time_ms
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                email_id,
                meta_data.get('sentiment'),
                meta_data.get('sentiment_score'),
                meta_data.get('priority'),
                meta_data.get('priority_score'),
                meta_data.get('category'),
                meta_data.get('category_confidence'),
                meta_data.get('entities_json'),
                meta_data.get('keywords_json'),
                meta_data.get('ai_model'),
                meta_data.get('processing_time_ms')
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Ошибка при вставке метаданных: {e}")
            conn.close()
            return False
    
    def get_email_meta(self, email_id: int) -> Optional[Dict]:
        """
        Получает AI-метаданные для письма
        
        Args:
            email_id: ID письма
        
        Returns:
            Словарь с метаданными или None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM email_meta WHERE email_id = ?", (email_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_emails_with_meta(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Получает письма вместе с их AI-метаданными
        
        Args:
            limit: Ограничение количества писем
        
        Returns:
            Список писем с метаданными
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                e.*,
                m.sentiment, m.sentiment_score,
                m.priority, m.priority_score,
                m.category, m.category_confidence,
                m.entities_json, m.keywords_json,
                m.ai_model, m.processing_time_ms
            FROM emails e
            LEFT JOIN email_meta m ON e.id = m.email_id
            ORDER BY e.date DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_emails_by_category(self, category: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Получает письма по категории
        
        Args:
            category: Категория (People/Work/Docs/Tasks/News/Spam)
            limit: Ограничение количества
        
        Returns:
            Список писем данной категории
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT e.*, m.*
            FROM emails e
            INNER JOIN email_meta m ON e.id = m.email_id
            WHERE m.category = ?
            ORDER BY e.date DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (category,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_emails_by_priority(self, priority: str, limit: Optional[int] = None) -> List[Dict]:
        """
        Получает письма по приоритету
        
        Args:
            priority: Приоритет (high/medium/low)
            limit: Ограничение количества
        
        Returns:
            Список писем данного приоритета
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT e.*, m.*
            FROM emails e
            INNER JOIN email_meta m ON e.id = m.email_id
            WHERE m.priority = ?
            ORDER BY m.priority_score DESC, e.date DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (priority,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # ==================== Sprint 0.2: Sync Status Methods ====================
    
    def init_sync_status(self, account_email: str, sync_days: int = 3) -> bool:
        """
        Инициализирует запись о синхронизации для аккаунта
        
        Args:
            account_email: Email аккаунта
            sync_days: Период синхронизации в днях
        
        Returns:
            True если запись создана
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO sync_status (account_email, sync_days)
                VALUES (?, ?)
            """, (account_email, sync_days))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Запись уже существует
            conn.close()
            return False
    
    def get_last_sync_date(self, account_email: str) -> Optional[str]:
        """
        Получает дату последней синхронизации
        
        Args:
            account_email: Email аккаунта
        
        Returns:
            ISO дата последней синхронизации или None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT last_sync_date FROM sync_status WHERE account_email = ?",
            (account_email,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            return row[0]
        return None
    
    def update_sync_status(
        self,
        account_email: str,
        last_sync_date: str,
        stats: Dict[str, int],
        success: bool = True,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Обновляет статус синхронизации
        
        Args:
            account_email: Email аккаунта
            last_sync_date: ISO дата синхронизации
            stats: Статистика синхронизации (total, new, skipped)
            success: Успешность синхронизации
            error_message: Сообщение об ошибке (если была)
        
        Returns:
            True если обновлено успешно
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Проверяем существование записи
            cursor.execute(
                "SELECT total_emails_synced FROM sync_status WHERE account_email = ?",
                (account_email,)
            )
            row = cursor.fetchone()
            
            if row:
                # Обновляем существующую запись
                total_synced = row[0] + stats.get('new', 0)
                
                cursor.execute("""
                    UPDATE sync_status
                    SET last_sync_date = ?,
                        last_sync_success = ?,
                        last_error_message = ?,
                        total_emails_synced = ?,
                        last_batch_count = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE account_email = ?
                """, (
                    last_sync_date,
                    1 if success else 0,
                    error_message,
                    total_synced,
                    stats.get('total', 0),
                    account_email
                ))
            else:
                # Создаем новую запись
                cursor.execute("""
                    INSERT INTO sync_status (
                        account_email, last_sync_date, last_sync_success,
                        last_error_message, total_emails_synced, last_batch_count
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    account_email,
                    last_sync_date,
                    1 if success else 0,
                    error_message,
                    stats.get('new', 0),
                    stats.get('total', 0)
                ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Ошибка при обновлении sync_status: {e}")
            conn.close()
            return False
    
    def get_sync_status(self, account_email: str) -> Optional[Dict]:
        """
        Получает полную информацию о статусе синхронизации
        
        Args:
            account_email: Email аккаунта
        
        Returns:
            Словарь со статусом или None
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM sync_status WHERE account_email = ?",
            (account_email,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_all_sync_statuses(self) -> List[Dict]:
        """
        Получает статусы всех синхронизированных аккаунтов
        
        Returns:
            Список статусов
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM sync_status ORDER BY updated_at DESC")
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
