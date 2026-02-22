#!/usr/bin/env python3
"""
CLI script to run job scrapers
"""
import sys
import logging
import argparse
from pathlib import Path

# Add pipeline to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.config import JOB_BOARDS
from pipeline.scrapers.indeed_scraper import IndeedScraper
from pipeline.scrapers.fuzu_scraper import FuzuScraper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_scraper(source_name: str):
    """Run scraper for specific source"""
    if source_name not in JOB_BOARDS:
        logger.error(f"Unknown source: {source_name}")
        return False
    
    config = JOB_BOARDS[source_name]
    
    if not config['enabled']:
        logger.warning(f"Scraper for {source_name} is disabled")
        return False
    
    logger.info(f"Running scraper for {source_name}")
    
    try:
        # Initialize scraper
        if source_name == 'indeed':
            scraper = IndeedScraper()
        elif source_name == 'fuzu':
            scraper = FuzuScraper()
        else:
            logger.error(f"Scraper not implemented for {source_name}")
            return False
        
        # Run scraper
        scraper.run(
            keywords=config['keywords'],
            locations=config['locations']
        )
        
        logger.info(f"Completed {source_name} scraper successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error running {source_name} scraper: {e}")
        return False


def run_all_scrapers():
    """Run all enabled scrapers"""
    logger.info("Running all enabled scrapers")
    
    results = {}
    for source_name, config in JOB_BOARDS.items():
        if config['enabled']:
            success = run_scraper(source_name)
            results[source_name] = success
    
    # Summary
    logger.info("=" * 50)
    logger.info("Scraping Summary:")
    for source, success in results.items():
        status = "✓ Success" if success else "✗ Failed"
        logger.info(f"  {source}: {status}")
    logger.info("=" * 50)
    
    return all(results.values())


def main():
    parser = argparse.ArgumentParser(description='Run job scrapers')
    parser.add_argument(
        '--source',
        type=str,
        choices=list(JOB_BOARDS.keys()) + ['all'],
        default='all',
        help='Source to scrape (default: all)'
    )
    
    args = parser.parse_args()
    
    if args.source == 'all':
        success = run_all_scrapers()
    else:
        success = run_scraper(args.source)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()






