"""
Jumia Kenya Product Scraper
"""
import re
import logging
from datetime import datetime
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import hashlib

logger = logging.getLogger(__name__)


class JumiaScraper:
    """Scraper for Jumia Kenya"""
    
    def __init__(self):
        self.source = 'jumia'
        self.base_url = 'https://www.jumia.co.ke'
        self.driver = None
    
    def init_driver(self):
        """Initialize Selenium WebDriver"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
        
        try:
            self.driver = webdriver.Chrome(options=options)
            logger.info("WebDriver initialized")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def close_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            logger.info("WebDriver closed")
    
    def generate_product_id(self, url: str) -> str:
        """Generate unique product ID from URL"""
        return hashlib.md5(f"jumia:{url}".encode()).hexdigest()
    
    def parse_price(self, price_text: str) -> float:
        """Parse price text to float"""
        if not price_text:
            return None
        
        # Remove currency symbols and commas
        price_clean = re.sub(r'[^\d.]', '', price_text.replace(',', ''))
        
        try:
            return float(price_clean)
        except ValueError:
            return None
    
    def scrape_category(self, category_url: str, max_pages: int = 3) -> List[Dict]:
        """Scrape products from category"""
        products = []
        
        for page in range(1, max_pages + 1):
            url = f"{category_url}?page={page}"
            logger.info(f"Scraping: {url}")
            
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "prd"))
                )
                
                # Find product cards
                product_cards = self.driver.find_elements(By.CLASS_NAME, "prd")
                
                for card in product_cards:
                    try:
                        product_data = self.parse_product_card(card)
                        if product_data:
                            products.append(product_data)
                    except Exception as e:
                        logger.warning(f"Error parsing product card: {e}")
                        continue
                
                logger.info(f"Scraped {len(product_cards)} products from page {page}")
                
            except TimeoutException:
                logger.warning(f"Timeout loading page {page}")
                break
            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                break
        
        return products
    
    def parse_product_card(self, card) -> Dict:
        """Parse individual product card"""
        try:
            # Product name
            name_elem = card.find_element(By.CLASS_NAME, "name")
            name = name_elem.text.strip() if name_elem else None
            
            # Product URL
            link_elem = card.find_element(By.TAG_NAME, "a")
            product_url = link_elem.get_attribute('href') if link_elem else None
            
            if not name or not product_url:
                return None
            
            # Price
            price_elem = card.find_element(By.CLASS_NAME, "prc")
            price_text = price_elem.text.strip() if price_elem else None
            current_price = self.parse_price(price_text)
            
            # Old price (if on sale)
            old_price = None
            try:
                old_price_elem = card.find_element(By.CLASS_NAME, "old")
                old_price_text = old_price_elem.text.strip()
                old_price = self.parse_price(old_price_text)
            except:
                pass
            
            # Discount
            discount_percent = None
            if old_price and current_price:
                discount_percent = round(((old_price - current_price) / old_price) * 100, 2)
            
            # Rating
            rating = None
            try:
                rating_elem = card.find_element(By.CLASS_NAME, "stars")
                rating_text = rating_elem.get_attribute('data-rating')
                rating = float(rating_text) if rating_text else None
            except:
                pass
            
            # Review count
            review_count = 0
            try:
                review_elem = card.find_element(By.CLASS_NAME, "rev")
                review_text = review_elem.text.strip()
                review_match = re.search(r'(\d+)', review_text)
                if review_match:
                    review_count = int(review_match.group(1))
            except:
                pass
            
            # Image
            image_url = None
            try:
                img_elem = card.find_element(By.TAG_NAME, "img")
                image_url = img_elem.get_attribute('data-src') or img_elem.get_attribute('src')
            except:
                pass
            
            # Generate product ID
            product_id = self.generate_product_id(product_url)
            
            product_data = {
                'product_id': product_id,
                'source': 'jumia',
                'name': name,
                'url': product_url,
                'current_price': current_price,
                'old_price': old_price,
                'discount_percent': discount_percent,
                'currency': 'KES',
                'rating': rating,
                'review_count': review_count,
                'image_url': image_url,
                'in_stock': True,  # Assume in stock if listed
                'scraped_at': datetime.utcnow(),
            }
            
            return product_data
            
        except Exception as e:
            logger.error(f"Error parsing product card: {e}")
            return None
    
    def run(self, categories: List[str] = None):
        """Run scraper for specified categories"""
        if not categories:
            categories = ['electronics', 'phones-tablets', 'computing']
        
        self.init_driver()
        
        try:
            all_products = []
            
            for category in categories:
                category_url = f"{self.base_url}/{category}/"
                logger.info(f"Scraping category: {category}")
                
                products = self.scrape_category(category_url)
                all_products.extend(products)
            
            logger.info(f"Total products scraped: {len(all_products)}")
            return all_products
            
        finally:
            self.close_driver()






