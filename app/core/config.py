import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.dev' if os.getenv('ENVIRONMENT') != 'production' else '.env.prod')

class Settings:
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./database.db')
    
    # JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    ALGORITHM = os.getenv('ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    
    # Email
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASS = os.getenv('EMAIL_PASS', '')
    EMAIL_FROM = os.getenv('EMAIL_FROM', '')
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', '5'))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', '60'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')

settings = Settings()
