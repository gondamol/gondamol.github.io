"""
Update Dashboard to Use Real + Demo Data

Combines scraped data (if available) with demo data for a rich dashboard.
"""
import json
from pathlib import Path
from datetime import datetime

# Directories
PROJECT_DIR = Path(__file__).parent.parent
SCRAPED_DIR = PROJECT_DIR / "data" / "scraped"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_scraped_data():
    """Load all scraped JSON files"""
    jobs = []
    
    if not SCRAPED_DIR.exists():
        print("No scraped directory found")
        return jobs
    
    # Load BrighterMonday data
    bm_file = SCRAPED_DIR / "brightermonday_latest.json"
    if bm_file.exists():
        with open(bm_file) as f:
            bm_jobs = json.load(f)
            print(f"Loaded {len(bm_jobs)} jobs from BrighterMonday")
            jobs.extend(bm_jobs)
    
    # Load Fuzu data if available
    fuzu_file = SCRAPED_DIR / "fuzu_latest.json"
    if fuzu_file.exists():
        with open(fuzu_file) as f:
            fuzu_jobs = json.load(f)
            print(f"Loaded {len(fuzu_jobs)} jobs from Fuzu")
            jobs.extend(fuzu_jobs)
    
    return jobs


def load_demo_data():
    """Load demo data"""
    demo_file = PROCESSED_DIR / "jobs.json"
    if demo_file.exists():
        with open(demo_file) as f:
            jobs = json.load(f)
            print(f"Loaded {len(jobs)} demo jobs")
            return jobs
    return []


def merge_and_save():
    """Merge scraped and demo data, prioritizing scraped"""
    scraped = load_scraped_data()
    demo = load_demo_data()
    
    # Mark demo jobs
    for job in demo:
        job['is_demo'] = True
    
    # Mark scraped jobs
    for job in scraped:
        job['is_demo'] = False
    
    # Combine - scraped first
    combined = scraped + demo
    
    # Save combined data
    with open(PROCESSED_DIR / "jobs.json", 'w') as f:
        json.dump(combined, f, indent=2)
    
    print(f"\nSaved {len(combined)} total jobs ({len(scraped)} real, {len(demo)} demo)")
    
    # Generate updated stats
    generate_stats(combined)
    
    return combined


def generate_stats(jobs):
    """Generate statistics from jobs"""
    skill_counts = {}
    company_counts = {}
    location_counts = {}
    source_counts = {}
    
    for job in jobs:
        # Skills
        for skill in job.get('skills', []):
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        
        # Company
        company = job.get('company_name', 'Unknown')
        company_counts[company] = company_counts.get(company, 0) + 1
        
        # Location
        location = job.get('location', 'Kenya')
        location_counts[location] = location_counts.get(location, 0) + 1
        
        # Source
        source = job.get('source', 'unknown')
        source_counts[source] = source_counts.get(source, 0) + 1
    
    # Convert to list format
    skill_stats = [
        {"name": k, "category": "Other", "job_count": v, "percentage": round(v/len(jobs)*100, 1)}
        for k, v in sorted(skill_counts.items(), key=lambda x: -x[1])
    ]
    
    company_stats = [
        {"company": k, "job_count": v}
        for k, v in sorted(company_counts.items(), key=lambda x: -x[1])
    ]
    
    location_stats = [
        {"location": k, "job_count": v}
        for k, v in sorted(location_counts.items(), key=lambda x: -x[1])
    ]
    
    source_stats = [
        {"source": k, "job_count": v}
        for k, v in source_counts.items()
    ]
    
    # Count real vs demo
    real_count = sum(1 for j in jobs if not j.get('is_demo', True))
    demo_count = sum(1 for j in jobs if j.get('is_demo', True))
    
    summary = {
        "total_jobs": len(jobs),
        "real_jobs": real_count,
        "demo_jobs": demo_count,
        "recent_jobs_7_days": len([j for j in jobs if 'posted_date' in j]),
        "avg_salary_min": 150000,  # Placeholder
        "avg_salary_max": 300000,  # Placeholder
        "total_companies": len(company_counts),
        "total_skills_tracked": len(skill_counts),
        "sources_count": len(source_counts),
        "generated_at": datetime.now().isoformat(),
    }
    
    # Save all stats
    with open(PROCESSED_DIR / "skill_stats.json", 'w') as f:
        json.dump(skill_stats, f, indent=2)
    
    with open(PROCESSED_DIR / "company_stats.json", 'w') as f:
        json.dump(company_stats, f, indent=2)
    
    with open(PROCESSED_DIR / "location_stats.json", 'w') as f:
        json.dump(location_stats, f, indent=2)
    
    with open(PROCESSED_DIR / "source_stats.json", 'w') as f:
        json.dump(source_stats, f, indent=2)
    
    with open(PROCESSED_DIR / "summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Updated statistics files")
    print(f"  - Real jobs: {real_count}")
    print(f"  - Demo jobs: {demo_count}")
    print(f"  - Companies: {len(company_counts)}")


if __name__ == "__main__":
    print("=" * 50)
    print("Merging Scraped + Demo Data")
    print("=" * 50)
    merge_and_save()
    print("=" * 50)
