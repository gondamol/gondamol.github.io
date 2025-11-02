"""
Fuzu Kenya Job Scraper
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class FuzuScraper(BaseScraper):
    """Scraper for Fuzu Kenya job board"""
    
    def __init__(self):
        super().__init__('fuzu')
        self.base_url = 'https://www.fuzu.com'
    
    def parse_posted_date(self, date_text: str) -> datetime:
        """Parse posted date text to datetime"""
        if not date_text:
            return datetime.utcnow()
        
        date_text = date_text.lower()
        now = datetime.utcnow()
        
        if 'hour' in date_text:
            hours_match = re.search(r'(\d+)\s*hour', date_text)
            if hours_match:
                hours = int(hours_match.group(1))
                return now - timedelta(hours=hours)
        elif 'day' in date_text:
            days_match = re.search(r'(\d+)\s*day', date_text)
            if days_match:
                days = int(days_match.group(1))
                return now - timedelta(days=days)
        elif 'week' in date_text:
            weeks_match = re.search(r'(\d+)\s*week', date_text)
            if weeks_match:
                weeks = int(weeks_match.group(1))
                return now - timedelta(weeks=weeks)
        
        return now
    
    def scrape_jobs(self, keywords: List[str], locations: List[str]) -> List[Dict]:
        """Scrape jobs from Fuzu Kenya"""
        jobs = []
        
        for keyword in keywords:
            logger.info(f"Scraping Fuzu for '{keyword}'")
            
            # Construct search URL
            search_url = f"{self.base_url}/ke/jobs/search"
            params = {
                'query': keyword,
            }
            
            url = f"{search_url}?query={params['query'].replace(' ', '+')}"
            
            soup = self.fetch_page(url)
            if not soup:
                continue
            
            # Find job cards
            job_cards = soup.find_all('div', class_='job-card') or \
                       soup.find_all('div', class_='job-item') or \
                       soup.find_all('article', class_='job')
            
            for card in job_cards:
                try:
                    job_data = self.parse_job_card(card)
                    if job_data:
                        jobs.append(job_data)
                except Exception as e:
                    logger.warning(f"Error parsing job card: {e}")
                    continue
            
            self.rate_limit()
        
        return jobs
    
    def parse_job_card(self, card) -> Dict:
        """Parse individual job card"""
        try:
            # Job URL
            link_elem = card.find('a', href=True)
            if not link_elem:
                return None
            
            job_path = link_elem['href']
            if not job_path.startswith('http'):
                job_url = f"{self.base_url}{job_path}"
            else:
                job_url = job_path
            
            # Title
            title_elem = card.find('h2') or card.find('h3') or card.find('a', class_='job-title')
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown'
            
            # Company
            company_elem = card.find('span', class_='company-name') or \
                          card.find('div', class_='company')
            company_name = company_elem.get_text(strip=True) if company_elem else 'Unknown'
            
            # Location
            location_elem = card.find('span', class_='location') or \
                           card.find('div', class_='job-location')
            location = location_elem.get_text(strip=True) if location_elem else 'Kenya'
            
            # Description/snippet
            description_elem = card.find('div', class_='job-description') or \
                              card.find('p', class_='job-snippet')
            description = description_elem.get_text(strip=True) if description_elem else ''
            
            # Posted date
            date_elem = card.find('span', class_='posted-date') or \
                       card.find('time')
            posted_date = self.parse_posted_date(
                date_elem.get_text(strip=True) if date_elem else ''
            )
            
            # Generate unique job ID
            job_id = self.generate_job_id('fuzu', job_url)
            
            # Get or create company
            company_id = self.get_or_create_company(company_name)
            
            job_data = {
                'job_id': job_id,
                'source': 'fuzu',
                'source_url': job_url,
                'title': title,
                'company_id': company_id,
                'company_name': company_name,
                'location': location,
                'country': 'Kenya',
                'description': description,
                'posted_date': posted_date,
                'is_active': True,
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job card: {e}")
            return None


