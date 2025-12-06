#!/usr/bin/env python3
"""
Telegram Job Alert Bot

Sends notifications to Telegram when new matching jobs are found.

Setup:
1. Create a bot via @BotFather on Telegram
2. Get your chat ID by messaging @userinfobot
3. Set environment variables or create .env file:
   - TELEGRAM_BOT_TOKEN=your_bot_token
   - TELEGRAM_CHAT_ID=your_chat_id

Usage:
    python3 scripts/telegram_alerts.py

Environment Variables:
    TELEGRAM_BOT_TOKEN: Bot token from @BotFather
    TELEGRAM_CHAT_ID: Your chat ID or channel ID
    
Or create a .env file with these values.
"""
import os
import json
import requests
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
PROJECT_DIR = Path(__file__).parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
ALERTS_FILE = PROJECT_DIR / "data" / "last_alerts.json"


def load_env_file():
    """Load environment variables from .env file"""
    env_file = PROJECT_DIR / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')


def get_telegram_config():
    """Get Telegram configuration from environment"""
    load_env_file()
    
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        logger.warning("Telegram credentials not configured")
        logger.info("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables")
        return None, None
    
    return token, chat_id


class TelegramBot:
    """Simple Telegram bot for job alerts"""
    
    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{token}"
    
    def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """Send a message to Telegram"""
        try:
            response = requests.post(
                f"{self.api_url}/sendMessage",
                json={
                    "chat_id": self.chat_id,
                    "text": text,
                    "parse_mode": parse_mode,
                    "disable_web_page_preview": True
                },
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("✅ Message sent successfully")
                return True
            else:
                logger.error(f"❌ Failed to send message: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error sending message: {e}")
            return False
    
    def format_job_alert(self, job: Dict) -> str:
        """Format a job posting for Telegram"""
        title = job.get('title', 'Unknown Position')
        company = job.get('company_name', 'Unknown Company')
        location = job.get('location', 'Unknown')
        url = job.get('source_url', '')
        source = job.get('source', 'Unknown')
        skills = job.get('skills', [])[:5]
        
        # Format salary
        salary = ""
        if job.get('salary_min') or job.get('salary_max'):
            sal_min = job.get('salary_min', 0)
            sal_max = job.get('salary_max', 0)
            if sal_min and sal_max:
                salary = f"\n💰 ${sal_min:,} - ${sal_max:,}"
            elif sal_max:
                salary = f"\n💰 Up to ${sal_max:,}"
        
        skills_str = ""
        if skills:
            skills_str = f"\n🛠️ {', '.join(skills[:5])}"
        
        message = f"""🆕 <b>{title}</b>

🏢 {company}
📍 {location}
📌 Source: {source.title()}{salary}{skills_str}

<a href="{url}">🔗 Apply Now</a>"""
        
        return message
    
    def send_job_alert(self, job: Dict) -> bool:
        """Send a job alert"""
        message = self.format_job_alert(job)
        return self.send_message(message)
    
    def send_summary(self, jobs: List[Dict], new_count: int) -> bool:
        """Send a summary of new jobs"""
        if new_count == 0:
            message = "📊 <b>Job Market Update</b>\n\nNo new matching jobs found."
        else:
            # Top skills from new jobs
            skills = {}
            for job in jobs[:new_count]:
                for skill in job.get('skills', []):
                    skills[skill] = skills.get(skill, 0) + 1
            
            top_skills = sorted(skills.items(), key=lambda x: -x[1])[:5]
            skills_str = ", ".join([s[0] for s in top_skills]) if top_skills else "Various"
            
            message = f"""📊 <b>Job Market Update</b>

🆕 <b>{new_count} new jobs found!</b>

📈 Total jobs tracked: {len(jobs)}
🛠️ Top skills: {skills_str}

<a href="https://data-analytics-jobs.streamlit.app">🔗 View Dashboard</a>"""
        
        return self.send_message(message)


def load_last_alerts() -> Dict:
    """Load record of last sent alerts"""
    if ALERTS_FILE.exists():
        with open(ALERTS_FILE) as f:
            return json.load(f)
    return {"last_job_ids": [], "last_check": None}


def save_last_alerts(data: Dict):
    """Save record of sent alerts"""
    ALERTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def load_jobs() -> List[Dict]:
    """Load current jobs"""
    jobs_file = PROCESSED_DIR / "jobs.json"
    if jobs_file.exists():
        with open(jobs_file) as f:
            return json.load(f)
    return []


def filter_relevant_jobs(jobs: List[Dict], keywords: List[str] = None) -> List[Dict]:
    """Filter jobs by relevant keywords"""
    keywords = keywords or [
        'data analyst', 'data scientist', 'analytics', 'business intelligence',
        'data engineer', 'machine learning', 'python', 'sql', 'tableau', 'power bi'
    ]
    
    relevant = []
    for job in jobs:
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        skills = ' '.join(job.get('skills', [])).lower()
        
        combined = f"{title} {description} {skills}"
        
        if any(kw.lower() in combined for kw in keywords):
            relevant.append(job)
    
    return relevant


def find_new_jobs(current_jobs: List[Dict], last_job_ids: List[str]) -> List[Dict]:
    """Find jobs that haven't been alerted before"""
    new_jobs = []
    for job in current_jobs:
        job_id = job.get('job_id', '')
        if job_id and job_id not in last_job_ids:
            new_jobs.append(job)
    return new_jobs


def run_alerts(max_individual_alerts: int = 5, send_summary: bool = True):
    """Main function to run job alerts"""
    logger.info("=" * 50)
    logger.info("🔔 Running Job Alerts")
    logger.info("=" * 50)
    
    # Get Telegram config
    token, chat_id = get_telegram_config()
    if not token or not chat_id:
        logger.error("Telegram not configured. Exiting.")
        return
    
    bot = TelegramBot(token, chat_id)
    
    # Load jobs
    jobs = load_jobs()
    if not jobs:
        logger.warning("No jobs found")
        return
    
    # Filter relevant jobs
    relevant_jobs = filter_relevant_jobs(jobs)
    logger.info(f"Found {len(relevant_jobs)} relevant jobs out of {len(jobs)} total")
    
    # Find new jobs
    last_alerts = load_last_alerts()
    last_job_ids = last_alerts.get("last_job_ids", [])
    
    new_jobs = find_new_jobs(relevant_jobs, last_job_ids)
    logger.info(f"Found {len(new_jobs)} new jobs")
    
    # Send individual alerts for top new jobs
    sent_count = 0
    for job in new_jobs[:max_individual_alerts]:
        if bot.send_job_alert(job):
            sent_count += 1
    
    if sent_count > 0:
        logger.info(f"Sent {sent_count} individual job alerts")
    
    # Send summary if requested
    if send_summary:
        bot.send_summary(relevant_jobs, len(new_jobs))
    
    # Update last alerts
    current_job_ids = [j.get('job_id', '') for j in relevant_jobs]
    save_last_alerts({
        "last_job_ids": current_job_ids,
        "last_check": datetime.now().isoformat()
    })
    
    logger.info("=" * 50)
    logger.info("✅ Alerts complete")
    logger.info("=" * 50)


def test_connection():
    """Test Telegram bot connection"""
    token, chat_id = get_telegram_config()
    if not token or not chat_id:
        print("❌ Telegram not configured")
        print("\nTo configure:")
        print("1. Message @BotFather on Telegram to create a bot")
        print("2. Message @userinfobot to get your chat ID")
        print("3. Create .env file with:")
        print("   TELEGRAM_BOT_TOKEN=your_bot_token")
        print("   TELEGRAM_CHAT_ID=your_chat_id")
        return False
    
    bot = TelegramBot(token, chat_id)
    
    test_message = """🤖 <b>Job Market Intelligence Bot</b>

✅ Connection test successful!

Your bot is configured and ready to send job alerts.

<a href="https://data-analytics-jobs.streamlit.app">🔗 View Dashboard</a>"""
    
    if bot.send_message(test_message):
        print("✅ Test message sent successfully!")
        return True
    else:
        print("❌ Failed to send test message")
        return False


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_connection()
    else:
        run_alerts()


if __name__ == "__main__":
    main()
