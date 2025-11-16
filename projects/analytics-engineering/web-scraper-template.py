#!/usr/bin/env python3
"""
Web Scraper Template for Analytics Engineering Projects
This template provides a foundation for building production-ready web scrapers
that can be integrated into analytics engineering pipelines.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from datetime import datetime
from pathlib import Path
import json
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebScraperTemplate:
    """
    Base class for web scraping operations in analytics engineering projects.
    
    Features:
    - Rate limiting
    - Error handling
    - Data validation
    - JSON/CSV export
    - Logging
    """
    
    def __init__(self, 
                 base_url: str,
                 output_dir: str = "data",
                 delay: float = 1.0,
                 headers: Optional[Dict] = None):
        """
        Initialize the scraper.
        
        Args:
            base_url: Base URL to scrape from
            output_dir: Directory to save scraped data
            delay: Delay between requests (seconds)
            headers: HTTP headers to use
        """
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.delay = delay
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a webpage.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            time.sleep(self.delay)  # Rate limiting
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_data(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract data from parsed HTML.
        Override this method in subclasses.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of dictionaries containing extracted data
        """
        raise NotImplementedError("Subclasses must implement extract_data method")
    
    def validate_data(self, data: List[Dict]) -> List[Dict]:
        """
        Validate scraped data.
        
        Args:
            data: List of data dictionaries
            
        Returns:
            Validated data
        """
        if not data:
            logger.warning("No data extracted")
            return []
        
        # Remove entries with missing required fields
        validated = []
        for item in data:
            if all(v is not None for v in item.values()):
                validated.append(item)
        
        logger.info(f"Validated {len(validated)}/{len(data)} records")
        return validated
    
    def save_data(self, data: List[Dict], filename: str, format: str = 'json'):
        """
        Save scraped data to file.
        
        Args:
            data: Data to save
            filename: Output filename
            format: Output format ('json' or 'csv')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename}_{timestamp}.{format}"
        filepath = self.output_dir / filename
        
        if format == 'json':
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        elif format == 'csv':
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"Saved {len(data)} records to {filepath}")
        return filepath
    
    def run(self, urls: List[str]) -> List[Dict]:
        """
        Main scraping method.
        
        Args:
            urls: List of URLs to scrape
            
        Returns:
            List of extracted data dictionaries
        """
        all_data = []
        
        for url in urls:
            soup = self.fetch_page(url)
            if soup:
                data = self.extract_data(soup)
                all_data.extend(data)
        
        validated_data = self.validate_data(all_data)
        return validated_data


class ExampleScraper(WebScraperTemplate):
    """
    Example implementation for scraping job listings.
    """
    
    def extract_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract job listings from HTML."""
        jobs = []
        
        # Example: Extract job cards (adjust selectors based on target site)
        job_cards = soup.find_all('div', class_='job-card')  # Adjust selector
        
        for card in job_cards:
            try:
                job = {
                    'title': card.find('h2').text.strip() if card.find('h2') else None,
                    'company': card.find('span', class_='company').text.strip() if card.find('span', class_='company') else None,
                    'location': card.find('span', class_='location').text.strip() if card.find('span', class_='location') else None,
                    'salary': card.find('span', class_='salary').text.strip() if card.find('span', class_='salary') else None,
                    'url': card.find('a')['href'] if card.find('a') else None,
                    'scraped_at': datetime.now().isoformat()
                }
                jobs.append(job)
            except Exception as e:
                logger.error(f"Error extracting job data: {e}")
                continue
        
        return jobs


def main():
    """Example usage."""
    scraper = ExampleScraper(
        base_url="https://example.com/jobs",
        output_dir="data/jobs",
        delay=2.0
    )
    
    # Example URLs (replace with actual URLs)
    urls = [
        "https://example.com/jobs?page=1",
        "https://example.com/jobs?page=2",
    ]
    
    data = scraper.run(urls)
    scraper.save_data(data, "jobs", format='json')
    scraper.save_data(data, "jobs", format='csv')


if __name__ == "__main__":
    main()

