# 🎯 Job Market Intelligence Platform

Automated job market intelligence platform that scrapes job postings from multiple boards, extracts insights using NLP, and provides intelligent alerts.

## 🚀 Features

- **Multi-Source Scraping**: Indeed, Fuzu, Glassdoor, LinkedIn, BrighterMonday
- **NLP Skill Extraction**: Automatic skill identification from job descriptions
- **Smart Matching**: Intelligent job-user matching algorithm
- **Real-time Alerts**: Telegram/Email notifications for relevant jobs
- **Interactive Dashboard**: Streamlit dashboard with market insights
- **RESTful API**: (Coming soon) Programmatic access to data

## 🏗️ Architecture

```
job-market-intelligence/
├── pipeline/              # Data pipeline
│   ├── scrapers/         # Web scrapers for each source
│   ├── nlp/              # Skill extraction using spaCy
│   ├── matching/         # Job-user matching algorithm
│   ├── notifications/    # Telegram/Email alerts
│   └── database/         # PostgreSQL models & connection
├── dashboard/            # Streamlit dashboard
├── scripts/              # CLI tools
└── tests/                # Unit tests
```

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL 14+
- (Optional) Telegram Bot Token
- (Optional) SendGrid API Key

## 🛠️ Installation

### 1. Clone & Setup

```bash
cd job-market-intelligence
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r pipeline/requirements.txt
```

### 2. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Setup Database

```bash
# Create PostgreSQL database
createdb job_market_db

# Run migrations
python scripts/setup_database.py
```

## 🚀 Usage

### Run Scrapers

```bash
# Run all enabled scrapers
python scripts/run_scrapers.py

# Run specific scraper
python scripts/run_scrapers.py --source indeed
```

### Extract Skills

```bash
# Process all jobs
python scripts/process_skills.py

# Process limited number
python scripts/process_skills.py --limit 100
```

### Run Job Matching

```bash
# Match jobs to users
python scripts/run_matching.py --min-score 70
```

### Send Notifications

```bash
# Send daily digests
python scripts/send_notifications.py --digest
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard will be available at http://localhost:8501

## 🗄️ Database Schema

Key tables:
- `jobs`: Job postings
- `companies`: Company information
- `skills`: Skills master table
- `job_skills`: Job-skill relationships
- `user_profiles`: User preferences
- `job_alerts`: Match alerts
- `scraping_logs`: Scraper run logs

## 🔄 Automation

### Using Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Run scrapers every hour
0 * * * * cd /path/to/project && /path/to/venv/bin/python scripts/run_scrapers.py

# Extract skills every 2 hours
0 */2 * * * cd /path/to/project && /path/to/venv/bin/python scripts/process_skills.py

# Run matching every 3 hours
0 */3 * * * cd /path/to/project && /path/to/venv/bin/python scripts/run_matching.py

# Send digests daily at 8 AM
0 8 * * * cd /path/to/project && /path/to/venv/bin/python scripts/send_notifications.py --digest
```

### Using Apache Airflow (Recommended for Production)

See `airflow_dags/` directory for DAG examples.

## 🐳 Docker Deployment

```bash
# Build image
docker build -t job-market-intelligence .

# Run with Docker Compose
docker-compose up -d
```

## 📊 Dashboard Features

- **Real-time Metrics**: Active jobs, sources, salaries
- **Interactive Charts**: Top locations, companies, skills
- **Skill Analysis**: Most in-demand skills by category
- **Job Browser**: Filter and search recent postings
- **Market Trends**: Salary trends, hiring patterns

## 🔒 Legal & Ethical Considerations

- ✅ Respects robots.txt
- ✅ Rate limiting (2s between requests)
- ✅ Clear user-agent identification
- ✅ Uses official APIs where available
- ✅ No PII storage beyond user profiles
- ✅ Complies with platform ToS

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional scrapers (Remote.co, Wellfound, etc.)
- Machine learning for salary prediction
- Browser extension for easy job tracking
- Public API with authentication

## 📝 License

MIT License - See LICENSE file

## 👤 Author

**Nicodemus Werre**
- Portfolio: [gondamol.github.io](https://gondamol.github.io)
- LinkedIn: [linkedin.com/in/amollow](https://linkedin.com/in/amollow)
- Email: nichodemuswerre@gmail.com

---

**Note**: This is an educational project demonstrating data engineering and analytics skills. Always ensure compliance with websites' Terms of Service when scraping.






