"""
Configuration for Job Market Intelligence Platform
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'job_market_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
}

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"
)

# Scraping Configuration
SCRAPING_CONFIG = {
    'user_agent': 'JobMarketIntelligence/1.0 (Educational Project; contact@example.com)',
    'rate_limit_delay': 2,  # seconds between requests
    'max_concurrent_requests': 2,
    'timeout': 30,
    'retry_times': 3,
}

# Job Boards to Scrape
JOB_BOARDS = {
    'linkedin': {
        'enabled': True,
        'keywords': ['data analyst', 'data scientist', 'data engineer'],
        'locations': ['Kenya', 'Remote', 'East Africa'],
        'api_available': False,
    },
    'indeed': {
        'enabled': True,
        'keywords': ['data analyst', 'data scientist', 'business intelligence'],
        'locations': ['Kenya', 'Remote'],
        'api_available': True,  # Indeed has Publisher API
    },
    'glassdoor': {
        'enabled': True,
        'keywords': ['data analyst', 'data engineer'],
        'locations': ['Kenya', 'Nairobi'],
        'api_available': False,
    },
    'fuzu': {
        'enabled': True,
        'keywords': ['data', 'analytics', 'business intelligence'],
        'locations': ['Kenya'],
        'api_available': False,
    },
    'brightermonday': {
        'enabled': True,
        'keywords': ['data analyst', 'data scientist'],
        'locations': ['Kenya', 'Uganda', 'Tanzania'],
        'api_available': False,
    },
}

# NLP Configuration
NLP_CONFIG = {
    'spacy_model': 'en_core_web_sm',
    'skill_extraction_enabled': True,
    'salary_extraction_enabled': True,
}

# Skills to Extract (common data analytics skills)
TARGET_SKILLS = [
    # Programming Languages
    'Python', 'R', 'SQL', 'JavaScript', 'Java', 'Scala',
    
    # Data Tools
    'Excel', 'Power BI', 'Tableau', 'Looker', 'Qlik',
    
    # Databases
    'PostgreSQL', 'MySQL', 'MongoDB', 'Cassandra', 'Redis',
    
    # Big Data
    'Spark', 'Hadoop', 'Kafka', 'Airflow', 'Databricks',
    
    # Cloud
    'AWS', 'Azure', 'GCP', 'Snowflake', 'Redshift',
    
    # ML/AI
    'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
    'TensorFlow', 'PyTorch', 'scikit-learn', 'XGBoost',
    
    # Statistics
    'Statistics', 'A/B Testing', 'Hypothesis Testing', 'Regression',
    
    # Other
    'Git', 'Docker', 'Kubernetes', 'API', 'ETL', 'Data Warehousing',
    'Data Modeling', 'Dashboard Design', 'Data Visualization',
]

# Notification Configuration
TELEGRAM_CONFIG = {
    'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
    'enabled': bool(os.getenv('TELEGRAM_BOT_TOKEN')),
}

EMAIL_CONFIG = {
    'sendgrid_api_key': os.getenv('SENDGRID_API_KEY', ''),
    'from_email': os.getenv('FROM_EMAIL', 'noreply@jobmarket.ai'),
    'enabled': bool(os.getenv('SENDGRID_API_KEY')),
}

# Airflow Configuration
AIRFLOW_CONFIG = {
    'schedule_interval': '@hourly',  # Run every hour
    'catchup': False,
}

# Dashboard Configuration
DASHBOARD_CONFIG = {
    'port': int(os.getenv('DASHBOARD_PORT', '8501')),
    'host': os.getenv('DASHBOARD_HOST', '0.0.0.0'),
    'title': 'Job Market Intelligence Dashboard',
}


