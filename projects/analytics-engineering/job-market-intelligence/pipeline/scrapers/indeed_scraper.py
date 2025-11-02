"""
Indeed.com Job Scraper
Note: Indeed has a Publisher API - use that in production
This scraper is for demonstration purposes
"""
import re
from datetime import datetime, timedelta
from typing import List, Dict
from .base_scraper import BaseScraper
import logging

logger = logging.getLogger(__name__)


class IndeedScraper(BaseScraper):
    """Scraper for Indeed job board"""
    
    def __init__(self):
        super().__init__('indeed')
        self.base_url = 'https://ke.indeed.com'
    
    def parse_salary(self, salary_text: str) -> Dict:
        """Parse salary text to extract min/max and period"""
        if not salary_text:
            return {}
        
        # Extract numbers
        numbers = re.findall(r'[\d,]+', salary_text.replace(',', ''))
        numbers = [int(n) for n in numbers if n]
        
        # Determine period
        period = 'Monthly'
        if 'year' in salary_text.lower() or 'annual' in salary_text.lower():
            period = 'Yearly'
        elif 'hour' in salary_text.lower():
            period = 'Hourly'
        
        # Determine currency
        currency = 'KES'
        if '$' in salary_text or 'USD' in salary_text:
            currency = 'USD'
        
        result = {
            'salary_currency': currency,
            'salary_period': period,
        }
        
        if len(numbers) >= 2:
            result['salary_min'] = min(numbers)
            result['salary_max'] = max(numbers)
        elif len(numbers) == 1:
            result['salary_min'] = numbers[0]
            result['salary_max'] = numbers[0]
        
        return result
    
    def parse_posted_date(self, date_text: str) -> datetime:
        """Parse posted date text to datetime"""
        if not date_text:
            return datetime.utcnow()
        
        date_text = date_text.lower()
        now = datetime.utcnow()
        
        if 'just posted' in date_text or 'today' in date_text:
            return now
        elif 'yesterday' in date_text:
            return now - timedelta(days=1)
        else:
            # Extract number of days
            days_match = re.search(r'(\d+)\s*day', date_text)
            if days_match:
                days = int(days_match.group(1))
                return now - timedelta(days=days)
        
        return now
    
    def scrape_jobs(self, keywords: List[str], locations: List[str]) -> List[Dict]:
        """
        Scrape jobs from Indeed
        
        Note: In production, use Indeed Publisher API instead of scraping
        This is a demonstration of the scraping structure
        """
        jobs = []
        
        for keyword in keywords:
            for location in locations:
                logger.info(f"Scraping Indeed for '{keyword}' in '{location}'")
                
                # Construct search URL
                search_url = f"{self.base_url}/jobs"
                params = {
                    'q': keyword,
                    'l': location,
                }
                
                # Build URL with params
                url = f"{search_url}?q={params['q'].replace(' ', '+')}&l={params['l'].replace(' ', '+')}"
                
                soup = self.fetch_page(url)
                if not soup:
                    continue
                
                # Find job cards (Indeed's structure as of 2024)
                # Note: These selectors may need updates
                job_cards = soup.find_all('div', class_='job_seen_beacon') or \
                           soup.find_all('div', attrs={'data-jk': True})
                
                for card in job_cards:
                    try:
                        job_data = self.parse_job_card(card, location)
                        if job_data:
                            jobs.append(job_data)
                    except Exception as e:
                        logger.warning(f"Error parsing job card: {e}")
                        continue
                
                self.rate_limit()
        
        return jobs
    
    def parse_job_card(self, card, location: str) -> Dict:
        """Parse individual job card"""
        try:
            # Extract job ID
            job_key = card.get('data-jk') or card.get('id', '').replace('job_', '')
            if not job_key:
                return None
            
            # Job URL
            job_url = f"{self.base_url}/viewjob?jk={job_key}"
            
            # Title
            title_elem = card.find('h2', class_='jobTitle') or card.find('a', class_='jcs-JobTitle')
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown'
            
            # Company
            company_elem = card.find('span', class_='companyName')
            company_name = company_elem.get_text(strip=True) if company_elem else 'Unknown'
            
            # Location
            location_elem = card.find('div', class_='companyLocation')
            job_location = location_elem.get_text(strip=True) if location_elem else location
            
            # Salary
            salary_elem = card.find('div', class_='salary-snippet')
            salary_data = {}
            if salary_elem:
                salary_data = self.parse_salary(salary_elem.get_text(strip=True))
            
            # Description snippet
            description_elem = card.find('div', class_='job-snippet')
            description = description_elem.get_text(strip=True) if description_elem else ''
            
            # Posted date
            date_elem = card.find('span', class_='date')
            posted_date = self.parse_posted_date(
                date_elem.get_text(strip=True) if date_elem else ''
            )
            
            # Generate unique job ID
            job_id = self.generate_job_id('indeed', job_url)
            
            # Get or create company
            company_id = self.get_or_create_company(company_name)
            
            job_data = {
                'job_id': job_id,
                'source': 'indeed',
                'source_url': job_url,
                'title': title,
                'company_id': company_id,
                'company_name': company_name,
                'location': job_location,
                'country': 'Kenya' if location.lower() == 'kenya' else location,
                'description': description,
                'posted_date': posted_date,
                'is_active': True,
                **salary_data
            }
            
            return job_data
            
        except Exception as e:
            logger.error(f"Error parsing job card: {e}")
            return None


