"""
Generate Demo Data for Job Market Intelligence Dashboard

This script creates realistic sample data for demonstrating the dashboard
without requiring a live database connection.
"""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Kenyan Companies
COMPANIES = [
    {"name": "Safaricom PLC", "industry": "Telecommunications", "size": "10000+", "location": "Nairobi"},
    {"name": "Kenya Commercial Bank", "industry": "Banking", "size": "5000-10000", "location": "Nairobi"},
    {"name": "Equity Bank", "industry": "Banking", "size": "5000-10000", "location": "Nairobi"},
    {"name": "NCBA Bank", "industry": "Banking", "size": "1000-5000", "location": "Nairobi"},
    {"name": "M-KOPA", "industry": "Fintech", "size": "500-1000", "location": "Nairobi"},
    {"name": "Twiga Foods", "industry": "AgriTech", "size": "500-1000", "location": "Nairobi"},
    {"name": "KEMRI", "industry": "Research", "size": "1000-5000", "location": "Nairobi"},
    {"name": "Africa Population Health Research Center", "industry": "Research", "size": "200-500", "location": "Nairobi"},
    {"name": "World Bank Kenya", "industry": "Development", "size": "200-500", "location": "Nairobi"},
    {"name": "UNICEF Kenya", "industry": "Development", "size": "200-500", "location": "Nairobi"},
    {"name": "MSF/Doctors Without Borders", "industry": "Healthcare", "size": "500-1000", "location": "Nairobi"},
    {"name": "Jumia Kenya", "industry": "E-commerce", "size": "200-500", "location": "Nairobi"},
    {"name": "Bolt (Taxify)", "industry": "Transport", "size": "100-200", "location": "Nairobi"},
    {"name": "Gro Intelligence", "industry": "AgriTech/Data", "size": "50-100", "location": "Nairobi"},
    {"name": "iProcure", "industry": "AgriTech", "size": "50-100", "location": "Nairobi"},
    {"name": "Cellulant", "industry": "Fintech", "size": "200-500", "location": "Nairobi"},
    {"name": "Andela Kenya", "industry": "Tech", "size": "100-200", "location": "Nairobi"},
    {"name": "Microsoft ADC", "industry": "Tech", "size": "500-1000", "location": "Nairobi"},
    {"name": "Google Kenya", "industry": "Tech", "size": "100-200", "location": "Nairobi"},
    {"name": "IBM Kenya", "industry": "Tech", "size": "100-200", "location": "Nairobi"},
]

# Job Titles
JOB_TITLES = [
    "Data Analyst",
    "Senior Data Analyst",
    "Data Scientist",
    "Business Intelligence Analyst",
    "Data Engineer",
    "Machine Learning Engineer",
    "Analytics Manager",
    "Research Data Manager",
    "Monitoring & Evaluation Officer",
    "Statistician",
    "Quantitative Analyst",
    "Health Data Analyst",
    "Financial Analyst",
    "Database Administrator",
    "ETL Developer",
    "BI Developer",
    "Junior Data Analyst",
    "Data Quality Analyst",
    "Market Research Analyst",
    "Product Analyst",
]

# Locations
LOCATIONS = [
    "Nairobi, Kenya",
    "Mombasa, Kenya",
    "Kisumu, Kenya",
    "Nakuru, Kenya",
    "Remote - Kenya",
    "Remote - East Africa",
    "Hybrid - Nairobi",
    "Nairobi CBD",
    "Westlands, Nairobi",
    "Upper Hill, Nairobi",
]

# Skills
SKILLS = [
    {"name": "Python", "category": "Programming"},
    {"name": "R", "category": "Programming"},
    {"name": "SQL", "category": "Programming"},
    {"name": "Excel", "category": "Office Suite"},
    {"name": "Power BI", "category": "BI Tool"},
    {"name": "Tableau", "category": "BI Tool"},
    {"name": "PostgreSQL", "category": "Database"},
    {"name": "MySQL", "category": "Database"},
    {"name": "MongoDB", "category": "Database"},
    {"name": "Machine Learning", "category": "ML/AI"},
    {"name": "Statistics", "category": "Analytics"},
    {"name": "AWS", "category": "Cloud"},
    {"name": "Azure", "category": "Cloud"},
    {"name": "GCP", "category": "Cloud"},
    {"name": "Apache Spark", "category": "Big Data"},
    {"name": "Apache Airflow", "category": "Orchestration"},
    {"name": "Docker", "category": "DevOps"},
    {"name": "Git", "category": "Version Control"},
    {"name": "Looker", "category": "BI Tool"},
    {"name": "dbt", "category": "Analytics Engineering"},
    {"name": "Snowflake", "category": "Cloud"},
    {"name": "Redshift", "category": "Cloud"},
    {"name": "TensorFlow", "category": "ML/AI"},
    {"name": "scikit-learn", "category": "ML/AI"},
    {"name": "Pandas", "category": "Programming"},
    {"name": "NumPy", "category": "Programming"},
    {"name": "Stata", "category": "Statistics"},
    {"name": "SPSS", "category": "Statistics"},
]

# Sources
SOURCES = ["fuzu", "brightermonday", "indeed", "linkedin", "glassdoor"]

# Experience Levels
EXPERIENCE_LEVELS = ["Entry", "Mid", "Senior", "Lead", "Manager"]

# Employment Types
EMPLOYMENT_TYPES = ["Full-time", "Contract", "Part-time", "Internship"]

# Salary Ranges (KES/month)
SALARY_RANGES = {
    "Entry": (50000, 100000),
    "Mid": (100000, 200000),
    "Senior": (200000, 400000),
    "Lead": (300000, 500000),
    "Manager": (400000, 700000),
}


def generate_job_description(title: str, skills: list) -> str:
    """Generate a realistic job description"""
    skill_list = ", ".join(skills[:5])
    templates = [
        f"We are looking for a talented {title} to join our growing team. "
        f"The ideal candidate will have experience with {skill_list}. "
        f"You will work on data-driven projects that impact business decisions.",
        
        f"Join our data team as a {title}! "
        f"Requirements include proficiency in {skill_list}. "
        f"Great opportunity to work with cutting-edge analytics technologies.",
        
        f"Exciting opportunity for a {title} to drive insights and analytics. "
        f"Must have strong skills in {skill_list}. "
        f"Competitive salary and benefits package offered.",
    ]
    return random.choice(templates)


def generate_jobs(num_jobs: int = 150) -> list:
    """Generate sample jobs"""
    jobs = []
    now = datetime.now()
    
    for i in range(num_jobs):
        company = random.choice(COMPANIES)
        title = random.choice(JOB_TITLES)
        exp_level = random.choice(EXPERIENCE_LEVELS)
        salary_min, salary_max = SALARY_RANGES[exp_level]
        
        # Randomize salary within range
        actual_min = random.randint(salary_min, salary_min + 30000)
        actual_max = random.randint(actual_min, salary_max)
        
        # Random skills for this job
        job_skills = random.sample(SKILLS, random.randint(3, 8))
        
        # Random posted date (within last 30 days)
        days_ago = random.randint(0, 30)
        posted_date = now - timedelta(days=days_ago)
        
        job = {
            "id": i + 1,
            "job_id": f"job_{i+1:05d}",
            "source": random.choice(SOURCES),
            "source_url": f"https://www.{random.choice(SOURCES)}.com/jobs/{i+1}",
            "title": title,
            "company_id": COMPANIES.index(company) + 1,
            "company_name": company["name"],
            "location": random.choice(LOCATIONS),
            "country": "Kenya",
            "city": random.choice(["Nairobi", "Mombasa", "Kisumu"]),
            "remote_type": random.choice(["On-site", "Remote", "Hybrid"]),
            "description": generate_job_description(title, [s["name"] for s in job_skills]),
            "requirements": f"Minimum {random.choice([1, 2, 3, 5])}+ years experience. "
                          f"Bachelor's degree in Computer Science, Statistics, or related field.",
            "salary_min": actual_min,
            "salary_max": actual_max,
            "salary_currency": "KES",
            "salary_period": "Monthly",
            "employment_type": random.choice(EMPLOYMENT_TYPES),
            "experience_level": exp_level,
            "posted_date": posted_date.isoformat(),
            "scraped_at": now.isoformat(),
            "is_active": True,
            "skills": [s["name"] for s in job_skills],
        }
        jobs.append(job)
    
    return jobs


def generate_skill_stats(jobs: list) -> list:
    """Calculate skill statistics from jobs"""
    skill_counts = {}
    
    for job in jobs:
        for skill in job.get("skills", []):
            if skill not in skill_counts:
                skill_counts[skill] = 0
            skill_counts[skill] += 1
    
    # Get category for each skill
    skill_category_map = {s["name"]: s["category"] for s in SKILLS}
    
    skill_stats = []
    for skill_name, count in sorted(skill_counts.items(), key=lambda x: -x[1]):
        skill_stats.append({
            "name": skill_name,
            "category": skill_category_map.get(skill_name, "Other"),
            "job_count": count,
            "percentage": round(count / len(jobs) * 100, 1),
        })
    
    return skill_stats


def generate_company_stats(jobs: list) -> list:
    """Calculate company hiring statistics"""
    company_counts = {}
    
    for job in jobs:
        company = job["company_name"]
        if company not in company_counts:
            company_counts[company] = 0
        company_counts[company] += 1
    
    return sorted(
        [{"company": k, "job_count": v} for k, v in company_counts.items()],
        key=lambda x: -x["job_count"]
    )


def generate_source_stats(jobs: list) -> list:
    """Calculate jobs by source"""
    source_counts = {}
    
    for job in jobs:
        source = job["source"]
        if source not in source_counts:
            source_counts[source] = 0
        source_counts[source] += 1
    
    return [{"source": k, "job_count": v} for k, v in source_counts.items()]


def generate_location_stats(jobs: list) -> list:
    """Calculate jobs by location"""
    location_counts = {}
    
    for job in jobs:
        loc = job["location"]
        if loc not in location_counts:
            location_counts[loc] = 0
        location_counts[loc] += 1
    
    return sorted(
        [{"location": k, "job_count": v} for k, v in location_counts.items()],
        key=lambda x: -x["job_count"]
    )


def main():
    """Generate all demo data"""
    print("🚀 Generating demo data for Job Market Intelligence...")
    
    # Generate jobs
    jobs = generate_jobs(150)
    print(f"✅ Generated {len(jobs)} sample jobs")
    
    # Generate statistics
    skill_stats = generate_skill_stats(jobs)
    company_stats = generate_company_stats(jobs)
    source_stats = generate_source_stats(jobs)
    location_stats = generate_location_stats(jobs)
    
    # Calculate summary metrics
    total_jobs = len(jobs)
    recent_jobs = len([j for j in jobs if (datetime.now() - datetime.fromisoformat(j["posted_date"])).days <= 7])
    avg_salary_min = sum(j["salary_min"] for j in jobs if j["salary_min"]) / len(jobs)
    avg_salary_max = sum(j["salary_max"] for j in jobs if j["salary_max"]) / len(jobs)
    
    summary = {
        "total_jobs": total_jobs,
        "recent_jobs_7_days": recent_jobs,
        "avg_salary_min": round(avg_salary_min),
        "avg_salary_max": round(avg_salary_max),
        "total_companies": len(set(j["company_name"] for j in jobs)),
        "total_skills_tracked": len(skill_stats),
        "sources_count": len(source_stats),
        "generated_at": datetime.now().isoformat(),
    }
    
    # Save all data
    with open(OUTPUT_DIR / "jobs.json", "w") as f:
        json.dump(jobs, f, indent=2)
    print(f"✅ Saved jobs to {OUTPUT_DIR / 'jobs.json'}")
    
    with open(OUTPUT_DIR / "skill_stats.json", "w") as f:
        json.dump(skill_stats, f, indent=2)
    print(f"✅ Saved skill stats to {OUTPUT_DIR / 'skill_stats.json'}")
    
    with open(OUTPUT_DIR / "company_stats.json", "w") as f:
        json.dump(company_stats, f, indent=2)
    print(f"✅ Saved company stats")
    
    with open(OUTPUT_DIR / "source_stats.json", "w") as f:
        json.dump(source_stats, f, indent=2)
    print(f"✅ Saved source stats")
    
    with open(OUTPUT_DIR / "location_stats.json", "w") as f:
        json.dump(location_stats, f, indent=2)
    print(f"✅ Saved location stats")
    
    with open(OUTPUT_DIR / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"✅ Saved summary stats")
    
    # Save companies
    with open(OUTPUT_DIR / "companies.json", "w") as f:
        json.dump([{"id": i+1, **c} for i, c in enumerate(COMPANIES)], f, indent=2)
    print(f"✅ Saved companies")
    
    # Save skills master list
    with open(OUTPUT_DIR / "skills.json", "w") as f:
        json.dump([{"id": i+1, **s} for i, s in enumerate(SKILLS)], f, indent=2)
    print(f"✅ Saved skills")
    
    print("\n🎉 Demo data generation complete!")
    print(f"\nSummary:")
    print(f"  - Total Jobs: {summary['total_jobs']}")
    print(f"  - Jobs This Week: {summary['recent_jobs_7_days']}")
    print(f"  - Avg Salary: KES {summary['avg_salary_min']:,} - {summary['avg_salary_max']:,}")
    print(f"  - Companies: {summary['total_companies']}")
    print(f"  - Skills Tracked: {summary['total_skills_tracked']}")


if __name__ == "__main__":
    main()
