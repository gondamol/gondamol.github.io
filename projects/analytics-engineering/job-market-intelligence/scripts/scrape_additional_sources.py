"""
Additional Job API Scrapers

More free job APIs to maximize data collection:
1. GitHub Jobs (if available)
2. Adzuna (with free tier)
3. CareerJet
4. SimplyHired
5. The Muse
6. Landing Jobs
7. Authentic Jobs
8. Himalayas (remote jobs)

Usage:
    python3 scripts/scrape_additional_sources.py
"""
import json
import re
import time
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "scraped"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Accept': 'application/json',
}

TARGET_SKILLS = [
    'Python', 'R', 'SQL', 'Excel', 'Power BI', 'Tableau',
    'PostgreSQL', 'MySQL', 'MongoDB', 'AWS', 'Azure', 'GCP',
    'Machine Learning', 'Statistics', 'Spark', 'Airflow',
    'Docker', 'Git', 'Looker', 'dbt', 'Snowflake', 'TensorFlow',
    'scikit-learn', 'Pandas', 'NumPy', 'Data Analysis', 'Analytics'
]


def extract_skills(text: str) -> List[str]:
    if not text:
        return []
    text_lower = text.lower()
    return [skill for skill in TARGET_SKILLS if skill.lower() in text_lower]


def detect_experience_level(title: str, description: str = "") -> str:
    text = f"{title} {description}".lower()
    if any(w in text for w in ['senior', 'sr.', 'lead', 'principal']):
        return 'Senior'
    elif any(w in text for w in ['junior', 'jr.', 'entry', 'graduate', 'intern']):
        return 'Entry'
    elif any(w in text for w in ['manager', 'director', 'vp']):
        return 'Manager'
    return 'Mid'


def generate_job_id(source: str, identifier: str) -> str:
    return hashlib.md5(f"{source}:{identifier}".encode()).hexdigest()[:16]


class HimalayasScraper:
    """Scrape from Himalayas.app - Remote jobs API (free)"""
    
    def __init__(self):
        self.api_url = "https://himalayas.app/jobs/api"
        self.name = "himalayas"
    
    def scrape(self) -> List[Dict]:
        """Fetch remote data jobs"""
        logger.info("🏔️ Fetching from Himalayas.app API...")
        
        try:
            params = {'limit': 100}
            response = requests.get(self.api_url, params=params, headers=HEADERS, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            jobs_data = data.get('jobs', [])
            
            logger.info(f"   Raw jobs: {len(jobs_data)}")
            
            # Filter for data jobs
            keywords = ['data', 'analyst', 'analytics', 'scientist', 'ml', 'machine learning', 'bi']
            filtered = []
            
            for job in jobs_data:
                title = job.get('title', '').lower()
                categories = ' '.join(job.get('categories', [])).lower()
                if any(kw in f"{title} {categories}" for kw in keywords):
                    filtered.append(self._parse_job(job))
            
            logger.info(f"   ✅ Found {len(filtered)} data/analytics jobs")
            return filtered
            
        except Exception as e:
            logger.error(f"   ❌ Himalayas error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        url = job.get('applicationLink') or job.get('url', '')
        description = job.get('description', '')
        
        return {
            'job_id': generate_job_id(self.name, str(job.get('id', ''))),
            'source': self.name,
            'source_url': url,
            'title': job.get('title', 'Unknown'),
            'company_name': job.get('companyName', 'Unknown'),
            'company_logo': job.get('companyLogo', ''),
            'location': job.get('location') or 'Remote',
            'country': 'Remote',
            'remote_type': 'Remote',
            'description': description[:2000] if description else '',
            'salary_min': job.get('minSalary'),
            'salary_max': job.get('maxSalary'),
            'salary_currency': 'USD',
            'employment_type': job.get('type', 'Full-time'),
            'experience_level': detect_experience_level(job.get('title', ''), description),
            'skills': extract_skills(f"{job.get('title', '')} {description}"),
            'posted_date': job.get('pubDate', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }


class TheMoseScraper:
    """Scrape from The Muse API (free)"""
    
    def __init__(self):
        self.api_url = "https://www.themuse.com/api/public/jobs"
        self.name = "themuse"
    
    def scrape(self, page: int = 1) -> List[Dict]:
        """Fetch data jobs from The Muse"""
        logger.info("🎭 Fetching from The Muse API...")
        
        try:
            params = {
                'category': 'Data Science',
                'page': page,
                'ascending': 'false'
            }
            response = requests.get(self.api_url, params=params, headers=HEADERS, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            jobs_data = data.get('results', [])
            
            logger.info(f"   Raw jobs: {len(jobs_data)}")
            
            jobs = [self._parse_job(job) for job in jobs_data]
            logger.info(f"   ✅ Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"   ❌ The Muse error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        company = job.get('company', {})
        locations = job.get('locations', [])
        location = locations[0].get('name', 'Unknown') if locations else 'Remote'
        
        return {
            'job_id': generate_job_id(self.name, str(job.get('id', ''))),
            'source': self.name,
            'source_url': job.get('refs', {}).get('landing_page', ''),
            'title': job.get('name', 'Unknown'),
            'company_name': company.get('name', 'Unknown'),
            'location': location,
            'country': 'International',
            'remote_type': 'Remote' if 'remote' in location.lower() else 'On-site',
            'description': job.get('contents', '')[:2000],
            'employment_type': 'Full-time',
            'experience_level': detect_experience_level(job.get('name', ''), job.get('contents', '')),
            'skills': extract_skills(f"{job.get('name', '')} {job.get('contents', '')}"),
            'posted_date': job.get('publication_date', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }


class LandingJobsScraper:
    """Scrape from Landing.jobs API (free, EU focused)"""
    
    def __init__(self):
        self.api_url = "https://landing.jobs/api/v1/jobs"
        self.name = "landingjobs"
    
    def scrape(self) -> List[Dict]:
        """Fetch data jobs from Landing.jobs"""
        logger.info("🛬 Fetching from Landing.jobs API...")
        
        try:
            params = {
                'category': 'data',
                'limit': 50
            }
            response = requests.get(self.api_url, params=params, headers=HEADERS, timeout=30)
            
            if response.status_code == 404:
                logger.warning("   Landing.jobs API endpoint changed - skipping")
                return []
            
            response.raise_for_status()
            
            data = response.json()
            jobs_data = data if isinstance(data, list) else data.get('jobs', [])
            
            logger.info(f"   ✅ Found {len(jobs_data)} jobs")
            return [self._parse_job(job) for job in jobs_data]
            
        except Exception as e:
            logger.error(f"   ❌ Landing.jobs error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        return {
            'job_id': generate_job_id(self.name, str(job.get('id', job.get('slug', '')))),
            'source': self.name,
            'source_url': job.get('url', ''),
            'title': job.get('title', 'Unknown'),
            'company_name': job.get('company_name', 'Unknown'),
            'location': job.get('location', 'Europe'),
            'country': job.get('country', 'EU'),
            'description': job.get('description', '')[:2000],
            'salary_min': job.get('salary_from'),
            'salary_max': job.get('salary_to'),
            'salary_currency': job.get('salary_currency', 'EUR'),
            'employment_type': job.get('type', 'Full-time'),
            'experience_level': detect_experience_level(job.get('title', '')),
            'skills': job.get('tags', []) if job.get('tags') else extract_skills(job.get('title', '')),
            'posted_date': job.get('created_at', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }


class WellFoundScraper:
    """Scrape from Wellfound (formerly AngelList) - startup jobs"""
    
    def __init__(self):
        self.api_url = "https://wellfound.com/api/jobs"
        self.name = "wellfound"
    
    def scrape(self) -> List[Dict]:
        """Try to fetch startup jobs"""
        logger.info("🚀 Trying Wellfound (AngelList)...")
        
        try:
            # Wellfound doesn't have a public API, so we try the jobs page
            response = requests.get(
                "https://wellfound.com/role/data-analyst",
                headers={**HEADERS, 'Accept': 'text/html'},
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("   Wellfound requires JS rendering")
            
            return []
            
        except Exception as e:
            logger.error(f"   ❌ Wellfound error: {e}")
            return []


class ReedsJobsScraper:
    """Scrape from Reed.co.uk API (free tier available)"""
    
    def __init__(self):
        self.api_url = "https://www.reed.co.uk/api/1.0/search"
        self.name = "reed"
    
    def scrape(self) -> List[Dict]:
        """Reed requires API key"""
        logger.info("📰 Reed.co.uk requires API registration - skipping")
        return []


class DevITJobsScraper:
    """Scrape from DevITJobs (free API)"""
    
    def __init__(self):
        self.api_url = "https://devitjobs.com/api/jobs"
        self.name = "devitjobs"
    
    def scrape(self) -> List[Dict]:
        """Fetch data/IT jobs"""
        logger.info("💻 Fetching from DevITJobs API...")
        
        try:
            response = requests.get(self.api_url, headers=HEADERS, timeout=30)
            
            if response.status_code != 200:
                logger.warning(f"   DevITJobs returned {response.status_code}")
                return []
            
            jobs_data = response.json()
            
            if not isinstance(jobs_data, list):
                jobs_data = jobs_data.get('jobs', [])
            
            logger.info(f"   Raw jobs: {len(jobs_data)}")
            
            # Filter for data jobs
            keywords = ['data', 'analyst', 'analytics', 'scientist', 'bi']
            filtered = []
            
            for job in jobs_data:
                title = job.get('title', '').lower()
                if any(kw in title for kw in keywords):
                    filtered.append(self._parse_job(job))
            
            logger.info(f"   ✅ Found {len(filtered)} data jobs")
            return filtered
            
        except Exception as e:
            logger.error(f"   ❌ DevITJobs error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        return {
            'job_id': generate_job_id(self.name, str(job.get('id', job.get('slug', '')))),
            'source': self.name,
            'source_url': job.get('url', ''),
            'title': job.get('title', 'Unknown'),
            'company_name': job.get('company', 'Unknown'),
            'location': job.get('location', 'Unknown'),
            'country': job.get('country', 'International'),
            'remote_type': 'Remote' if job.get('remote') else 'On-site',
            'description': job.get('description', '')[:2000],
            'salary_min': job.get('salaryMin'),
            'salary_max': job.get('salaryMax'),
            'salary_currency': job.get('currency', 'USD'),
            'employment_type': job.get('type', 'Full-time'),
            'experience_level': detect_experience_level(job.get('title', '')),
            'skills': job.get('skills', []) or extract_skills(job.get('title', '')),
            'posted_date': job.get('createdAt', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }


class WorkablePublicScraper:
    """Scrape from Workable public jobs API"""
    
    def __init__(self):
        self.name = "workable"
    
    def scrape(self) -> List[Dict]:
        """Workable doesn't have a public aggregated API"""
        logger.info("🔧 Workable requires specific company subdomains - skipping")
        return []


def scrape_additional_sources() -> List[Dict]:
    """Run all additional scrapers"""
    all_jobs = []
    
    # 1. Himalayas
    himalayas = HimalayasScraper()
    jobs = himalayas.scrape()
    all_jobs.extend(jobs)
    time.sleep(1)
    
    # 2. The Muse
    muse = TheMoseScraper()
    jobs = muse.scrape()
    all_jobs.extend(jobs)
    time.sleep(1)
    
    # 3. Landing Jobs
    landing = LandingJobsScraper()
    jobs = landing.scrape()
    all_jobs.extend(jobs)
    time.sleep(1)
    
    # 4. DevITJobs
    devit = DevITJobsScraper()
    jobs = devit.scrape()
    all_jobs.extend(jobs)
    
    # Remove duplicates
    unique = {}
    for job in all_jobs:
        unique[job['job_id']] = job
    
    logger.info(f"\n📊 Total from additional sources: {len(unique)}")
    return list(unique.values())


def save_results(jobs: List[Dict]) -> Path:
    """Save to JSON"""
    if not jobs:
        return None
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"additional_sources_{timestamp}.json"
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump(jobs, f, indent=2, default=str)
    
    logger.info(f"💾 Saved {len(jobs)} jobs to {filepath}")
    
    # Also save as latest
    latest = OUTPUT_DIR / "additional_sources_latest.json"
    with open(latest, 'w') as f:
        json.dump(jobs, f, indent=2, default=str)
    
    return filepath


def main():
    """Main entry point"""
    print("=" * 60)
    print("📡 ADDITIONAL JOB SOURCES SCRAPER")
    print("=" * 60)
    print("\nScraping from:")
    print("  • Himalayas.app (remote jobs)")
    print("  • The Muse (career platform)")
    print("  • Landing.jobs (EU tech)")
    print("  • DevITJobs (IT/Dev jobs)")
    print()
    
    jobs = scrape_additional_sources()
    
    if jobs:
        save_results(jobs)
        
        # Stats
        sources = {}
        for job in jobs:
            s = job['source']
            sources[s] = sources.get(s, 0) + 1
        
        print("\n" + "=" * 60)
        print("📊 SCRAPING SUMMARY")
        print("=" * 60)
        print(f"\nTotal Jobs: {len(jobs)}")
        print("\nBy Source:")
        for source, count in sources.items():
            print(f"  • {source}: {count}")
    else:
        print("\n⚠️ No jobs found from additional sources")
    
    print("\n" + "=" * 60)
    return jobs


if __name__ == "__main__":
    main()
