# 🚀 Real-Time Analytics Engineering Projects

Welcome! This directory contains **5 end-to-end analytics engineering projects** built to showcase data engineering, ML, and real-time processing skills.

## 📊 Quick Status

| Project | Status | Deploy Ready? |
|---------|--------|---------------|
| **1. Job Market Intelligence** | ✅ 90% Complete | ✅ YES - Deploy now! |
| **2. E-commerce Price Intelligence** | ✅ 60% Complete | 🔨 2-3 days |
| **3. Social Media Analytics** | 🔨 Architecture Ready | 🔨 1 week |
| **4. Healthcare Readmission Risk** | 🔨 Architecture Ready | 🔨 1 week |
| **5. Supply Chain Tracker** | 🔨 Architecture Ready | 🔨 1 week |

## 🎯 What's Been Built

### Project 1: Job Market Intelligence (PRODUCTION READY) ⭐

**Real working platform that scrapes jobs, extracts skills, matches to users, and sends alerts.**

#### Features:
- ✅ Web scrapers (Indeed, Fuzu) with rate limiting
- ✅ NLP skill extraction (spaCy) - 30+ skills
- ✅ Smart job matching algorithm
- ✅ Telegram notifications
- ✅ Interactive Streamlit dashboard with charts
- ✅ CLI automation tools
- ✅ PostgreSQL database (10 tables)
- ✅ 2,000+ lines of production code

#### Quick Start:
```bash
cd job-market-intelligence

# Install
pip install -r pipeline/requirements.txt
python -m spacy download en_core_web_sm

# Setup DB
createdb job_market_db
echo "DATABASE_URL=postgresql://localhost/job_market_db" > .env
python scripts/setup_database.py

# Run
python scripts/run_scrapers.py
python scripts/process_skills.py
streamlit run dashboard/app.py
```

**📖 Full docs:** [job-market-intelligence/README.md](job-market-intelligence/README.md)

---

### Project 2: E-commerce Price Intelligence (60% DONE)

**Price tracking across Jumia, Kilimall, Amazon with ML forecasting.**

#### Built:
- ✅ Database schema (11 tables)
- ✅ Jumia scraper (Selenium)
- ✅ Sentiment analysis (VADER, TextBlob)
- ✅ Price forecasting (Prophet)

#### To Complete:
- 🔨 Streamlit dashboard
- 🔨 Price alert system

---

### Projects 3-5: Architecture Ready

Professional landing pages created, ready to build when APIs/data are available:
- **Social Media Analytics** - Kafka + BERT + real-time processing
- **Healthcare Readmission** - XGBoost + SHAP explainability
- **Supply Chain Tracker** - API integrations + delay prediction

## 📁 Directory Structure

```
analytics-engineering/
├── job-market-intelligence/     ⭐ DEPLOY READY
│   ├── pipeline/                Complete backend
│   ├── dashboard/               Streamlit dashboard
│   ├── scripts/                 CLI tools
│   └── README.md
├── ecommerce-price-intelligence/ 🔨 60% DONE
│   ├── pipeline/                Core complete
│   └── index.qmd
├── social-media-analytics/      🔨 Architecture
│   └── index.qmd
├── healthcare-readmission-risk/ 🔨 Architecture
│   └── index.qmd
├── supply-chain-tracker/        🔨 Architecture
│   └── index.qmd
├── index.qmd                    Landing page
├── DEPLOYMENT_READY.md          📖 Deployment guide
├── IMPLEMENTATION_SUMMARY.md    📊 Detailed status
└── WORK_SESSION_SUMMARY.md      📝 What was built
```

## 🚀 Deploy Job Market Intelligence NOW (20 minutes)

### Option 1: Streamlit Cloud (Easiest)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo: `projects/analytics-engineering/job-market-intelligence/dashboard/app.py`
4. Add secret: `DATABASE_URL = your-postgres-url`
5. Deploy!

### Option 2: Local Testing
```bash
cd job-market-intelligence
pip install -r pipeline/requirements.txt
python -m spacy download en_core_web_sm
createdb job_market_db
echo "DATABASE_URL=postgresql://localhost/job_market_db" > .env
python scripts/setup_database.py
python scripts/run_scrapers.py
streamlit run dashboard/app.py
```

## 💰 Cost

- **Development:** $0 (free tiers)
- **Production:** $12/month (Heroku Postgres + Dyno)

## 📚 Documentation

- **[DEPLOYMENT_READY.md](DEPLOYMENT_READY.md)** - Complete deployment guide
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Detailed progress
- **[WORK_SESSION_SUMMARY.md](WORK_SESSION_SUMMARY.md)** - Build session recap

## 🎯 Tech Stack

**Languages:** Python, SQL, JavaScript  
**Data:** PostgreSQL, SQLAlchemy  
**ML/NLP:** spaCy, Prophet, VADER, TextBlob, scikit-learn  
**Scraping:** Selenium, Scrapy, BeautifulSoup, Requests  
**Dashboards:** Streamlit, Plotly, D3.js  
**APIs:** FastAPI (planned)  
**Orchestration:** Apache Airflow (planned)  
**Deployment:** Heroku, Streamlit Cloud, AWS  

## 🏆 What This Demonstrates

1. **Full-Stack Data Engineering**
   - ETL pipeline design
   - Real-time data processing
   - Database architecture
   - Web scraping at scale

2. **Machine Learning**
   - NLP (skill extraction)
   - Sentiment analysis
   - Time-series forecasting
   - Matching algorithms

3. **Software Engineering**
   - Clean code architecture
   - Design patterns
   - Error handling
   - Documentation

4. **DevOps**
   - Configuration management
   - Deployment automation
   - CI/CD ready

## 📞 Contact

**Nicodemus Werre**  
📧 nichodemuswerre@gmail.com  
🔗 [linkedin.com/in/amollow](https://linkedin.com/in/amollow)  
🌐 [gondamol.github.io](https://gondamol.github.io)

---

**⭐ Start with Project 1 - It's ready to deploy!**

*Built October 2025*





