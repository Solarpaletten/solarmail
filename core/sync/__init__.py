"""
SolarMail - Sync Package
Модуль синхронизации почты через IMAP
"""

from .solar_sync import SolarSync
from .db_manager import DatabaseManager

__version__ = "0.1.0"
__all__ = ["SolarSync", "DatabaseManager"]
