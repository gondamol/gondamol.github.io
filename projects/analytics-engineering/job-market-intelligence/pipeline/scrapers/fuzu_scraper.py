"""
Fuzu Kenya Job Scraper - Enhanced Version

Scrapes job postings from Fuzu.com (Kenya's leading job portal)
Handles pagination, detailed job pages, and robust error handling.
"""
import re
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlencode
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class FuzuScraper(BaseScraper):
    """
    Scraper for Fuzu Kenya job board (https://www.fuzu.com)
    
    Features:
    - Multi-keyword search
    - Pagination handling
    - Detailed job page scraping
    - Salary extraction
    - Experience level detection
    """
    
    def __init__(self):
        super().__init__('fuzu')
        self.base_url = 'https://www.fuzu.com'
        self.search_url = 'https://www.fuzu.com/kenya/jobs'
        self.max_pages = 5  # Limit pages per search
    
    def parse_posted_date(self, date_text: str) -> datetime:
        """Parse Fuzu's posted date text to datetime"""
        if not date_text:
            return datetime.utcnow()
        
        date_text = date_text.lower().strip()
        now = datetime.utcnow()
        
        # Handle "X hours ago"
        if 'hour' in date_text:
            match = re.search(r'(\d+)\s*hour', date_text)
            if match:
                return now - timedelta(hours=int(match.group(1)))
        
        # Handle "X days ago"
        elif 'day' in date_text:
            match = re.search(r'(\d+)\s*day', date_text)
            if match:
                return now - timedelta(days=int(match.group(1)))
        
        # Handle "X weeks ago"
        elif 'week' in date_text:
            match = re.search(r'(\d+)\s*week', date_text)
            if match:
                return now - timedelta(weeks=int(match.group(1)))
        
        # Handle "X months ago"
        elif 'month' in date_text:
            match = re.search(r'(\d+)\s*month', date_text)
            if match:
                return now - timedelta(days=int(match.group(1)) * 30)
        
        # Handle "today"
        elif 'today' in date_text:
            return now
        
        # Handle "yesterday"
        elif 'yesterday' in date_text:
            return now - timedelta(days=1)
        
        return now
    
    def parse_salary(self, text: str) -> tuple:
        """Extract salary range from text"""
        if not text:
            return None, None
        
        text = text.lower().replace(',', '')
        
        # Pattern: KES 100000 - 200000 or 100k - 200k
        patterns = [
            r'kes?\s*(\d+)k?\s*[-–to]\s*(\d+)k?',
            r'(\d+),?\d*\s*[-–to]\s*(\d+),?\d*',
            r'(\d+)k\s*[-–to]\s*(\d+)k',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                min_sal = int(match.group(1))
                max_sal = int(match.group(2))
                
                # Handle 'k' suffix
                if min_sal < 1000:
                    min_sal *= 1000
                if max_sal < 1000:
                    max_sal *= 1000
                
                return min_sal, max_sal
        
        return None, None
    
    def detect_experience_level(self, title: str, description: str) -> str:
        """Detect experience level from job title and description"""
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['senior', 'sr.', 'lead', 'principal', 'head of']):
            return 'Senior'
        elif any(word in text for word in ['junior', 'jr.', 'entry', 'graduate', 'intern']):
            return 'Entry'
        elif any(word in text for word in ['manager', 'director', 'vp', 'chief']):
            return 'Manager'
        elif any(word in text for word in ['mid', 'intermediate', '2-4 years', '3-5 years']):
            return 'Mid'
        
        return 'Mid'  # Default
    
    def detect_employment_type(self, text: str) -> str:
        """Detect employment type from job text"""
        text = text.lower()
        
        if 'contract' in text or 'fixed term' in text:
            return 'Contract'
        elif 'part-time' in text or 'part time' in text:
            return 'Part-time'
        elif 'intern' in text:
            return 'Internship'
        elif 'freelance' in text:
            return 'Freelance'
        
        return 'Full-time'  # Default
    
    def detect_remote_type(self, text: str) -> str:
        """Detect remote work type"""
        text = text.lower()
        
        if 'remote' in text and 'hybrid' not in text:
            return 'Remote'
        elif 'hybrid' in text:
            return 'Hybrid'
        
        return 'On-site'
    
    def build_search_url(self, keyword: str, page: int = 1) -> str:
        """Build search URL with parameters"""
        params = {
            'q': keyword,
            'page': page,
        }
        return f"{self.search_url}?{urlencode(params)}"
    
    def scrape_jobs(self, keywords: List[str], locations: List[str] = None) -> List[Dict]:
        """
        Scrape jobs from Fuzu Kenya
        
        Args:
            keywords: List of job search terms
            locations: List of locations (not heavily used by Fuzu - Kenya focused)
            
        Returns:
            List of job dictionaries
        """
        jobs = []
        seen_urls = set()
        
        for keyword in keywords:
            logger.info(f"🔍 Scraping Fuzu for '{keyword}'...")
            
            for page in range(1, self.max_pages + 1):
                url = self.build_search_url(keyword, page)
                logger.debug(f"Fetching page {page}: {url}")
                
                soup = self.fetch_page(url)
                if not soup:
                    logger.warning(f"Failed to fetch page {page} for '{keyword}'")
                    break
                
                # Find job listings - Fuzu uses various container classes
                job_cards = (
                    soup.find_all('div', {'class': re.compile(r'job-card|job-listing|job-item')}) or
                    soup.find_all('article', {'class': re.compile(r'job')}) or
                    soup.find_all('li', {'class': re.compile(r'job')}) or
                    soup.select('.jobs-list .job') or
                    soup.select('[data-job-id]')
                )
                
                if not job_cards:
                    logger.info(f"No more jobs found on page {page}")
                    break
                
                for card in job_cards:
                    try:
                        job_data = self.parse_job_card(card)
                        
                        if job_data and job_data['source_url'] not in seen_urls:
                            seen_urls.add(job_data['source_url'])
                            jobs.append(job_data)
                            logger.debug(f"Added: {job_data['title']} at {job_data['company_name']}")
                            
                    except Exception as e:
                        logger.warning(f"Error parsing job card: {e}")
                        continue
                
                # Rate limiting between pages
                self.rate_limit()
                
                # Check if there's a next page
                next_page = soup.find('a', {'rel': 'next'}) or soup.find('a', text=re.compile(r'next|→|»', re.I))
                if not next_page:
                    break
            
            logger.info(f"Found {len(jobs)} jobs so far for '{keyword}'")
        
        logger.info(f"✅ Total jobs scraped from Fuzu: {len(jobs)}")
        return jobs
    
    def parse_job_card(self, card) -> Optional[Dict]:
        """
        Parse individual job card from search results
        
        Args:
            card: BeautifulSoup element containing job info
            
        Returns:
            Dictionary with job data or None if parsing failed
        """
        try:
            # === Job URL ===
            link_elem = (
                card.find('a', {'href': re.compile(r'/jobs/|/job/')}) or
                card.find('a', {'class': re.compile(r'job-title|job-link')}) or
                card.find('h2', recursive=True) and card.find('h2').find('a') or
                card.find('a', href=True)
            )
            
            if not link_elem:
                return None
            
            job_path = link_elem.get('href', '')
            job_url = urljoin(self.base_url, job_path) if job_path else None
            
            if not job_url:
                return None
            
            # === Title ===
            title_elem = (
                card.find(['h2', 'h3', 'h4'], {'class': re.compile(r'title|name', re.I)}) or
                card.find('a', {'class': re.compile(r'title', re.I)}) or
                card.find(['h2', 'h3', 'h4']) or
                link_elem
            )
            title = title_elem.get_text(strip=True) if title_elem else 'Unknown Position'
            
            # === Company ===
            company_elem = (
                card.find(['span', 'div', 'a'], {'class': re.compile(r'company|employer|org', re.I)}) or
                card.find('span', {'itemprop': 'hiringOrganization'}) or
                card.find(['span', 'div'], text=re.compile(r'^[A-Z].*(?:Ltd|Inc|PLC|Limited|Corp|Kenya|Africa)', re.I))
            )
            company_name = company_elem.get_text(strip=True) if company_elem else 'Unknown Company'
            
            # === Location ===
            location_elem = (
                card.find(['span', 'div'], {'class': re.compile(r'location|place|city', re.I)}) or
                card.find('span', {'itemprop': 'jobLocation'}) or
                card.find(['span', 'div'], text=re.compile(r'nairobi|mombasa|kisumu|kenya', re.I))
            )
            location = location_elem.get_text(strip=True) if location_elem else 'Nairobi, Kenya'
            
            # === Description snippet ===
            desc_elem = (
                card.find(['div', 'p'], {'class': re.compile(r'desc|summary|excerpt|snippet', re.I)}) or
                card.find('p')
            )
            description = desc_elem.get_text(strip=True) if desc_elem else ''
            
            # === Posted Date ===
            date_elem = (
                card.find(['span', 'time', 'div'], {'class': re.compile(r'date|time|posted|ago', re.I)}) or
                card.find('time') or
                card.find(['span', 'div'], text=re.compile(r'\d+\s*(hour|day|week|month)s?\s*ago', re.I))
            )
            posted_date = self.parse_posted_date(
                date_elem.get_text(strip=True) if date_elem else ''
            )
            
            # === Salary (if available) ===
            salary_elem = card.find(['span', 'div'], {'class': re.compile(r'salary|pay|wage', re.I)})
            salary_min, salary_max = self.parse_salary(
                salary_elem.get_text(strip=True) if salary_elem else ''
            )
            
            # === Experience Level ===
            experience_level = self.detect_experience_level(title, description)
            
            # === Employment Type ===
            employment_type = self.detect_employment_type(f"{title} {description}")
            
            # === Remote Type ===
            remote_type = self.detect_remote_type(f"{location} {description}")
            
            # === Generate unique ID ===
            job_id = self.generate_job_id('fuzu', job_url)
            
            # === Get/create company ===
            company_id = self.get_or_create_company(company_name)
            
            return {
                'job_id': job_id,
                'source': 'fuzu',
                'source_url': job_url,
                'title': title,
                'company_id': company_id,
                'company_name': company_name,
                'location': location,
                'country': 'Kenya',
                'city': self._extract_city(location),
                'remote_type': remote_type,
                'description': description,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'salary_currency': 'KES',
                'salary_period': 'Monthly',
                'employment_type': employment_type,
                'experience_level': experience_level,
                'posted_date': posted_date,
                'is_active': True,
            }
            
        except Exception as e:
            logger.error(f"Error parsing job card: {e}")
            return None
    
    def _extract_city(self, location: str) -> str:
        """Extract city from location string"""
        if not location:
            return 'Nairobi'
        
        location_lower = location.lower()
        cities = ['nairobi', 'mombasa', 'kisumu', 'nakuru', 'eldoret', 'thika', 'malindi']
        
        for city in cities:
            if city in location_lower:
                return city.title()
        
        return 'Nairobi'
    
    def scrape_job_details(self, job_url: str) -> Optional[Dict]:
        """
        Scrape detailed information from individual job page
        
        Args:
            job_url: URL of the job posting
            
        Returns:
            Dictionary with additional job details
        """
        soup = self.fetch_page(job_url)
        if not soup:
            return None
        
        try:
            # Full description
            desc_elem = soup.find('div', {'class': re.compile(r'description|content|detail', re.I)})
            full_description = desc_elem.get_text(strip=True) if desc_elem else ''
            
            # Requirements
            req_elem = soup.find(['div', 'section'], text=re.compile(r'requirement|qualif', re.I))
            requirements = req_elem.get_text(strip=True) if req_elem else ''
            
            # Responsibilities
            resp_elem = soup.find(['div', 'section'], text=re.compile(r'responsib|duties', re.I))
            responsibilities = resp_elem.get_text(strip=True) if resp_elem else ''
            
            return {
                'description': full_description,
                'requirements': requirements,
                'responsibilities': responsibilities,
            }
            
        except Exception as e:
            logger.warning(f"Error scraping job details from {job_url}: {e}")
            return None


# CLI for testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    scraper = FuzuScraper()
    jobs = scraper.scrape_jobs(
        keywords=['data analyst', 'data scientist'],
        locations=['Kenya']
    )
    
    print(f"\n🎯 Found {len(jobs)} jobs")
    for job in jobs[:5]:
        print(f"  - {job['title']} at {job['company_name']} ({job['location']})")
