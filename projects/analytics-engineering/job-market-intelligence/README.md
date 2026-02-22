# 🎯 Job Market Intelligence Dashboard

> **Real-time Data Analytics Job Market Insights**

A comprehensive dashboard that scrapes, analyzes, and visualizes job postings from multiple sources to provide actionable insights for data professionals.

![Dashboard Preview](assets/dashboard-preview.png)

## 🌐 Live Dashboard

**[View Live Dashboard →](https://data-analytics-jobs.streamlit.app)**

## 📊 Data Sources

| Source | Type | Jobs |
|--------|------|------|
| RemoteOK | API | ~90+ |
| Jobicy | API | ~50 |
| Landing Jobs | API | ~50 |
| Arbeitnow | API | ~10 |
| Remotive | API | ~5 |
| Himalayas | API | ~5 |
| BrighterMonday | Scraper | Kenya-specific |

**Total: 200+ real job postings updated regularly**

## ✨ Features

### 📈 Market Overview
- Total active job postings
- Companies actively hiring
- Average salary ranges (USD)
- Skills demand tracking

### 🛠️ Skills Analysis
- Top 30 most in-demand skills
- Skills by category (Programming, Cloud, ML/AI, BI Tools)
- Percentage of jobs requiring each skill

### 💼 Company Insights
- Top hiring companies
- Job distribution by company
- Company-specific trends

### 📍 Location Distribution
- Geographic job distribution
- Remote vs on-site opportunities
- Regional market analysis

### 💰 Salary Insights
- Salary ranges by experience level
- Industry salary benchmarks
- Compensation trends

### 🔍 Job Search
- Filter by location, experience, source
- Search by title, company, or skills
- Direct links to apply

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Local Installation

```bash
# Clone the repository
git clone https://github.com/gondamol/job-market-intelligence.git
cd job-market-intelligence

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard/app.py
```

### Running Scrapers

```bash
# Activate virtual environment
source venv/bin/activate

# Run all scrapers
python3 scripts/run_all_scrapers.py

# Update dashboard data
python3 scripts/update_dashboard_data.py
```

## 📁 Project Structure

```
job-market-intelligence/
├── dashboard/
│   ├── app.py              # Main Streamlit dashboard
│   └── demo_app.py         # Development version
├── scripts/
│   ├── run_all_scrapers.py         # Master scraper script
│   ├── scrape_all_sources.py       # Main API scrapers
│   ├── scrape_additional_sources.py # Extra API scrapers
│   ├── scrape_linkedin.py          # LinkedIn scraper (Selenium)
│   ├── scrape_brightermonday.py    # Kenya job board scraper
│   └── update_dashboard_data.py    # Dashboard data updater
├── data/
│   ├── processed/          # Dashboard-ready data
│   └── scraped/            # Raw scraped data
├── logs/                   # Scraper logs
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── requirements.txt        # Python dependencies
└── README.md
```

## 🔧 Technology Stack

| Category | Technology |
|----------|------------|
| **Frontend** | Streamlit, Plotly |
| **Data** | Pandas, JSON |
| **Scraping** | Requests, BeautifulSoup, Selenium |
| **APIs** | RemoteOK, Remotive, Arbeitnow, Jobicy |
| **Deployment** | Streamlit Community Cloud |

## 📈 Key Insights

Based on current data:

- **Top Skills**: Python, SQL, R, Excel, Power BI, AWS
- **Experience**: ~60% Senior roles, ~20% Mid-level, ~10% Entry
- **Remote**: ~85% of positions are remote-friendly
- **Industries**: Tech, Finance, Healthcare, Consulting

## 🔄 Automated Updates

The dashboard data is refreshed regularly via scheduled scrapers:

```bash
# Set up cron job (every 6 hours)
chmod +x scripts/setup_cron.sh
./scripts/setup_cron.sh
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Nicodemus Werre Amollo**
- Website: [gondamol.github.io](https://gondamol.github.io)
- LinkedIn: [linkedin.com/in/amollow](https://www.linkedin.com/in/nichodemusamollo/)
- Email: nichodemuswerre@gmail.com

---

*Built with ❤️ using Streamlit and Python*
