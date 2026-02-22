#!/usr/bin/env python3
"""
Master Job Scraper - Runs All Available Scrapers

This script combines all scrapers to maximize job data collection:
1. RemoteOK, Remotive, Arbeitnow, Jobicy (free APIs)
2. Himalayas, The Muse (additional APIs)
3. BrighterMonday (Kenya-specific)
4. LinkedIn (optional, requires Selenium)

Usage:
    python3 scripts/run_all_scrapers.py
    python3 scripts/run_all_scrapers.py --with-linkedin  # Include LinkedIn
    
Schedule with cron (every 6 hours):
    0 */6 * * * cd /path/to/job-market-intelligence && ./venv/bin/python3 scripts/run_all_scrapers.py >> logs/scraper.log 2>&1

Author: Nicodemus Werre
"""
import json
import sys
import argparse
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# Setup paths
PROJECT_DIR = Path(__file__).parent.parent
SCRAPED_DIR = PROJECT_DIR / "data" / "scraped"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
LOGS_DIR = PROJECT_DIR / "logs"

# Create directories
SCRAPED_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
log_file = LOGS_DIR / f"scraper_{datetime.now().strftime('%Y%m%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_existing_jobs() -> Dict[str, Dict]:
    """Load existing jobs to avoid duplicates"""
    existing = {}
    
    jobs_file = PROCESSED_DIR / "jobs.json"
    if jobs_file.exists():
        try:
            with open(jobs_file) as f:
                jobs = json.load(f)
                for job in jobs:
                    existing[job.get('job_id', '')] = job
        except:
            pass
    
    return existing


def run_main_scrapers() -> List[Dict]:
    """Run main API scrapers"""
    logger.info("=" * 60)
    logger.info("RUNNING MAIN API SCRAPERS")
    logger.info("=" * 60)
    
    try:
        # Import the main scraper
        sys.path.insert(0, str(PROJECT_DIR / "scripts"))
        from scrape_all_sources import scrape_all_sources
        
        jobs = scrape_all_sources()
        logger.info(f"Main scrapers returned {len(jobs)} jobs")
        return jobs
        
    except Exception as e:
        logger.error(f"Main scrapers failed: {e}")
        return []


def run_additional_scrapers() -> List[Dict]:
    """Run additional API scrapers"""
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING ADDITIONAL SCRAPERS")
    logger.info("=" * 60)
    
    try:
        sys.path.insert(0, str(PROJECT_DIR / "scripts"))
        from scrape_additional_sources import scrape_additional_sources
        
        jobs = scrape_additional_sources()
        logger.info(f"Additional scrapers returned {len(jobs)} jobs")
        return jobs
        
    except Exception as e:
        logger.error(f"Additional scrapers failed: {e}")
        return []


def run_brightermonday_scraper() -> List[Dict]:
    """Run BrighterMonday scraper"""
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING BRIGHTERMONDAY SCRAPER")
    logger.info("=" * 60)
    
    try:
        sys.path.insert(0, str(PROJECT_DIR / "scripts"))
        from scrape_brightermonday import BrighterMondayScraper
        
        scraper = BrighterMondayScraper()
        jobs = scraper.run(
            keywords=['data-analyst', 'analytics', 'software-data'],
            fetch_details=False
        )
        logger.info(f"BrighterMonday returned {len(jobs)} jobs")
        return jobs
        
    except Exception as e:
        logger.error(f"BrighterMonday scraper failed: {e}")
        return []


def run_linkedin_scraper() -> List[Dict]:
    """Run LinkedIn scraper (Selenium)"""
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING LINKEDIN SCRAPER (Selenium)")
    logger.info("=" * 60)
    
    try:
        sys.path.insert(0, str(PROJECT_DIR / "scripts"))
        from scrape_linkedin import LinkedInScraper, SELENIUM_AVAILABLE
        
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available - skipping LinkedIn")
            return []
        
        scraper = LinkedInScraper()
        jobs = scraper.run([
            'data analyst remote',
            'data scientist remote'
        ])
        
        if jobs:
            scraper.save_results(jobs)
        
        logger.info(f"LinkedIn returned {len(jobs)} jobs")
        return jobs
        
    except Exception as e:
        logger.error(f"LinkedIn scraper failed: {e}")
        return []


def merge_all_jobs(new_jobs: List[Dict], existing: Dict[str, Dict]) -> List[Dict]:
    """Merge new jobs with existing, avoiding duplicates"""
    merged = existing.copy()
    
    new_count = 0
    for job in new_jobs:
        job_id = job.get('job_id', '')
        if job_id and job_id not in merged:
            merged[job_id] = job
            new_count += 1
    
    logger.info(f"Added {new_count} new jobs (total: {len(merged)})")
    return list(merged.values())


def calculate_stats(jobs: List[Dict]) -> Dict:
    """Calculate statistics for dashboard"""
    skill_counts = {}
    company_counts = {}
    location_counts = {}
    source_counts = {}
    
    for job in jobs:
        # Skills
        for skill in job.get('skills', []):
            if isinstance(skill, str) and len(skill) > 1:
                skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Company
        company = job.get('company_name', 'Unknown')
        if company and company != 'Unknown':
            company_counts[company] = company_counts.get(company, 0) + 1
        
        # Location
        location = str(job.get('location', 'Unknown'))[:40]
        location_counts[location] = location_counts.get(location, 0) + 1
        
        # Source
        source = job.get('source', 'unknown')
        source_counts[source] = source_counts.get(source, 0) + 1
    
    # Format for dashboard
    skill_stats = []
    for name, count in sorted(skill_counts.items(), key=lambda x: -x[1])[:30]:
        category = 'Other'
        if name in ['Python', 'R', 'SQL', 'Java', 'JavaScript', 'Scala']:
            category = 'Programming'
        elif name in ['AWS', 'Azure', 'GCP', 'Snowflake']:
            category = 'Cloud'
        elif name in ['Machine Learning', 'TensorFlow', 'scikit-learn']:
            category = 'ML/AI'
        elif name in ['Power BI', 'Tableau', 'Looker', 'Dashboard', 'BI']:
            category = 'BI Tool'
        
        skill_stats.append({
            'name': name,
            'category': category,
            'job_count': count,
            'percentage': round(count / len(jobs) * 100, 1) if jobs else 0
        })
    
    company_stats = [{'company': k, 'job_count': v} 
                     for k, v in sorted(company_counts.items(), key=lambda x: -x[1])[:25]]
    
    location_stats = [{'location': k, 'job_count': v}
                      for k, v in sorted(location_counts.items(), key=lambda x: -x[1])[:15]]
    
    source_stats = [{'source': k, 'job_count': v} for k, v in source_counts.items()]
    
    # Salary averages
    sal_min = [j.get('salary_min') for j in jobs if j.get('salary_min')]
    sal_max = [j.get('salary_max') for j in jobs if j.get('salary_max')]
    
    summary = {
        'total_jobs': len(jobs),
        'real_jobs': len(jobs),
        'demo_jobs': 0,
        'recent_jobs_7_days': len(jobs),
        'avg_salary_min': int(sum(sal_min) / len(sal_min)) if sal_min else 0,
        'avg_salary_max': int(sum(sal_max) / len(sal_max)) if sal_max else 0,
        'total_companies': len(company_counts),
        'total_skills_tracked': len(skill_counts),
        'sources_count': len(source_counts),
        'generated_at': datetime.now().isoformat(),
    }
    
    return {
        'skill_stats': skill_stats,
        'company_stats': company_stats,
        'location_stats': location_stats,
        'source_stats': source_stats,
        'summary': summary
    }


def save_all_data(jobs: List[Dict], stats: Dict):
    """Save all data files for dashboard"""
    # Jobs
    with open(PROCESSED_DIR / "jobs.json", 'w') as f:
        json.dump(jobs, f, indent=2, default=str)
    
    # Skills
    with open(PROCESSED_DIR / "skill_stats.json", 'w') as f:
        json.dump(stats['skill_stats'], f, indent=2)
    
    # Companies
    with open(PROCESSED_DIR / "company_stats.json", 'w') as f:
        json.dump(stats['company_stats'], f, indent=2)
    
    # Locations
    with open(PROCESSED_DIR / "location_stats.json", 'w') as f:
        json.dump(stats['location_stats'], f, indent=2)
    
    # Sources
    with open(PROCESSED_DIR / "source_stats.json", 'w') as f:
        json.dump(stats['source_stats'], f, indent=2)
    
    # Summary
    with open(PROCESSED_DIR / "summary.json", 'w') as f:
        json.dump(stats['summary'], f, indent=2)
    
    # Also save master lists
    with open(PROCESSED_DIR / "companies.json", 'w') as f:
        companies = [{'id': i+1, 'name': s['company']} 
                     for i, s in enumerate(stats['company_stats'])]
        json.dump(companies, f, indent=2)
    
    with open(PROCESSED_DIR / "skills.json", 'w') as f:
        skills = [{'id': i+1, 'name': s['name'], 'category': s['category']}
                  for i, s in enumerate(stats['skill_stats'])]
        json.dump(skills, f, indent=2)
    
    logger.info(f"💾 Saved all data files to {PROCESSED_DIR}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Run all job scrapers')
    parser.add_argument('--with-linkedin', action='store_true',
                        help='Include LinkedIn scraper (requires Selenium)')
    parser.add_argument('--quick', action='store_true',
                        help='Quick mode - only main scrapers')
    args = parser.parse_args()
    
    start_time = datetime.now()
    
    print("\n" + "=" * 70)
    print("🚀 MASTER JOB SCRAPER - COLLECTING REAL DATA")
    print("=" * 70)
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load existing jobs
    existing_jobs = load_existing_jobs()
    logger.info(f"Loaded {len(existing_jobs)} existing jobs")
    
    # Collect all new jobs
    all_new_jobs = []
    
    # 1. Main scrapers (RemoteOK, Remotive, Arbeitnow, Jobicy)
    jobs = run_main_scrapers()
    all_new_jobs.extend(jobs)
    
    if not args.quick:
        # 2. Additional scrapers (Himalayas, The Muse)
        jobs = run_additional_scrapers()
        all_new_jobs.extend(jobs)
        
        # 3. BrighterMonday (Kenya)
        jobs = run_brightermonday_scraper()
        all_new_jobs.extend(jobs)
    
    # 4. LinkedIn (optional)
    if args.with_linkedin:
        jobs = run_linkedin_scraper()
        all_new_jobs.extend(jobs)
    
    # Merge with existing
    logger.info("\n" + "=" * 60)
    logger.info("MERGING AND SAVING DATA")
    logger.info("=" * 60)
    
    all_jobs = merge_all_jobs(all_new_jobs, existing_jobs)
    
    # Calculate stats
    stats = calculate_stats(all_jobs)
    
    # Save everything
    save_all_data(all_jobs, stats)
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).seconds
    
    print("\n" + "=" * 70)
    print("📊 FINAL SUMMARY")
    print("=" * 70)
    print(f"\n✅ Scraping complete!")
    print(f"   Duration: {duration} seconds")
    print(f"   Total jobs: {stats['summary']['total_jobs']}")
    print(f"   Companies: {stats['summary']['total_companies']}")
    print(f"   Skills tracked: {stats['summary']['total_skills_tracked']}")
    print(f"   Sources: {stats['summary']['sources_count']}")
    
    print("\nJobs by Source:")
    for source in stats['source_stats']:
        print(f"   • {source['source']}: {source['job_count']}")
    
    print(f"\n💾 Data saved to: {PROCESSED_DIR}")
    print(f"📝 Log saved to: {log_file}")
    print("\n" + "=" * 70)
    
    return all_jobs


if __name__ == "__main__":
    main()
