"""
Standalone Fuzu Job Scraper - No Database Required

Scrapes real job postings from Fuzu.com Kenya and saves to JSON files.
This version works independently without PostgreSQL.

Usage:
    python3 scripts/scrape_fuzu.py
"""
import json
import re
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlencode, quote_plus
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
    'rate_limit_delay': 2,  # seconds between requests
    'timeout': 30,
    'retry_times': 3,
    'max_pages': 3,  # pages per keyword
    'user_agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}

# Search keywords for data analytics jobs
SEARCH_KEYWORDS = [
    'data analyst',
    'data scientist',
    'business intelligence',
    'data engineer',
    'analytics',
    'statistician',
    'machine learning',
    'research analyst',
]

# Skills to extract
TARGET_SKILLS = [
    'Python', 'R', 'SQL', 'Excel', 'Power BI', 'Tableau',
    'PostgreSQL', 'MySQL', 'MongoDB', 'AWS', 'Azure', 'GCP',
    'Machine Learning', 'Statistics', 'Spark', 'Airflow',
    'Docker', 'Git', 'Looker', 'dbt', 'Snowflake', 'TensorFlow',
    'scikit-learn', 'Pandas', 'NumPy', 'Stata', 'SPSS',
    'Java', 'JavaScript', 'Scala', 'Hadoop', 'Kafka'
]


class FuzuScraper:
    """Standalone scraper for Fuzu.com Kenya"""
    
    def __init__(self):
        self.base_url = 'https://www.fuzu.com'
        self.search_url = 'https://www.fuzu.com/kenya/jobs'
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
        """Generate unique job ID from URL"""
        return hashlib.md5(f"fuzu:{url}".encode()).hexdigest()[:16]
    
    def rate_limit(self):
        """Apply rate limiting between requests"""
        time.sleep(CONFIG['rate_limit_delay'])
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page with retry logic"""
        for attempt in range(CONFIG['retry_times']):
            try:
                logger.debug(f"Fetching: {url}")
                response = self.session.get(url, timeout=CONFIG['timeout'])
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < CONFIG['retry_times'] - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All attempts failed for {url}")
                    return None
        return None
    
    def parse_posted_date(self, date_text: str) -> str:
        """Parse Fuzu's posted date text to ISO format"""
        if not date_text:
            return datetime.now().isoformat()
        
        date_text = date_text.lower().strip()
        now = datetime.now()
        
        if 'hour' in date_text:
            match = re.search(r'(\d+)\s*hour', date_text)
            if match:
                result = now - timedelta(hours=int(match.group(1)))
                return result.isoformat()
        
        elif 'day' in date_text:
            match = re.search(r'(\d+)\s*day', date_text)
            if match:
                result = now - timedelta(days=int(match.group(1)))
                return result.isoformat()
        
        elif 'week' in date_text:
            match = re.search(r'(\d+)\s*week', date_text)
            if match:
                result = now - timedelta(weeks=int(match.group(1)))
                return result.isoformat()
        
        elif 'month' in date_text:
            match = re.search(r'(\d+)\s*month', date_text)
            if match:
                result = now - timedelta(days=int(match.group(1)) * 30)
                return result.isoformat()
        
        elif 'today' in date_text:
            return now.isoformat()
        
        elif 'yesterday' in date_text:
            return (now - timedelta(days=1)).isoformat()
        
        return now.isoformat()
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from job description"""
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
        """Detect experience level from text"""
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['senior', 'sr.', 'lead', 'principal', 'head']):
            return 'Senior'
        elif any(word in text for word in ['junior', 'jr.', 'entry', 'graduate', 'intern']):
            return 'Entry'
        elif any(word in text for word in ['manager', 'director', 'vp', 'chief']):
            return 'Manager'
        
        return 'Mid'
    
    def detect_employment_type(self, text: str) -> str:
        """Detect employment type"""
        text = text.lower()
        
        if 'contract' in text or 'fixed term' in text:
            return 'Contract'
        elif 'part-time' in text or 'part time' in text:
            return 'Part-time'
        elif 'intern' in text:
            return 'Internship'
        
        return 'Full-time'
    
    def parse_salary(self, text: str) -> tuple:
        """Extract salary range from text"""
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
        # Fuzu uses different URL structure
        keyword_slug = quote_plus(keyword)
        return f"{self.search_url}?utf8=%E2%9C%93&q={keyword_slug}&page={page}"
    
    def scrape_job_list(self, keyword: str) -> List[Dict]:
        """Scrape job listings for a keyword"""
        jobs = []
        
        for page in range(1, CONFIG['max_pages'] + 1):
            url = self.build_search_url(keyword, page)
            logger.info(f"📄 Scraping page {page} for '{keyword}': {url}")
            
            soup = self.fetch_page(url)
            if not soup:
                break
            
            # Try multiple selectors for job cards
            job_cards = (
                soup.select('.job-listing') or
                soup.select('.job-card') or
                soup.select('[data-controller="job-card"]') or
                soup.select('article.job') or
                soup.select('.jobs-list > div') or
                soup.find_all('div', class_=lambda x: x and 'job' in x.lower()) or
                soup.find_all('a', href=lambda x: x and '/jobs/' in str(x))
            )
            
            logger.info(f"   Found {len(job_cards)} job cards")
            
            if not job_cards:
                # Try to find job links directly
                job_links = soup.find_all('a', href=re.compile(r'/kenya/jobs/\d+'))
                logger.info(f"   Found {len(job_links)} job links instead")
                
                for link in job_links:
                    job_url = urljoin(self.base_url, link.get('href', ''))
                    if job_url not in self.seen_urls:
                        self.seen_urls.add(job_url)
                        # Scrape the individual job page
                        job_data = self.scrape_job_page(job_url)
                        if job_data:
                            jobs.append(job_data)
                            self.rate_limit()
            else:
                for card in job_cards:
                    try:
                        job_data = self.parse_job_card(card)
                        if job_data and job_data['source_url'] not in self.seen_urls:
                            self.seen_urls.add(job_data['source_url'])
                            jobs.append(job_data)
                    except Exception as e:
                        logger.warning(f"   Error parsing card: {e}")
                        continue
            
            self.rate_limit()
            
            # Check for next page
            next_btn = soup.find('a', {'rel': 'next'}) or soup.find('a', text=re.compile(r'next|→|»', re.I))
            if not next_btn:
                logger.info(f"   No more pages for '{keyword}'")
                break
        
        return jobs
    
    def parse_job_card(self, card) -> Optional[Dict]:
        """Parse a job card from search results"""
        try:
            # Find job URL
            link_elem = (
                card.find('a', href=re.compile(r'/jobs/|/kenya/jobs/')) or
                card.find('a', href=True)
            )
            
            if not link_elem:
                return None
            
            job_url = urljoin(self.base_url, link_elem.get('href', ''))
            
            # Title
            title_elem = (
                card.find(['h2', 'h3', 'h4']) or
                card.find('a', class_=re.compile(r'title', re.I)) or
                link_elem
            )
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown'
            
            # Company
            company_elem = (
                card.find(class_=re.compile(r'company|employer|org', re.I)) or
                card.find('span', text=re.compile(r'^[A-Z].*Ltd|Inc|PLC|Limited', re.I))
            )
            company = company_elem.get_text(strip=True) if company_elem else 'Unknown'
            
            # Location
            location_elem = card.find(class_=re.compile(r'location|place|city', re.I))
            location = location_elem.get_text(strip=True) if location_elem else 'Kenya'
            
            # Date
            date_elem = card.find(class_=re.compile(r'date|time|posted|ago', re.I))
            posted_date = self.parse_posted_date(
                date_elem.get_text(strip=True) if date_elem else ''
            )
            
            # Description snippet
            desc_elem = card.find(class_=re.compile(r'desc|summary|snippet', re.I))
            description = desc_elem.get_text(strip=True) if desc_elem else ''
            
            return {
                'job_id': self.generate_job_id(job_url),
                'source': 'fuzu',
                'source_url': job_url,
                'title': title,
                'company_name': company,
                'location': location,
                'country': 'Kenya',
                'description': description,
                'posted_date': posted_date,
                'scraped_at': datetime.now().isoformat(),
                'experience_level': self.detect_experience_level(title, description),
                'employment_type': self.detect_employment_type(f"{title} {description}"),
                'skills': self.extract_skills(description),
                'is_active': True,
            }
            
        except Exception as e:
            logger.error(f"Error parsing job card: {e}")
            return None
    
    def scrape_job_page(self, url: str) -> Optional[Dict]:
        """Scrape detailed information from a job page"""
        soup = self.fetch_page(url)
        if not soup:
            return None
        
        try:
            # Title
            title_elem = (
                soup.find('h1') or
                soup.find(class_=re.compile(r'job-title|position', re.I))
            )
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown'
            
            # Company
            company_elem = (
                soup.find(class_=re.compile(r'company-name|employer', re.I)) or
                soup.find('a', href=re.compile(r'/companies/'))
            )
            company = company_elem.get_text(strip=True) if company_elem else 'Unknown'
            
            # Location
            location_elem = soup.find(class_=re.compile(r'location|place', re.I))
            location = location_elem.get_text(strip=True) if location_elem else 'Kenya'
            
            # Description
            desc_elem = (
                soup.find(class_=re.compile(r'description|job-content|details', re.I)) or
                soup.find('article') or
                soup.find('main')
            )
            description = desc_elem.get_text(strip=True) if desc_elem else ''
            
            # Posted date
            date_elem = soup.find(class_=re.compile(r'posted|date|time', re.I))
            posted_date = self.parse_posted_date(
                date_elem.get_text(strip=True) if date_elem else ''
            )
            
            # Salary
            salary_elem = soup.find(class_=re.compile(r'salary|pay|compensation', re.I))
            salary_min, salary_max = self.parse_salary(
                salary_elem.get_text(strip=True) if salary_elem else ''
            )
            
            return {
                'job_id': self.generate_job_id(url),
                'source': 'fuzu',
                'source_url': url,
                'title': title,
                'company_name': company,
                'location': location,
                'country': 'Kenya',
                'description': description[:2000],  # Truncate long descriptions
                'salary_min': salary_min,
                'salary_max': salary_max,
                'salary_currency': 'KES',
                'posted_date': posted_date,
                'scraped_at': datetime.now().isoformat(),
                'experience_level': self.detect_experience_level(title, description),
                'employment_type': self.detect_employment_type(description),
                'skills': self.extract_skills(description),
                'is_active': True,
            }
            
        except Exception as e:
            logger.error(f"Error scraping job page {url}: {e}")
            return None
    
    def run(self, keywords: List[str] = None) -> List[Dict]:
        """Run the scraper"""
        keywords = keywords or SEARCH_KEYWORDS
        
        logger.info(f"🚀 Starting Fuzu scraper with {len(keywords)} keywords...")
        logger.info(f"   Keywords: {', '.join(keywords)}")
        
        all_jobs = []
        
        for keyword in keywords:
            logger.info(f"\n🔍 Searching for '{keyword}'...")
            jobs = self.scrape_job_list(keyword)
            all_jobs.extend(jobs)
            logger.info(f"   Found {len(jobs)} jobs for '{keyword}'")
            self.rate_limit()
        
        # Deduplicate by job_id
        unique_jobs = {}
        for job in all_jobs:
            if job['job_id'] not in unique_jobs:
                unique_jobs[job['job_id']] = job
        
        self.jobs_scraped = list(unique_jobs.values())
        
        logger.info(f"\n✅ Scraping complete!")
        logger.info(f"   Total unique jobs: {len(self.jobs_scraped)}")
        
        return self.jobs_scraped
    
    def save_results(self, filename: str = None) -> Path:
        """Save scraped jobs to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"fuzu_jobs_{timestamp}.json"
        
        filepath = OUTPUT_DIR / filename
        
        with open(filepath, 'w') as f:
            json.dump(self.jobs_scraped, f, indent=2, default=str)
        
        logger.info(f"💾 Saved {len(self.jobs_scraped)} jobs to {filepath}")
        
        # Also save as latest.json for easy access
        latest_path = OUTPUT_DIR / "fuzu_latest.json"
        with open(latest_path, 'w') as f:
            json.dump(self.jobs_scraped, f, indent=2, default=str)
        
        logger.info(f"💾 Also saved to {latest_path}")
        
        return filepath
    
    def generate_stats(self) -> Dict:
        """Generate statistics from scraped jobs"""
        if not self.jobs_scraped:
            return {}
        
        # Skill counts
        skill_counts = {}
        for job in self.jobs_scraped:
            for skill in job.get('skills', []):
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Company counts
        company_counts = {}
        for job in self.jobs_scraped:
            company = job.get('company_name', 'Unknown')
            company_counts[company] = company_counts.get(company, 0) + 1
        
        # Location counts
        location_counts = {}
        for job in self.jobs_scraped:
            location = job.get('location', 'Unknown')
            location_counts[location] = location_counts.get(location, 0) + 1
        
        stats = {
            'total_jobs': len(self.jobs_scraped),
            'scraped_at': datetime.now().isoformat(),
            'top_skills': sorted(skill_counts.items(), key=lambda x: -x[1])[:20],
            'top_companies': sorted(company_counts.items(), key=lambda x: -x[1])[:20],
            'locations': sorted(location_counts.items(), key=lambda x: -x[1]),
            'experience_levels': {},
            'employment_types': {},
        }
        
        for job in self.jobs_scraped:
            exp = job.get('experience_level', 'Unknown')
            stats['experience_levels'][exp] = stats['experience_levels'].get(exp, 0) + 1
            
            emp = job.get('employment_type', 'Unknown')
            stats['employment_types'][emp] = stats['employment_types'].get(emp, 0) + 1
        
        # Save stats
        stats_path = OUTPUT_DIR / "fuzu_stats.json"
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        
        logger.info(f"📊 Saved statistics to {stats_path}")
        
        return stats


def main():
    """Main entry point"""
    print("=" * 60)
    print("🎯 FUZU KENYA JOB SCRAPER")
    print("=" * 60)
    print()
    
    scraper = FuzuScraper()
    
    # Start with a few keywords to test
    test_keywords = ['data analyst', 'data scientist', 'analytics']
    
    jobs = scraper.run(keywords=test_keywords)
    
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
    else:
        print("\n⚠️ No jobs found. The website structure may have changed.")
        print("   Check the logs above for details.")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
