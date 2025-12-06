"""
Multi-Source Job Scraper for Kenya Data Analytics Jobs

Scrapes from multiple FREE job APIs and aggregators:
1. RemoteOK - Free API for remote tech jobs
2. Remotive - Free API for remote jobs  
3. Arbeitnow - Free job listings API
4. JobIcy - Remote jobs API
5. LinkedIn via browser automation (requires Selenium)

Usage:
    python3 scripts/scrape_all_sources.py
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

# Skills to detect
TARGET_SKILLS = [
    'Python', 'R', 'SQL', 'Excel', 'Power BI', 'Tableau',
    'PostgreSQL', 'MySQL', 'MongoDB', 'AWS', 'Azure', 'GCP',
    'Machine Learning', 'Statistics', 'Spark', 'Airflow',
    'Docker', 'Git', 'Looker', 'dbt', 'Snowflake', 'TensorFlow',
    'scikit-learn', 'Pandas', 'NumPy', 'Stata', 'SPSS',
    'Java', 'JavaScript', 'Scala', 'Hadoop', 'Kafka',
    'Data Analysis', 'Data Science', 'Analytics', 'ETL',
    'Business Intelligence', 'BI', 'Visualization', 'Dashboard'
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json',
}


def extract_skills(text: str) -> List[str]:
    """Extract skills from text"""
    if not text:
        return []
    text_lower = text.lower()
    return [skill for skill in TARGET_SKILLS if skill.lower() in text_lower]


def detect_experience_level(title: str, description: str = "") -> str:
    """Detect experience level"""
    text = f"{title} {description}".lower()
    if any(w in text for w in ['senior', 'sr.', 'lead', 'principal', 'staff', 'head']):
        return 'Senior'
    elif any(w in text for w in ['junior', 'jr.', 'entry', 'graduate', 'intern', 'trainee']):
        return 'Entry'
    elif any(w in text for w in ['manager', 'director', 'vp', 'chief']):
        return 'Manager'
    return 'Mid'


def generate_job_id(source: str, url: str) -> str:
    """Generate unique job ID"""
    return hashlib.md5(f"{source}:{url}".encode()).hexdigest()[:16]


class RemoteOKScraper:
    """Scrape from RemoteOK.com - Free API"""
    
    def __init__(self):
        self.api_url = "https://remoteok.com/api"
        self.name = "remoteok"
    
    def scrape(self, keywords: List[str] = None) -> List[Dict]:
        """Fetch jobs from RemoteOK API"""
        logger.info("🌐 Fetching from RemoteOK API...")
        
        try:
            response = requests.get(
                self.api_url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            # First item is usually metadata, skip it
            jobs_data = data[1:] if len(data) > 1 else data
            
            logger.info(f"   Raw jobs from API: {len(jobs_data)}")
            
            # Filter for data/analytics jobs
            keywords = keywords or ['data', 'analyst', 'analytics', 'scientist', 'machine learning', 'statistics', 'bi']
            filtered_jobs = []
            
            for job in jobs_data:
                title = job.get('position', '').lower()
                tags = ' '.join(job.get('tags', [])).lower()
                company = job.get('company', '').lower()
                description = job.get('description', '').lower()
                
                # Check if job matches our keywords
                combined = f"{title} {tags} {description}"
                if any(kw.lower() in combined for kw in keywords):
                    filtered_jobs.append(self._parse_job(job))
            
            logger.info(f"   ✅ Found {len(filtered_jobs)} data/analytics jobs")
            return filtered_jobs
            
        except Exception as e:
            logger.error(f"   ❌ RemoteOK error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        """Parse RemoteOK job data"""
        url = job.get('url', f"https://remoteok.com/remote-jobs/{job.get('id', '')}")
        description = job.get('description', '')
        title = job.get('position', 'Unknown Position')
        
        # Parse salary
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')
        
        return {
            'job_id': generate_job_id(self.name, url),
            'source': self.name,
            'source_url': url,
            'title': title,
            'company_name': job.get('company', 'Unknown'),
            'company_logo': job.get('company_logo', ''),
            'location': job.get('location', 'Remote'),
            'country': 'Remote',
            'remote_type': 'Remote',
            'description': description[:2000] if description else '',
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_currency': 'USD',
            'employment_type': 'Full-time',
            'experience_level': detect_experience_level(title, description),
            'skills': extract_skills(f"{title} {description} {' '.join(job.get('tags', []))}"),
            'tags': job.get('tags', []),
            'posted_date': job.get('date', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }


class RemotiveScraper:
    """Scrape from Remotive.com - Free API"""
    
    def __init__(self):
        self.api_url = "https://remotive.com/api/remote-jobs"
        self.name = "remotive"
    
    def scrape(self, category: str = "data") -> List[Dict]:
        """Fetch jobs from Remotive API"""
        logger.info("🌐 Fetching from Remotive API...")
        
        try:
            # Remotive has category-based filtering
            params = {'category': category, 'limit': 100}
            response = requests.get(
                self.api_url,
                params=params,
                headers=HEADERS,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            jobs_data = data.get('jobs', [])
            
            logger.info(f"   Raw jobs: {len(jobs_data)}")
            
            # Parse all jobs
            jobs = [self._parse_job(job) for job in jobs_data]
            logger.info(f"   ✅ Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"   ❌ Remotive error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        """Parse Remotive job data"""
        url = job.get('url', '')
        description = job.get('description', '')
        title = job.get('title', 'Unknown Position')
        
        # Parse salary from description if available
        salary_min, salary_max = self._parse_salary(job.get('salary', ''))
        
        return {
            'job_id': generate_job_id(self.name, url),
            'source': self.name,
            'source_url': url,
            'title': title,
            'company_name': job.get('company_name', 'Unknown'),
            'company_logo': job.get('company_logo_url', ''),
            'location': job.get('candidate_required_location', 'Remote'),
            'country': 'Remote',
            'remote_type': 'Remote',
            'description': description[:2000] if description else '',
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_currency': 'USD',
            'employment_type': job.get('job_type', 'Full-time'),
            'experience_level': detect_experience_level(title, description),
            'skills': extract_skills(f"{title} {description}"),
            'category': job.get('category', ''),
            'posted_date': job.get('publication_date', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }
    
    def _parse_salary(self, salary_str: str) -> tuple:
        """Parse salary string"""
        if not salary_str:
            return None, None
        # Try to extract numbers
        numbers = re.findall(r'\d+', salary_str.replace(',', ''))
        if len(numbers) >= 2:
            return int(numbers[0]) * 1000, int(numbers[1]) * 1000
        elif len(numbers) == 1:
            return int(numbers[0]) * 1000, int(numbers[0]) * 1000
        return None, None


class ArbeitnowScraper:
    """Scrape from Arbeitnow - Free job listings API"""
    
    def __init__(self):
        self.api_url = "https://www.arbeitnow.com/api/job-board-api"
        self.name = "arbeitnow"
    
    def scrape(self) -> List[Dict]:
        """Fetch jobs from Arbeitnow API"""
        logger.info("🌐 Fetching from Arbeitnow API...")
        
        try:
            response = requests.get(self.api_url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            jobs_data = data.get('data', [])
            
            logger.info(f"   Raw jobs: {len(jobs_data)}")
            
            # Filter for data/analytics jobs
            keywords = ['data', 'analyst', 'analytics', 'scientist', 'machine learning', 'bi', 'intelligence']
            filtered_jobs = []
            
            for job in jobs_data:
                title = job.get('title', '').lower()
                tags = ' '.join(job.get('tags', [])).lower()
                
                if any(kw in f"{title} {tags}" for kw in keywords):
                    filtered_jobs.append(self._parse_job(job))
            
            logger.info(f"   ✅ Found {len(filtered_jobs)} data/analytics jobs")
            return filtered_jobs
            
        except Exception as e:
            logger.error(f"   ❌ Arbeitnow error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        """Parse Arbeitnow job data"""
        url = job.get('url', '')
        description = job.get('description', '')
        title = job.get('title', 'Unknown Position')
        
        return {
            'job_id': generate_job_id(self.name, url),
            'source': self.name,
            'source_url': url,
            'title': title,
            'company_name': job.get('company_name', 'Unknown'),
            'location': job.get('location', 'Unknown'),
            'country': 'International',
            'remote_type': 'Remote' if job.get('remote', False) else 'On-site',
            'description': description[:2000] if description else '',
            'employment_type': 'Full-time',
            'experience_level': detect_experience_level(title, description),
            'skills': extract_skills(f"{title} {description} {' '.join(job.get('tags', []))}"),
            'tags': job.get('tags', []),
            'posted_date': job.get('created_at', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }


class JobicyScraper:
    """Scrape from Jobicy - Remote jobs"""
    
    def __init__(self):
        self.api_url = "https://jobicy.com/api/v2/remote-jobs"
        self.name = "jobicy"
    
    def scrape(self, category: str = "data-science") -> List[Dict]:
        """Fetch jobs from Jobicy API"""
        logger.info("🌐 Fetching from Jobicy API...")
        
        try:
            params = {'count': 50, 'industry': category}
            response = requests.get(
                self.api_url,
                params=params,
                headers=HEADERS,
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            jobs_data = data.get('jobs', [])
            
            logger.info(f"   Raw jobs: {len(jobs_data)}")
            
            jobs = [self._parse_job(job) for job in jobs_data]
            logger.info(f"   ✅ Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logger.error(f"   ❌ Jobicy error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        """Parse Jobicy job data"""
        url = job.get('url', '')
        description = job.get('jobDescription', '')
        title = job.get('jobTitle', 'Unknown Position')
        
        # Parse salary
        salary_min = job.get('annualSalaryMin')
        salary_max = job.get('annualSalaryMax')
        
        return {
            'job_id': generate_job_id(self.name, url),
            'source': self.name,
            'source_url': url,
            'title': title,
            'company_name': job.get('companyName', 'Unknown'),
            'company_logo': job.get('companyLogo', ''),
            'location': job.get('jobGeo', 'Remote'),
            'country': job.get('jobGeo', 'Remote'),
            'remote_type': 'Remote',
            'description': description[:2000] if description else '',
            'salary_min': salary_min,
            'salary_max': salary_max,
            'salary_currency': 'USD',
            'employment_type': job.get('jobType', 'Full-time'),
            'experience_level': job.get('jobLevel', detect_experience_level(title, description)),
            'skills': extract_skills(f"{title} {description}"),
            'industry': job.get('jobIndustry', []),
            'posted_date': job.get('pubDate', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }


class FindWorkScraper:
    """Scrape from FindWork.dev - Developer jobs API (free)"""
    
    def __init__(self):
        self.api_url = "https://findwork.dev/api/jobs/"
        self.name = "findwork"
    
    def scrape(self, search: str = "data") -> List[Dict]:
        """Fetch jobs from FindWork API"""
        logger.info("🌐 Fetching from FindWork.dev API...")
        
        try:
            params = {'search': search, 'sort_by': 'relevance'}
            response = requests.get(
                self.api_url,
                params=params,
                headers=HEADERS,
                timeout=30
            )
            
            if response.status_code == 401:
                logger.warning("   FindWork requires API key - skipping")
                return []
            
            response.raise_for_status()
            
            data = response.json()
            jobs_data = data.get('results', [])
            
            logger.info(f"   ✅ Found {len(jobs_data)} jobs")
            return [self._parse_job(job) for job in jobs_data]
            
        except Exception as e:
            logger.error(f"   ❌ FindWork error: {e}")
            return []
    
    def _parse_job(self, job: dict) -> Dict:
        """Parse FindWork job data"""
        url = job.get('url', '')
        description = job.get('text', '')
        title = job.get('role', 'Unknown Position')
        
        return {
            'job_id': generate_job_id(self.name, url),
            'source': self.name,
            'source_url': url,
            'title': title,
            'company_name': job.get('company_name', 'Unknown'),
            'company_logo': job.get('logo', ''),
            'location': job.get('location', 'Remote'),
            'country': job.get('country', 'Unknown'),
            'remote_type': 'Remote' if job.get('remote', False) else 'On-site',
            'description': description[:2000] if description else '',
            'employment_type': job.get('employment_type', 'Full-time'),
            'experience_level': detect_experience_level(title, description),
            'skills': job.get('keywords', []),
            'posted_date': job.get('date_posted', datetime.now().isoformat()),
            'scraped_at': datetime.now().isoformat(),
            'is_active': True,
        }


def scrape_all_sources() -> List[Dict]:
    """Run all scrapers and combine results"""
    all_jobs = []
    
    # 1. RemoteOK
    remoteok = RemoteOKScraper()
    jobs = remoteok.scrape()
    all_jobs.extend(jobs)
    time.sleep(1)
    
    # 2. Remotive
    remotive = RemotiveScraper()
    jobs = remotive.scrape(category='data')
    all_jobs.extend(jobs)
    time.sleep(1)
    
    # Also try software development category for data eng roles
    jobs = remotive.scrape(category='software-dev')
    for job in jobs:
        title = job.get('title', '').lower()
        if any(kw in title for kw in ['data', 'analyst', 'analytics', 'ml', 'machine learning']):
            all_jobs.append(job)
    time.sleep(1)
    
    # 3. Arbeitnow
    arbeitnow = ArbeitnowScraper()
    jobs = arbeitnow.scrape()
    all_jobs.extend(jobs)
    time.sleep(1)
    
    # 4. Jobicy
    jobicy = JobicyScraper()
    jobs = jobicy.scrape(category='data-science')
    all_jobs.extend(jobs)
    
    # Remove duplicates by job_id
    unique_jobs = {}
    for job in all_jobs:
        job_id = job.get('job_id', str(hash(job.get('source_url', ''))))
        if job_id not in unique_jobs:
            unique_jobs[job_id] = job
    
    final_jobs = list(unique_jobs.values())
    logger.info(f"\n📊 Total unique jobs collected: {len(final_jobs)}")
    
    return final_jobs


def save_results(jobs: List[Dict], filename: str = None):
    """Save jobs to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"all_sources_{timestamp}.json"
    
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump(jobs, f, indent=2, default=str)
    
    logger.info(f"💾 Saved {len(jobs)} jobs to {filepath}")
    
    # Also save as latest combined file
    latest = OUTPUT_DIR / "all_sources_latest.json"
    with open(latest, 'w') as f:
        json.dump(jobs, f, indent=2, default=str)
    
    return filepath


def generate_stats(jobs: List[Dict]) -> Dict:
    """Generate statistics from scraped jobs"""
    skill_counts = {}
    company_counts = {}
    source_counts = {}
    location_counts = {}
    exp_counts = {}
    
    for job in jobs:
        # Skills
        for skill in job.get('skills', []):
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Company
        company = job.get('company_name', 'Unknown')
        company_counts[company] = company_counts.get(company, 0) + 1
        
        # Source
        source = job.get('source', 'unknown')
        source_counts[source] = source_counts.get(source, 0) + 1
        
        # Location
        location = job.get('location', 'Unknown')[:30]  # Truncate long locations
        location_counts[location] = location_counts.get(location, 0) + 1
        
        # Experience
        exp = job.get('experience_level', 'Unknown')
        exp_counts[exp] = exp_counts.get(exp, 0) + 1
    
    stats = {
        'total_jobs': len(jobs),
        'scraped_at': datetime.now().isoformat(),
        'sources': source_counts,
        'top_skills': sorted(skill_counts.items(), key=lambda x: -x[1])[:20],
        'top_companies': sorted(company_counts.items(), key=lambda x: -x[1])[:20],
        'locations': sorted(location_counts.items(), key=lambda x: -x[1])[:15],
        'experience_levels': exp_counts,
    }
    
    # Save stats
    stats_path = OUTPUT_DIR / "all_sources_stats.json"
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2, default=str)
    
    return stats


def main():
    """Main entry point"""
    print("=" * 60)
    print("🚀 MULTI-SOURCE JOB SCRAPER")
    print("=" * 60)
    print("\nScraping from:")
    print("  • RemoteOK (free API)")
    print("  • Remotive (free API)")
    print("  • Arbeitnow (free API)")
    print("  • Jobicy (free API)")
    print()
    
    # Run all scrapers
    jobs = scrape_all_sources()
    
    if jobs:
        # Save results
        save_results(jobs)
        stats = generate_stats(jobs)
        
        print("\n" + "=" * 60)
        print("📊 SCRAPING SUMMARY")
        print("=" * 60)
        print(f"\nTotal Jobs: {stats['total_jobs']}")
        
        print(f"\nJobs by Source:")
        for source, count in stats['sources'].items():
            print(f"  • {source}: {count}")
        
        print(f"\nTop 10 Skills:")
        for skill, count in stats['top_skills'][:10]:
            print(f"  • {skill}: {count}")
        
        print(f"\nTop 10 Companies:")
        for company, count in stats['top_companies'][:10]:
            print(f"  • {company}: {count}")
        
        print(f"\nExperience Levels:")
        for level, count in stats['experience_levels'].items():
            print(f"  • {level}: {count}")
    else:
        print("\n⚠️ No jobs found from any source")
    
    print("\n" + "=" * 60)
    return jobs


if __name__ == "__main__":
    main()
