"""
BrighterMonday Kenya Job Scraper - Standalone Version

Scrapes real job postings from BrighterMonday.co.ke and saves to JSON files.

Usage:
    python3 scripts/scrape_brightermonday.py
"""
import json
import re
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, quote_plus
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "scraped"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuration
CONFIG = {
    'rate_limit_delay': 2,
    'timeout': 30,
    'retry_times': 3,
    'max_pages': 5,
    'user_agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}

# Search keywords
SEARCH_KEYWORDS = [
    'data-analyst',
    'data-scientist', 
    'business-intelligence',
    'data-engineer',
    'analytics',
    'statistician',
    'machine-learning',
    'research',
]

# Skills to extract
TARGET_SKILLS = [
    'Python', 'R', 'SQL', 'Excel', 'Power BI', 'Tableau',
    'PostgreSQL', 'MySQL', 'MongoDB', 'AWS', 'Azure', 'GCP',
    'Machine Learning', 'Statistics', 'Spark', 'Airflow',
    'Docker', 'Git', 'Looker', 'dbt', 'Snowflake', 'TensorFlow',
    'scikit-learn', 'Pandas', 'NumPy', 'Stata', 'SPSS',
    'Java', 'JavaScript', 'Scala', 'Hadoop', 'Kafka', 'REDCap',
    'SurveyCTO', 'ODK', 'Shiny', 'ggplot2', 'tidyverse'
]


class BrighterMondayScraper:
    """Scraper for BrighterMonday.co.ke"""
    
    def __init__(self):
        self.base_url = 'https://www.brightermonday.co.ke'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': CONFIG['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.jobs_scraped = []
        self.seen_urls = set()
    
    def generate_job_id(self, url: str) -> str:
        """Generate unique job ID"""
        return hashlib.md5(f"brightermonday:{url}".encode()).hexdigest()[:16]
    
    def rate_limit(self):
        """Rate limiting"""
        time.sleep(CONFIG['rate_limit_delay'])
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch page with retries"""
        for attempt in range(CONFIG['retry_times']):
            try:
                logger.debug(f"Fetching: {url}")
                response = self.session.get(url, timeout=CONFIG['timeout'])
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < CONFIG['retry_times'] - 1:
                    time.sleep(2 ** attempt)
        return None
    
    def parse_posted_date(self, date_text: str) -> str:
        """Parse date text to ISO format"""
        if not date_text:
            return datetime.now().isoformat()
        
        date_text = date_text.lower().strip()
        now = datetime.now()
        
        if 'hour' in date_text:
            match = re.search(r'(\d+)\s*hour', date_text)
            if match:
                return (now - timedelta(hours=int(match.group(1)))).isoformat()
        
        elif 'day' in date_text:
            match = re.search(r'(\d+)\s*day', date_text)
            if match:
                return (now - timedelta(days=int(match.group(1)))).isoformat()
        
        elif 'week' in date_text:
            match = re.search(r'(\d+)\s*week', date_text)
            if match:
                return (now - timedelta(weeks=int(match.group(1)))).isoformat()
        
        elif 'month' in date_text:
            match = re.search(r'(\d+)\s*month', date_text)
            if match:
                return (now - timedelta(days=int(match.group(1)) * 30)).isoformat()
        
        elif 'today' in date_text or 'just now' in date_text:
            return now.isoformat()
        
        elif 'yesterday' in date_text:
            return (now - timedelta(days=1)).isoformat()
        
        return now.isoformat()
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        for skill in TARGET_SKILLS:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return found_skills
    
    def detect_experience_level(self, title: str, description: str) -> str:
        """Detect experience level"""
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['senior', 'sr.', 'lead', 'principal', 'head']):
            return 'Senior'
        elif any(word in text for word in ['junior', 'jr.', 'entry', 'graduate', 'intern', 'trainee']):
            return 'Entry'
        elif any(word in text for word in ['manager', 'director', 'vp', 'chief', 'head of']):
            return 'Manager'
        
        return 'Mid'
    
    def detect_employment_type(self, text: str) -> str:
        """Detect employment type"""
        text = text.lower()
        
        if 'contract' in text or 'fixed term' in text or 'temporary' in text:
            return 'Contract'
        elif 'part-time' in text or 'part time' in text:
            return 'Part-time'
        elif 'intern' in text:
            return 'Internship'
        elif 'volunteer' in text:
            return 'Volunteer'
        
        return 'Full-time'
    
    def parse_salary(self, text: str) -> tuple:
        """Extract salary"""
        if not text:
            return None, None
        
        text = text.lower().replace(',', '').replace(' ', '')
        
        patterns = [
            r'kes?\s*(\d+)k?\s*[-–to]\s*(\d+)k?',
            r'ksh?\s*(\d+)k?\s*[-–to]\s*(\d+)k?',
            r'(\d+)k\s*[-–to]\s*(\d+)k',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                min_sal = int(match.group(1))
                max_sal = int(match.group(2))
                if min_sal < 1000:
                    min_sal *= 1000
                if max_sal < 1000:
                    max_sal *= 1000
                return min_sal, max_sal
        
        return None, None
    
    def build_search_url(self, keyword: str, page: int = 1) -> str:
        """Build search URL"""
        # BrighterMonday uses category paths, don't add page=1 as it causes redirect issues
        if page == 1:
            return f"{self.base_url}/jobs/{keyword}"
        return f"{self.base_url}/jobs/{keyword}?page={page}"
    
    def scrape_job_listings(self, keyword: str) -> List[Dict]:
        """Scrape job listings for a keyword"""
        jobs = []
        
        for page in range(1, CONFIG['max_pages'] + 1):
            url = self.build_search_url(keyword, page)
            logger.info(f"📄 Page {page}: {url}")
            
            soup = self.fetch_page(url)
            if not soup:
                break
            
            # Find job cards using data-job-id attribute (article elements)
            job_cards = soup.find_all('article', attrs={'data-job-id': True})
            logger.info(f"   Found {len(job_cards)} job cards")
            
            if not job_cards:
                logger.info(f"   No jobs found on page {page}")
                break
            
            for card in job_cards:
                try:
                    job_data = self.parse_job_card(card)
                    if job_data and job_data['source_url'] not in self.seen_urls:
                        self.seen_urls.add(job_data['source_url'])
                        jobs.append(job_data)
                        logger.info(f"   ✓ {job_data['title'][:40]} at {job_data['company_name'][:30]}")
                except Exception as e:
                    logger.warning(f"   Error parsing card: {e}")
            
            self.rate_limit()
            
            # Check for next page
            next_btn = soup.find('a', {'rel': 'next'}) or soup.find('a', text=re.compile(r'next|→', re.I))
            if not next_btn:
                break
        
        return jobs
    
    def parse_job_card(self, card) -> Optional[Dict]:
        """Parse job card from BrighterMonday"""
        try:
            job_id = card.get('data-job-id', '')
            
            # Title - h1 with data-cy="title-job"
            title_elem = (
                card.find('h1', attrs={'data-cy': 'title-job'}) or
                card.find('h1') or
                card.find(['h2', 'h3'])
            )
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown Position'
            
            # Company - second h2 element or first h2 after h1
            h2_elements = card.find_all('h2')
            company = 'Unknown Company'
            for h2 in h2_elements:
                text = h2.get_text(strip=True)
                # Skip category links (Software & Data, etc.)
                if text and not any(cat in text.lower() for cat in ['software', 'data', '&']):
                    company = text
                    break
                # Or take first substantial h2
                if text and len(text) > 3 and 'Software' not in text:
                    company = text
                    break
            
            if company == 'Unknown Company' and h2_elements:
                company = h2_elements[0].get_text(strip=True)
            
            # Location - look for links to /jobs/nairobi etc. or spans with location
            location = 'Kenya'
            location_link = card.find('a', href=re.compile(r'/jobs/(nairobi|mombasa|kisumu|eldoret|nakuru)', re.I))
            if location_link:
                location = location_link.get_text(strip=True)
            else:
                # Try finding any location mention in the card
                location_span = card.find(text=re.compile(r'nairobi|mombasa|kisumu|eldoret|nakuru|kenya', re.I))
                if location_span:
                    location = location_span.strip()
            
            # Employment type
            emp_link = card.find('a', href=re.compile(r'/jobs/(full-time|part-time|contract|temporary)', re.I))
            employment_type = emp_link.get_text(strip=True) if emp_link else 'Full-time'
            
            # Posted date (usually "Today", "2 days ago", etc.)
            date_elem = card.find(text=re.compile(r'today|yesterday|\d+\s*(day|week|month|hour)', re.I))
            posted_date = self.parse_posted_date(date_elem.strip() if date_elem else '')
            
            # Salary - look for KES spans
            salary_min, salary_max = None, None
            salary_span = card.find('span', text=re.compile(r'KES', re.I))
            if salary_span:
                salary_text = salary_span.parent.get_text() if salary_span.parent else salary_span.get_text()
                salary_min, salary_max = self.parse_salary(salary_text)
            
            # Build source URL - need to find the actual job link
            # Job detail links usually contain /job/ in the href
            job_link = card.find('a', href=re.compile(r'/job/\d+'))
            if job_link:
                source_url = urljoin(self.base_url, job_link.get('href', ''))
            else:
                # Construct from job_id
                source_url = f"{self.base_url}/job/{job_id}"
            
            # Description snippet (if available)
            desc_elem = card.find(class_=re.compile(r'description|summary', re.I))
            description = desc_elem.get_text(strip=True) if desc_elem else ''
            
            return {
                'job_id': self.generate_job_id(source_url),
                'external_id': job_id,
                'source': 'brightermonday',
                'source_url': source_url,
                'title': title,
                'company_name': company,
                'location': location,
                'country': 'Kenya',
                'description': description,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'salary_currency': 'KES' if salary_min else None,
                'posted_date': posted_date,
                'scraped_at': datetime.now().isoformat(),
                'experience_level': self.detect_experience_level(title, description),
                'employment_type': employment_type,
                'skills': self.extract_skills(f"{title} {description}"),
                'is_active': True,
            }
            
        except Exception as e:
            logger.error(f"Error parsing card: {e}")
            return None
    
    def scrape_job_details(self, job: Dict) -> Dict:
        """Scrape full details from job page"""
        url = job.get('source_url')
        if not url:
            return job
        
        soup = self.fetch_page(url)
        if not soup:
            return job
        
        try:
            # Full description
            desc_elem = (
                soup.find(class_=re.compile(r'description|job-content|details', re.I)) or
                soup.find('article') or
                soup.find(id='job-details')
            )
            if desc_elem:
                full_desc = desc_elem.get_text(strip=True)
                job['description'] = full_desc[:3000]  # Truncate
                job['skills'] = self.extract_skills(full_desc)
            
            # Salary
            salary_elem = soup.find(class_=re.compile(r'salary|pay|compensation', re.I))
            if salary_elem:
                salary_min, salary_max = self.parse_salary(salary_elem.get_text())
                job['salary_min'] = salary_min
                job['salary_max'] = salary_max
                job['salary_currency'] = 'KES'
            
            # Update experience level with full description
            job['experience_level'] = self.detect_experience_level(
                job.get('title', ''), 
                job.get('description', '')
            )
            
        except Exception as e:
            logger.warning(f"Error scraping details: {e}")
        
        return job
    
    def run(self, keywords: List[str] = None, fetch_details: bool = False) -> List[Dict]:
        """Run the scraper"""
        keywords = keywords or SEARCH_KEYWORDS
        
        logger.info(f"🚀 Starting BrighterMonday scraper...")
        logger.info(f"   Keywords: {', '.join(keywords)}")
        
        all_jobs = []
        
        for keyword in keywords:
            logger.info(f"\n🔍 Searching for '{keyword}'...")
            jobs = self.scrape_job_listings(keyword)
            all_jobs.extend(jobs)
            logger.info(f"   Found {len(jobs)} jobs")
            self.rate_limit()
        
        # Remove duplicates
        unique_jobs = {}
        for job in all_jobs:
            if job['job_id'] not in unique_jobs:
                unique_jobs[job['job_id']] = job
        
        self.jobs_scraped = list(unique_jobs.values())
        
        # Optionally fetch full details
        if fetch_details and self.jobs_scraped:
            logger.info(f"\n📋 Fetching detailed info for {len(self.jobs_scraped)} jobs...")
            for i, job in enumerate(self.jobs_scraped):
                logger.info(f"   [{i+1}/{len(self.jobs_scraped)}] {job['title'][:40]}...")
                self.jobs_scraped[i] = self.scrape_job_details(job)
                self.rate_limit()
        
        logger.info(f"\n✅ Scraping complete! Total unique jobs: {len(self.jobs_scraped)}")
        
        return self.jobs_scraped
    
    def save_results(self, filename: str = None) -> Path:
        """Save to JSON"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"brightermonday_jobs_{timestamp}.json"
        
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.jobs_scraped, f, indent=2, default=str)
        
        logger.info(f"💾 Saved {len(self.jobs_scraped)} jobs to {filepath}")
        
        # Also save as latest
        latest = OUTPUT_DIR / "brightermonday_latest.json"
        with open(latest, 'w') as f:
            json.dump(self.jobs_scraped, f, indent=2, default=str)
        
        return filepath
    
    def generate_stats(self) -> Dict:
        """Generate statistics"""
        if not self.jobs_scraped:
            return {}
        
        skill_counts = {}
        company_counts = {}
        location_counts = {}
        exp_counts = {}
        
        for job in self.jobs_scraped:
            for skill in job.get('skills', []):
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
            
            company = job.get('company_name', 'Unknown')
            company_counts[company] = company_counts.get(company, 0) + 1
            
            location = job.get('location', 'Unknown')
            location_counts[location] = location_counts.get(location, 0) + 1
            
            exp = job.get('experience_level', 'Unknown')
            exp_counts[exp] = exp_counts.get(exp, 0) + 1
        
        stats = {
            'total_jobs': len(self.jobs_scraped),
            'source': 'brightermonday',
            'scraped_at': datetime.now().isoformat(),
            'top_skills': sorted(skill_counts.items(), key=lambda x: -x[1])[:20],
            'top_companies': sorted(company_counts.items(), key=lambda x: -x[1])[:20],
            'locations': sorted(location_counts.items(), key=lambda x: -x[1]),
            'experience_levels': exp_counts,
        }
        
        stats_path = OUTPUT_DIR / "brightermonday_stats.json"
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        
        return stats


def main():
    """Main entry point"""
    print("=" * 60)
    print("🌟 BRIGHTERMONDAY KENYA JOB SCRAPER")
    print("=" * 60)
    print()
    
    scraper = BrighterMondayScraper()
    
    # Test with key data analytics keywords
    test_keywords = ['data-analyst', 'data-scientist', 'analytics', 'business-intelligence']
    
    jobs = scraper.run(keywords=test_keywords, fetch_details=False)
    
    if jobs:
        scraper.save_results()
        stats = scraper.generate_stats()
        
        print("\n" + "=" * 60)
        print("📊 SCRAPING SUMMARY")
        print("=" * 60)
        print(f"Total Jobs: {stats['total_jobs']}")
        print(f"\nTop Skills:")
        for skill, count in stats['top_skills'][:10]:
            print(f"  - {skill}: {count}")
        print(f"\nTop Companies:")
        for company, count in stats['top_companies'][:10]:
            print(f"  - {company}: {count}")
        print(f"\nLocations:")
        for location, count in stats['locations'][:5]:
            print(f"  - {location}: {count}")
        print(f"\nExperience Levels:")
        for level, count in stats['experience_levels'].items():
            print(f"  - {level}: {count}")
    else:
        print("\n⚠️ No jobs found.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
