"""
Base scraper class with common functionality
"""
import time
import logging
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup

from ..config import SCRAPING_CONFIG
from ..database.connection import get_db
from ..database.models import Job, Company, ScrapingLog

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Base class for all job board scrapers
    """
    
    def __init__(self, source_name: str):
        self.source_name = source_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': SCRAPING_CONFIG['user_agent']
        })
        self.rate_limit_delay = SCRAPING_CONFIG['rate_limit_delay']
        self.timeout = SCRAPING_CONFIG['timeout']
        self.retry_times = SCRAPING_CONFIG['retry_times']
        
        self.jobs_scraped = 0
        self.jobs_new = 0
        self.jobs_updated = 0
        
    def generate_job_id(self, source: str, url: str) -> str:
        """Generate unique job ID from source and URL"""
        unique_string = f"{source}:{url}"
        return hashlib.md5(unique_string.encode()).hexdigest()
    
    def rate_limit(self):
        """Apply rate limiting between requests"""
        time.sleep(self.rate_limit_delay)
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch a page with retry logic
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        for attempt in range(self.retry_times):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return BeautifulSoup(response.content, 'html.parser')
            except requests.exceptions.RequestException as e:
                logger.warning(f"Attempt {attempt + 1}/{self.retry_times} failed for {url}: {e}")
                if attempt < self.retry_times - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All attempts failed for {url}")
                    return None
    
    def save_job(self, job_data: Dict) -> bool:
        """
        Save or update job in database
        
        Args:
            job_data: Dictionary with job information
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with get_db() as db:
                # Check if job exists
                existing_job = db.query(Job).filter_by(job_id=job_data['job_id']).first()
                
                if existing_job:
                    # Update existing job
                    for key, value in job_data.items():
                        setattr(existing_job, key, value)
                    existing_job.updated_at = datetime.utcnow()
                    self.jobs_updated += 1
                    logger.info(f"Updated job: {job_data['title']} at {job_data['company_name']}")
                else:
                    # Create new job
                    new_job = Job(**job_data)
                    db.add(new_job)
                    self.jobs_new += 1
                    logger.info(f"Added new job: {job_data['title']} at {job_data['company_name']}")
                
                db.commit()
                self.jobs_scraped += 1
                return True
                
        except Exception as e:
            logger.error(f"Error saving job: {e}")
            return False
    
    def get_or_create_company(self, company_name: str, **kwargs) -> Optional[int]:
        """
        Get existing company or create new one
        
        Args:
            company_name: Name of the company
            **kwargs: Additional company attributes
            
        Returns:
            Company ID or None if failed
        """
        try:
            with get_db() as db:
                company = db.query(Company).filter_by(name=company_name).first()
                
                if not company:
                    company = Company(name=company_name, **kwargs)
                    db.add(company)
                    db.commit()
                    logger.info(f"Created new company: {company_name}")
                
                return company.id
        except Exception as e:
            logger.error(f"Error getting/creating company: {e}")
            return None
    
    def log_scraping_run(self, status: str, error_message: Optional[str] = None):
        """
        Log scraping run to database
        
        Args:
            status: Status of the run (running, completed, failed)
            error_message: Error message if failed
        """
        try:
            with get_db() as db:
                log = ScrapingLog(
                    source=self.source_name,
                    started_at=self.start_time,
                    completed_at=datetime.utcnow() if status != 'running' else None,
                    status=status,
                    jobs_scraped=self.jobs_scraped,
                    jobs_new=self.jobs_new,
                    jobs_updated=self.jobs_updated,
                    error_message=error_message,
                )
                db.add(log)
                db.commit()
        except Exception as e:
            logger.error(f"Error logging scraping run: {e}")
    
    @abstractmethod
    def scrape_jobs(self, keywords: List[str], locations: List[str]) -> List[Dict]:
        """
        Scrape jobs from the source
        
        Args:
            keywords: List of keywords to search
            locations: List of locations to search
            
        Returns:
            List of job dictionaries
        """
        pass
    
    def run(self, keywords: List[str], locations: List[str]):
        """
        Run the scraper
        
        Args:
            keywords: List of keywords to search
            locations: List of locations to search
        """
        self.start_time = datetime.utcnow()
        self.log_scraping_run('running')
        
        try:
            logger.info(f"Starting {self.source_name} scraper")
            jobs = self.scrape_jobs(keywords, locations)
            
            logger.info(f"Scraped {len(jobs)} jobs from {self.source_name}")
            
            for job_data in jobs:
                self.save_job(job_data)
                self.rate_limit()
            
            self.log_scraping_run('completed')
            logger.info(f"Completed {self.source_name} scraper: {self.jobs_new} new, {self.jobs_updated} updated")
            
        except Exception as e:
            error_msg = f"Error in {self.source_name} scraper: {e}"
            logger.error(error_msg)
            self.log_scraping_run('failed', error_msg)
            raise


