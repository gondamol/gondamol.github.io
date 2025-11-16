"""
Configuration for E-commerce Price Intelligence
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://localhost:5432/ecommerce_price_db'
)

# Scraping Configuration
SCRAPING_CONFIG = {
    'user_agent': 'PriceIntelligence/1.0 (Educational Project; contact@example.com)',
    'rate_limit_delay': 3,  # seconds between requests
    'max_concurrent_requests': 2,
    'timeout': 30,
    'retry_times': 3,
}

# E-commerce Platforms
ECOMMERCE_PLATFORMS = {
    'jumia': {
        'enabled': True,
        'name': 'Jumia Kenya',
        'base_url': 'https://www.jumia.co.ke',
        'categories': ['electronics', 'phones', 'laptops', 'fashion'],
        'use_selenium': True,  # For dynamic content
    },
    'kilimall': {
        'enabled': True,
        'name': 'Kilimall Kenya',
        'base_url': 'https://www.kilimall.co.ke',
        'categories': ['electronics', 'phones', 'appliances'],
        'use_selenium': True,
    },
    'amazon': {
        'enabled': False,  # Requires API or careful scraping
        'name': 'Amazon',
        'base_url': 'https://www.amazon.com',
        'categories': ['electronics'],
        'use_api': True,  # Use Product Advertising API if available
    },
}

# Product Categories to Track
PRODUCT_CATEGORIES = [
    'Electronics',
    'Mobile Phones',
    'Laptops',
    'TVs',
    'Home Appliances',
    'Fashion',
    'Books',
]

# Price Alert Thresholds
ALERT_CONFIG = {
    'price_drop_threshold': 10,  # percentage
    'significant_drop': 20,  # percentage
    'check_frequency': 'hourly',  # hourly, daily
}

# Sentiment Analysis
SENTIMENT_CONFIG = {
    'min_reviews': 3,  # Minimum reviews for sentiment analysis
    'enable_vader': True,
    'enable_textblob': True,
}

# Forecasting Configuration
FORECAST_CONFIG = {
    'prophet_enabled': True,
    'forecast_days': 30,
    'confidence_interval': 0.95,
}

# Notification Configuration
TELEGRAM_CONFIG = {
    'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'enabled': bool(os.getenv('TELEGRAM_BOT_TOKEN')),
}

TWILIO_CONFIG = {
    'account_sid': os.getenv('TWILIO_ACCOUNT_SID', ''),
    'auth_token': os.getenv('TWILIO_AUTH_TOKEN', ''),
    'from_number': os.getenv('TWILIO_FROM_NUMBER', ''),
    'enabled': bool(os.getenv('TWILIO_ACCOUNT_SID')),
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'port': int(os.getenv('DASHBOARD_PORT', '8502')),
    'host': os.getenv('DASHBOARD_HOST', '0.0.0.0'),
    'title': 'E-commerce Price Intelligence',
}






