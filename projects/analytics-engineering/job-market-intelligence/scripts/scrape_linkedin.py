"""
LinkedIn Job Scraper using Selenium

Scrapes data analytics jobs from LinkedIn without authentication.
Uses headless Chrome for faster scraping.

Note: LinkedIn has anti-bot measures. This scraper uses public job listings
that don't require login.

Usage:
    python3 scripts/scrape_linkedin.py
"""
import json
import re
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import quote_plus

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "scraped"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Skills to detect
TARGET_SKILLS = [
    'Python', 'R', 'SQL', 'Excel', 'Power BI', 'Tableau',
    'PostgreSQL', 'MySQL', 'MongoDB', 'AWS', 'Azure', 'GCP',
    'Machine Learning', 'Statistics', 'Spark', 'Airflow',
    'Docker', 'Git', 'Looker', 'dbt', 'Snowflake', 'TensorFlow',
    'scikit-learn', 'Pandas', 'NumPy', 'Stata', 'SPSS',
    'Data Analysis', 'Data Science', 'Analytics', 'ETL',
    'Business Intelligence', 'BI', 'Visualization'
]


def extract_skills(text: str) -> List[str]:
    """Extract skills from text"""
    if not text:
        return []
    text_lower = text.lower()
    return [skill for skill in TARGET_SKILLS if skill.lower() in text_lower]


def detect_experience_level(title: str, description: str = "") -> str:
    """Detect experience level"""
    text = f"{title} {description}".lower()
    if any(w in text for w in ['senior', 'sr.', 'lead', 'principal', 'staff']):
        return 'Senior'
    elif any(w in text for w in ['junior', 'jr.', 'entry', 'graduate', 'intern']):
        return 'Entry'
    elif any(w in text for w in ['manager', 'director', 'vp', 'chief']):
        return 'Manager'
    return 'Mid'


def generate_job_id(source: str, url: str) -> str:
    """Generate unique job ID"""
    return hashlib.md5(f"{source}:{url}".encode()).hexdigest()[:16]


class LinkedInScraper:
    """LinkedIn job scraper using Selenium"""
    
    def __init__(self):
        self.base_url = "https://www.linkedin.com/jobs/search"
        self.name = "linkedin"
        self.driver = None
    
    def setup_driver(self):
        """Set up headless Chrome driver"""
        if not SELENIUM_AVAILABLE:
            logger.error("Selenium not installed. Run: pip install selenium webdriver-manager")
            return False
        
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Disable automation flags
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Avoid detection
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                '''
            })
            
            logger.info("✅ Chrome driver initialized")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to set up driver: {e}")
            return False
    
    def close_driver(self):
        """Close the driver"""
        if self.driver:
            self.driver.quit()
    
    def build_search_url(self, keywords: str, location: str = "", remote: bool = False) -> str:
        """Build LinkedIn job search URL"""
        params = {
            'keywords': keywords,
            'location': location,
            'f_TPR': 'r86400',  # Last 24 hours
        }
        if remote:
            params['f_WT'] = '2'  # Remote
        
        query = '&'.join(f"{k}={quote_plus(str(v))}" for k, v in params.items())
        return f"{self.base_url}?{query}"
    
    def scrape_job_listings(self, keywords: str = "data analyst", location: str = "", max_jobs: int = 50) -> List[Dict]:
        """Scrape job listings from LinkedIn"""
        if not self.setup_driver():
            return []
        
        jobs = []
        
        try:
            # Build and navigate to search URL
            url = self.build_search_url(keywords, location, remote=True)
            logger.info(f"🔍 Searching: {keywords}")
            logger.info(f"   URL: {url}")
            
            self.driver.get(url)
            time.sleep(3)  # Wait for page load
            
            # Scroll to load more jobs
            for _ in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, 
                'div.base-card, div.job-search-card, li.jobs-search-results__list-item'
            )
            
            logger.info(f"   Found {len(job_cards)} job cards")
            
            for card in job_cards[:max_jobs]:
                try:
                    job = self._parse_job_card(card)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    logger.warning(f"   Error parsing card: {e}")
            
            logger.info(f"   ✅ Parsed {len(jobs)} jobs")
            
        except Exception as e:
            logger.error(f"❌ Scraping error: {e}")
        
        finally:
            self.close_driver()
        
        return jobs
    
    def _parse_job_card(self, card) -> Optional[Dict]:
        """Parse a LinkedIn job card"""
        try:
            # Title
            title_elem = card.find_element(By.CSS_SELECTOR, 
                'h3.base-search-card__title, .job-search-card__title, h3'
            )
            title = title_elem.text.strip() if title_elem else 'Unknown'
            
            # Company
            company_elem = card.find_element(By.CSS_SELECTOR,
                'h4.base-search-card__subtitle, .base-search-card__subtitle, a.hidden-nested-link'
            )
            company = company_elem.text.strip() if company_elem else 'Unknown'
            
            # Location
            location_elem = card.find_element(By.CSS_SELECTOR,
                'span.job-search-card__location, .job-result-card__location'
            )
            location = location_elem.text.strip() if location_elem else 'Remote'
            
            # URL
            link_elem = card.find_element(By.CSS_SELECTOR, 'a.base-card__full-link, a')
            job_url = link_elem.get_attribute('href') if link_elem else ''
            
            # Posted date (if available)
            try:
                date_elem = card.find_element(By.CSS_SELECTOR, 'time, .job-search-card__listdate')
                posted_date = date_elem.get_attribute('datetime') or date_elem.text
            except:
                posted_date = datetime.now().isoformat()
            
            return {
                'job_id': generate_job_id(self.name, job_url),
                'source': self.name,
                'source_url': job_url,
                'title': title,
                'company_name': company,
                'location': location,
                'country': 'International',
                'remote_type': 'Remote' if 'remote' in location.lower() else 'On-site',
                'description': '',  # Would need to visit individual page
                'employment_type': 'Full-time',
                'experience_level': detect_experience_level(title, ''),
                'skills': extract_skills(title),
                'posted_date': posted_date,
                'scraped_at': datetime.now().isoformat(),
                'is_active': True,
            }
            
        except Exception as e:
            logger.debug(f"Parse error: {e}")
            return None
    
    def run(self, search_queries: List[str] = None) -> List[Dict]:
        """Run the scraper with multiple search queries"""
        search_queries = search_queries or [
            'data analyst',
            'data scientist',
            'business intelligence',
            'data engineer',
            'machine learning engineer'
        ]
        
        all_jobs = []
        seen_urls = set()
        
        for query in search_queries:
            jobs = self.scrape_job_listings(keywords=query, max_jobs=30)
            for job in jobs:
                if job['source_url'] not in seen_urls:
                    seen_urls.add(job['source_url'])
                    all_jobs.append(job)
            time.sleep(5)  # Rate limit between searches
        
        logger.info(f"\n📊 Total unique jobs: {len(all_jobs)}")
        return all_jobs
    
    def save_results(self, jobs: List[Dict]) -> Path:
        """Save results to JSON"""
        if not jobs:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"linkedin_jobs_{timestamp}.json"
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(jobs, f, indent=2, default=str)
        
        logger.info(f"💾 Saved {len(jobs)} jobs to {filepath}")
        
        # Also save as latest
        latest = OUTPUT_DIR / "linkedin_latest.json"
        with open(latest, 'w') as f:
            json.dump(jobs, f, indent=2, default=str)
        
        return filepath


def main():
    """Main entry point"""
    print("=" * 60)
    print("🔗 LINKEDIN JOB SCRAPER (Selenium)")
    print("=" * 60)
    
    if not SELENIUM_AVAILABLE:
        print("\n❌ Selenium not installed!")
        print("Run: pip install selenium webdriver-manager")
        return
    
    scraper = LinkedInScraper()
    
    # Scrape with multiple keywords
    jobs = scraper.run([
        'data analyst remote',
        'data scientist remote',
        'analytics engineer'
    ])
    
    if jobs:
        scraper.save_results(jobs)
        
        print(f"\n✅ Scraped {len(jobs)} jobs from LinkedIn")
        print("\nSample jobs:")
        for job in jobs[:5]:
            print(f"  • {job['title']} at {job['company_name']}")
    else:
        print("\n⚠️ No jobs scraped. LinkedIn may have blocked the request.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
