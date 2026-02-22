"""
Update Dashboard Data with Real Scraped Jobs Only

Combines all scraped data and updates the processed directory for the dashboard.
NO demo data - only real scraped jobs.
"""
import json
from pathlib import Path
from datetime import datetime

# Directories
PROJECT_DIR = Path(__file__).parent.parent
SCRAPED_DIR = PROJECT_DIR / "data" / "scraped"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_all_scraped_data():
    """Load all scraped JSON files"""
    jobs = []
    
    if not SCRAPED_DIR.exists():
        print("No scraped directory found")
        return jobs
    
    # Load multi-source data (priority)
    all_sources = SCRAPED_DIR / "all_sources_latest.json"
    if all_sources.exists():
        with open(all_sources) as f:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} jobs from all_sources_latest.json")
            jobs.extend(data)
    
    # Load additional sources
    additional = SCRAPED_DIR / "additional_sources_latest.json"
    if additional.exists():
        with open(additional) as f:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} jobs from additional_sources")
            jobs.extend(data)
    
    # Load LinkedIn data
    linkedin = SCRAPED_DIR / "linkedin_latest.json"
    if linkedin.exists():
        with open(linkedin) as f:
            data = json.load(f)
            print(f"✅ Loaded {len(data)} jobs from LinkedIn")
            jobs.extend(data)
    
    # Load BrighterMonday data
    bm_file = SCRAPED_DIR / "brightermonday_latest.json"
    if bm_file.exists():
        with open(bm_file) as f:
            bm_jobs = json.load(f)
            print(f"✅ Loaded {len(bm_jobs)} jobs from BrighterMonday")
            jobs.extend(bm_jobs)
    
    # Load Fuzu data if available
    fuzu_file = SCRAPED_DIR / "fuzu_latest.json"
    if fuzu_file.exists():
        with open(fuzu_file) as f:
            fuzu_jobs = json.load(f)
            print(f"✅ Loaded {len(fuzu_jobs)} jobs from Fuzu")
            jobs.extend(fuzu_jobs)
    
    return jobs


def deduplicate_jobs(jobs):
    """Remove duplicate jobs by job_id"""
    seen = {}
    for job in jobs:
        job_id = job.get('job_id', str(hash(str(job))))
        if job_id not in seen:
            seen[job_id] = job
    return list(seen.values())


def generate_stats(jobs):
    """Generate statistics from jobs for dashboard"""
    skill_counts = {}
    company_counts = {}
    location_counts = {}
    source_counts = {}
    exp_counts = {}
    
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
        location = job.get('location', 'Unknown')[:40]  # Truncate
        location_counts[location] = location_counts.get(location, 0) + 1
        
        # Source
        source = job.get('source', 'unknown')
        source_counts[source] = source_counts.get(source, 0) + 1
        
        # Experience
        exp = job.get('experience_level', 'Unknown')
        exp_counts[exp] = exp_counts.get(exp, 0) + 1
    
    # Skill stats format for dashboard
    skill_stats = []
    for name, count in sorted(skill_counts.items(), key=lambda x: -x[1])[:30]:
        # Determine category
        category = 'Other'
        if name in ['Python', 'R', 'SQL', 'Java', 'JavaScript', 'Scala']:
            category = 'Programming'
        elif name in ['AWS', 'Azure', 'GCP', 'Snowflake']:
            category = 'Cloud'
        elif name in ['Machine Learning', 'TensorFlow', 'scikit-learn']:
            category = 'ML/AI'
        elif name in ['Power BI', 'Tableau', 'Looker', 'Dashboard', 'BI']:
            category = 'BI Tool'
        elif name in ['PostgreSQL', 'MySQL', 'MongoDB']:
            category = 'Database'
        elif name in ['Statistics', 'Analytics', 'Data Analysis']:
            category = 'Analytics'
        
        skill_stats.append({
            'name': name,
            'category': category,
            'job_count': count,
            'percentage': round(count / len(jobs) * 100, 1) if jobs else 0
        })
    
    # Company stats
    company_stats = [
        {'company': k, 'job_count': v}
        for k, v in sorted(company_counts.items(), key=lambda x: -x[1])[:25]
    ]
    
    # Location stats
    location_stats = [
        {'location': k, 'job_count': v}
        for k, v in sorted(location_counts.items(), key=lambda x: -x[1])[:15]
    ]
    
    # Source stats
    source_stats = [
        {'source': k, 'job_count': v}
        for k, v in source_counts.items()
    ]
    
    # Calculate salary averages
    salaries_min = [j.get('salary_min') for j in jobs if j.get('salary_min')]
    salaries_max = [j.get('salary_max') for j in jobs if j.get('salary_max')]
    
    avg_min = sum(salaries_min) / len(salaries_min) if salaries_min else 0
    avg_max = sum(salaries_max) / len(salaries_max) if salaries_max else 0
    
    # Summary
    summary = {
        'total_jobs': len(jobs),
        'real_jobs': len(jobs),
        'demo_jobs': 0,
        'recent_jobs_7_days': len(jobs),  # All are recent since just scraped
        'avg_salary_min': int(avg_min),
        'avg_salary_max': int(avg_max),
        'total_companies': len(company_counts),
        'total_skills_tracked': len(skill_counts),
        'sources_count': len(source_counts),
        'generated_at': datetime.now().isoformat(),
    }
    
    return skill_stats, company_stats, location_stats, source_stats, summary


def save_for_dashboard(jobs, skill_stats, company_stats, location_stats, source_stats, summary):
    """Save all data in format expected by dashboard"""
    
    # Save jobs
    with open(PROCESSED_DIR / "jobs.json", 'w') as f:
        json.dump(jobs, f, indent=2)
    print(f"💾 Saved {len(jobs)} jobs to jobs.json")
    
    # Save skill stats
    with open(PROCESSED_DIR / "skill_stats.json", 'w') as f:
        json.dump(skill_stats, f, indent=2)
    print(f"💾 Saved {len(skill_stats)} skill stats")
    
    # Save company stats
    with open(PROCESSED_DIR / "company_stats.json", 'w') as f:
        json.dump(company_stats, f, indent=2)
    print(f"💾 Saved {len(company_stats)} company stats")
    
    # Save location stats
    with open(PROCESSED_DIR / "location_stats.json", 'w') as f:
        json.dump(location_stats, f, indent=2)
    print(f"💾 Saved {len(location_stats)} location stats")
    
    # Save source stats
    with open(PROCESSED_DIR / "source_stats.json", 'w') as f:
        json.dump(source_stats, f, indent=2)
    print(f"💾 Saved {len(source_stats)} source stats")
    
    # Save summary
    with open(PROCESSED_DIR / "summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"💾 Saved summary")
    
    # Also save empty companies/skills master lists (can be populated later)
    with open(PROCESSED_DIR / "companies.json", 'w') as f:
        companies = [{'id': i+1, 'name': s['company']} for i, s in enumerate(company_stats)]
        json.dump(companies, f, indent=2)
    
    with open(PROCESSED_DIR / "skills.json", 'w') as f:
        skills = [{'id': i+1, 'name': s['name'], 'category': s['category']} for i, s in enumerate(skill_stats)]
        json.dump(skills, f, indent=2)


def main():
    print("=" * 60)
    print("📊 UPDATING DASHBOARD WITH REAL DATA ONLY")
    print("=" * 60)
    print()
    
    # Load all scraped data
    jobs = load_all_scraped_data()
    
    if not jobs:
        print("\n⚠️ No scraped data found!")
        print("Run the scrapers first:")
        print("  python3 scripts/scrape_all_sources.py")
        return
    
    # Deduplicate
    jobs = deduplicate_jobs(jobs)
    print(f"\nAfter deduplication: {len(jobs)} unique jobs")
    
    # Generate stats
    skill_stats, company_stats, location_stats, source_stats, summary = generate_stats(jobs)
    
    # Save for dashboard
    print()
    save_for_dashboard(jobs, skill_stats, company_stats, location_stats, source_stats, summary)
    
    print("\n" + "=" * 60)
    print("✅ DASHBOARD DATA UPDATED - REAL DATA ONLY")
    print("=" * 60)
    print(f"\nTotal Real Jobs: {summary['total_jobs']}")
    print(f"Companies: {summary['total_companies']}")
    print(f"Skills Tracked: {summary['total_skills_tracked']}")
    print(f"Sources: {summary['sources_count']}")
    print("\nDashboard will now show only real scraped data!")
    print("=" * 60)


if __name__ == "__main__":
    main()
