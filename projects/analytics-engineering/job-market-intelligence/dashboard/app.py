"""
Streamlit Dashboard for Job Market Intelligence
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add pipeline to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.database.connection import get_db
from pipeline.database.models import Job, Skill, JobSkill, UserProfile, ScrapingLog
from sqlalchemy import func, desc

# Page config
st.set_page_config(
    page_title="Job Market Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_job_statistics():
    """Load job statistics from database"""
    try:
        with get_db() as db:
            # Total jobs
            total_jobs = db.query(Job).filter_by(is_active=True).count()
            
            # Jobs by source
            jobs_by_source = db.query(
                Job.source,
                func.count(Job.id).label('count')
            ).filter_by(is_active=True).group_by(Job.source).all()
            
            # Recent jobs (last 7 days)
            week_ago = datetime.utcnow() - timedelta(days=7)
            recent_jobs = db.query(Job).filter(
                Job.is_active == True,
                Job.posted_date >= week_ago
            ).count()
            
            # Top locations
            top_locations = db.query(
                Job.location,
                func.count(Job.id).label('count')
            ).filter_by(is_active=True).group_by(Job.location).order_by(
                desc('count')
            ).limit(10).all()
            
            # Top companies
            top_companies = db.query(
                Job.company_name,
                func.count(Job.id).label('count')
            ).filter_by(is_active=True).group_by(Job.company_name).order_by(
                desc('count')
            ).limit(10).all()
            
            # Average salary by source
            avg_salaries = db.query(
                Job.source,
                func.avg(Job.salary_max).label('avg_salary')
            ).filter(
                Job.is_active == True,
                Job.salary_max.isnot(None)
            ).group_by(Job.source).all()
            
            return {
                'total_jobs': total_jobs,
                'recent_jobs': recent_jobs,
                'jobs_by_source': jobs_by_source,
                'top_locations': top_locations,
                'top_companies': top_companies,
                'avg_salaries': avg_salaries,
            }
    except Exception as e:
        st.error(f"Error loading statistics: {e}")
        return None


@st.cache_data(ttl=300)
def load_skill_statistics():
    """Load skill statistics from database"""
    try:
        with get_db() as db:
            # Top skills
            top_skills = db.query(
                Skill.name,
                Skill.category,
                func.count(JobSkill.id).label('job_count')
            ).join(JobSkill).join(Job).filter(
                Job.is_active == True
            ).group_by(Skill.id).order_by(
                desc('job_count')
            ).limit(20).all()
            
            # Skills by category
            skills_by_category = db.query(
                Skill.category,
                func.count(JobSkill.id).label('count')
            ).join(JobSkill).join(Job).filter(
                Job.is_active == True
            ).group_by(Skill.category).order_by(
                desc('count')
            ).all()
            
            return {
                'top_skills': top_skills,
                'skills_by_category': skills_by_category,
            }
    except Exception as e:
        st.error(f"Error loading skill statistics: {e}")
        return None


@st.cache_data(ttl=300)
def load_recent_jobs(limit=50):
    """Load recent jobs from database"""
    try:
        with get_db() as db:
            jobs = db.query(Job).filter_by(is_active=True).order_by(
                desc(Job.posted_date)
            ).limit(limit).all()
            
            jobs_data = []
            for job in jobs:
                jobs_data.append({
                    'Title': job.title,
                    'Company': job.company_name,
                    'Location': job.location,
                    'Source': job.source,
                    'Posted': job.posted_date.strftime('%Y-%m-%d') if job.posted_date else 'N/A',
                    'Salary Min': job.salary_min,
                    'Salary Max': job.salary_max,
                    'URL': job.source_url,
                })
            
            return pd.DataFrame(jobs_data)
    except Exception as e:
        st.error(f"Error loading recent jobs: {e}")
        return pd.DataFrame()


def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<p class="main-header">🎯 Job Market Intelligence</p>', unsafe_allow_html=True)
    st.markdown("### Real-time Data Analytics Job Market Insights")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Filters")
        
        refresh = st.button("🔄 Refresh Data", use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 📊 About")
        st.info(
            "This dashboard provides real-time insights into the data analytics "
            "job market by scraping and analyzing job postings from multiple sources."
        )
        
        st.markdown("### 🎯 Data Sources")
        st.markdown("""
        - Indeed Kenya
        - Fuzu Kenya
        - BrighterMonday
        - LinkedIn
        - Glassdoor
        - AngelList
        """)
    
    # Load data
    with st.spinner("Loading data..."):
        stats = load_job_statistics()
        skill_stats = load_skill_statistics()
    
    if not stats:
        st.error("Failed to load data. Please check database connection.")
        return
    
    # Key Metrics
    st.markdown("## 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Active Jobs",
            value=f"{stats['total_jobs']:,}",
            delta=f"+{stats['recent_jobs']} this week"
        )
    
    with col2:
        sources_count = len(stats['jobs_by_source'])
        st.metric(
            label="Job Boards",
            value=sources_count,
            delta="Live scraping"
        )
    
    with col3:
        if stats['avg_salaries']:
            avg_salary = sum([s[1] for s in stats['avg_salaries'] if s[1]]) / len(stats['avg_salaries'])
            st.metric(
                label="Avg. Max Salary (KES)",
                value=f"{avg_salary:,.0f}"
            )
    
    with col4:
        if skill_stats and skill_stats['top_skills']:
            total_skills = len(skill_stats['top_skills'])
            st.metric(
                label="Skills Tracked",
                value=total_skills,
                delta="From NLP analysis"
            )
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Top Locations")
        if stats['top_locations']:
            df_locations = pd.DataFrame(stats['top_locations'], columns=['Location', 'Count'])
            fig = px.bar(
                df_locations,
                x='Count',
                y='Location',
                orientation='h',
                color='Count',
                color_continuous_scale='Blues',
                title="Job Opportunities by Location"
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏢 Top Hiring Companies")
        if stats['top_companies']:
            df_companies = pd.DataFrame(stats['top_companies'], columns=['Company', 'Count'])
            fig = px.bar(
                df_companies,
                x='Count',
                y='Company',
                orientation='h',
                color='Count',
                color_continuous_scale='Greens',
                title="Most Active Employers"
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Jobs by Source")
        if stats['jobs_by_source']:
            df_sources = pd.DataFrame(stats['jobs_by_source'], columns=['Source', 'Count'])
            fig = px.pie(
                df_sources,
                values='Count',
                names='Source',
                title="Distribution by Job Board",
                hole=0.4
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 💰 Average Salary by Source")
        if stats['avg_salaries']:
            df_salaries = pd.DataFrame(stats['avg_salaries'], columns=['Source', 'Avg Salary'])
            df_salaries = df_salaries[df_salaries['Avg Salary'].notna()]
            fig = px.bar(
                df_salaries,
                x='Source',
                y='Avg Salary',
                color='Avg Salary',
                color_continuous_scale='Viridis',
                title="Average Maximum Salary (KES)"
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Skills Analysis
    if skill_stats and skill_stats['top_skills']:
        st.markdown("---")
        st.markdown("## 🛠️ Skills Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Top 20 In-Demand Skills")
            df_skills = pd.DataFrame(
                skill_stats['top_skills'],
                columns=['Skill', 'Category', 'Job Count']
            )
            fig = px.bar(
                df_skills.head(20),
                x='Job Count',
                y='Skill',
                orientation='h',
                color='Category',
                title="Most Required Skills"
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Skills by Category")
            df_cat = pd.DataFrame(
                skill_stats['skills_by_category'],
                columns=['Category', 'Count']
            )
            fig = px.pie(
                df_cat,
                values='Count',
                names='Category',
                title="Skill Distribution",
                hole=0.3
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Jobs Table
    st.markdown("---")
    st.markdown("## 📋 Recent Job Postings")
    
    df_jobs = load_recent_jobs(limit=100)
    
    if not df_jobs.empty:
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            sources = ['All'] + sorted(df_jobs['Source'].unique().tolist())
            selected_source = st.selectbox("Source", sources)
        
        with col2:
            locations = ['All'] + sorted(df_jobs['Location'].dropna().unique().tolist())
            selected_location = st.selectbox("Location", locations)
        
        with col3:
            search_term = st.text_input("Search in title", "")
        
        # Apply filters
        filtered_df = df_jobs.copy()
        if selected_source != 'All':
            filtered_df = filtered_df[filtered_df['Source'] == selected_source]
        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df['Location'] == selected_location]
        if search_term:
            filtered_df = filtered_df[
                filtered_df['Title'].str.contains(search_term, case=False, na=False)
            ]
        
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400,
            column_config={
                "URL": st.column_config.LinkColumn("Apply Link")
            }
        )
        
        st.markdown(f"**Showing {len(filtered_df)} of {len(df_jobs)} jobs**")
    else:
        st.info("No recent jobs found. Run the scraper to populate the database.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ by [Nicodemus Werre](https://linkedin.com/in/amollow) | "
        "📧 nichodemuswerre@gmail.com | "
        "🔗 [GitHub](https://github.com/gondamol)"
    )


if __name__ == "__main__":
    main()






