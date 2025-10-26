"""
SolarMail - Configuration
Настройки IMAP подключения и параметры синхронизации
"""

# ==========================================
# IMAP Configuration
# ==========================================

# Gmail IMAP Settings
IMAP_HOST = "imap.gmail.com"

# Ваши учетные данные
# ВАЖНО: Для Gmail используйте App Password, а не основной пароль
# Как создать App Password: https://support.google.com/accounts/answer/185833
EMAIL = "example@gmail.com"
PASSWORD = "app-password"

# ==========================================
# Другие популярные IMAP настройки
# ==========================================

# Outlook/Hotmail
# IMAP_HOST = "outlook.office365.com"

# Yahoo
# IMAP_HOST = "imap.mail.yahoo.com"

# Custom IMAP Server
# IMAP_HOST = "mail.example.com"

# ==========================================
# Sync Settings
# ==========================================

# Количество дней для синхронизации (по умолчанию в коде: 3)
SYNC_DAYS = 3

# Папка для синхронизации (по умолчанию: INBOX)
SYNC_FOLDER = "INBOX"
