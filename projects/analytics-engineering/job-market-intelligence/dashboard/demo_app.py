"""
Streamlit Dashboard for Job Market Intelligence
Demo Mode - Reads from JSON files (no database required)

Run with: streamlit run dashboard/demo_app.py
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path

# Data directory
DATA_DIR = Path(__file__).parent.parent / "data" / "processed"

# Page config
st.set_page_config(
    page_title="🎯 Kenya Job Market Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Kenyan theme
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        background: linear-gradient(90deg, #006f3c, #ce1126);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    
    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-top: 0;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #006f3c;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Skill badge */
    .skill-badge {
        display: inline-block;
        background: #e7f3ef;
        color: #006f3c;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 2px;
        font-size: 0.85rem;
    }
    
    /* Demo banner */
    .demo-banner {
        background: linear-gradient(90deg, #006f3c, #008751);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60)
def load_data():
    """Load all demo data from JSON files"""
    data = {}
    
    try:
        # Load jobs
        with open(DATA_DIR / "jobs.json", "r") as f:
            data['jobs'] = json.load(f)
        
        # Load statistics
        with open(DATA_DIR / "skill_stats.json", "r") as f:
            data['skill_stats'] = json.load(f)
        
        with open(DATA_DIR / "company_stats.json", "r") as f:
            data['company_stats'] = json.load(f)
        
        with open(DATA_DIR / "source_stats.json", "r") as f:
            data['source_stats'] = json.load(f)
        
        with open(DATA_DIR / "location_stats.json", "r") as f:
            data['location_stats'] = json.load(f)
        
        with open(DATA_DIR / "summary.json", "r") as f:
            data['summary'] = json.load(f)
        
        with open(DATA_DIR / "companies.json", "r") as f:
            data['companies'] = json.load(f)
        
        with open(DATA_DIR / "skills.json", "r") as f:
            data['skills'] = json.load(f)
        
        return data
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please run `python3 scripts/generate_demo_data.py` first to generate sample data.")
        return None


def format_salary(amount: int) -> str:
    """Format salary with K suffix"""
    if amount >= 1000000:
        return f"KES {amount/1000000:.1f}M"
    elif amount >= 1000:
        return f"KES {amount/1000:.0f}K"
    return f"KES {amount:,}"


def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<p class="main-header">🎯 Kenya Job Market Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Real-time Data Analytics Job Market Insights for Kenya</p>', unsafe_allow_html=True)
    
    # Demo banner
    st.markdown("""
    <div class="demo-banner">
        📊 <strong>DEMO MODE</strong> - Displaying sample data generated for demonstration purposes. 
        In production, this dashboard connects to live job scrapers.
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    if not data:
        return
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/200px-Flag_of_Kenya.svg.png", width=100)
        st.header("🔧 Dashboard Controls")
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Filters
        st.subheader("📍 Filters")
        
        # Location filter
        locations = ['All'] + sorted(set(j['location'] for j in data['jobs']))
        selected_location = st.selectbox("Location", locations)
        
        # Experience filter
        exp_levels = ['All'] + sorted(set(j['experience_level'] for j in data['jobs']))
        selected_exp = st.selectbox("Experience Level", exp_levels)
        
        # Source filter
        sources = ['All'] + sorted(set(j['source'] for j in data['jobs']))
        selected_source = st.selectbox("Job Source", sources)
        
        st.markdown("---")
        st.markdown("### 📊 About")
        st.info(
            "This dashboard provides real-time insights into Kenya's data analytics "
            "job market by scraping and analyzing job postings from multiple sources."
        )
        
        st.markdown("### 🎯 Data Sources")
        st.markdown("""
        - Fuzu Kenya
        - BrighterMonday
        - Indeed Kenya
        - LinkedIn
        - Glassdoor
        """)
    
    # Apply filters
    filtered_jobs = data['jobs']
    if selected_location != 'All':
        filtered_jobs = [j for j in filtered_jobs if j['location'] == selected_location]
    if selected_exp != 'All':
        filtered_jobs = [j for j in filtered_jobs if j['experience_level'] == selected_exp]
    if selected_source != 'All':
        filtered_jobs = [j for j in filtered_jobs if j['source'] == selected_source]
    
    summary = data['summary']
    
    # Key Metrics Row
    st.markdown("## 📈 Market Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Active Jobs",
            value=f"{len(filtered_jobs):,}",
            delta=f"+{summary['recent_jobs_7_days']} this week"
        )
    
    with col2:
        st.metric(
            label="Companies Hiring",
            value=summary['total_companies'],
            delta="Active employers"
        )
    
    with col3:
        avg_min = sum(j['salary_min'] for j in filtered_jobs if j.get('salary_min')) / max(len(filtered_jobs), 1)
        st.metric(
            label="Avg Min Salary",
            value=format_salary(int(avg_min)),
            delta="Monthly"
        )
    
    with col4:
        avg_max = sum(j['salary_max'] for j in filtered_jobs if j.get('salary_max')) / max(len(filtered_jobs), 1)
        st.metric(
            label="Avg Max Salary",
            value=format_salary(int(avg_max)),
            delta="Monthly"
        )
    
    with col5:
        st.metric(
            label="Skills Tracked",
            value=summary['total_skills_tracked'],
            delta="NLP extracted"
        )
    
    st.markdown("---")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💼 Top Hiring Companies")
        df_companies = pd.DataFrame(data['company_stats'][:10])
        fig = px.bar(
            df_companies,
            x='job_count',
            y='company',
            orientation='h',
            color='job_count',
            color_continuous_scale='Greens',
            labels={'job_count': 'Open Positions', 'company': 'Company'}
        )
        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📍 Jobs by Location")
        df_locations = pd.DataFrame(data['location_stats'][:10])
        fig = px.bar(
            df_locations,
            x='job_count',
            y='location',
            orientation='h',
            color='job_count',
            color_continuous_scale='Blues',
            labels={'job_count': 'Jobs Available', 'location': 'Location'}
        )
        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Jobs by Source")
        df_sources = pd.DataFrame(data['source_stats'])
        fig = px.pie(
            df_sources,
            values='job_count',
            names='source',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(height=400)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Experience Level Distribution")
        exp_counts = {}
        for job in filtered_jobs:
            exp = job.get('experience_level', 'Unknown')
            exp_counts[exp] = exp_counts.get(exp, 0) + 1
        
        df_exp = pd.DataFrame([
            {'level': k, 'count': v} for k, v in exp_counts.items()
        ])
        fig = px.pie(
            df_exp,
            values='count',
            names='level',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(height=400)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Skills Analysis
    st.markdown("---")
    st.markdown("## 🛠️ In-Demand Skills Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Top 15 Most Requested Skills")
        df_skills = pd.DataFrame(data['skill_stats'][:15])
        fig = px.bar(
            df_skills,
            x='job_count',
            y='name',
            orientation='h',
            color='category',
            labels={'job_count': 'Job Mentions', 'name': 'Skill', 'category': 'Category'}
        )
        fig.update_layout(
            height=500,
            yaxis={'categoryorder': 'total ascending'},
            legend={'orientation': 'h', 'y': -0.2}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Skills by Category")
        category_counts = {}
        for skill in data['skill_stats']:
            cat = skill.get('category', 'Other')
            category_counts[cat] = category_counts.get(cat, 0) + skill['job_count']
        
        df_cat = pd.DataFrame([
            {'category': k, 'count': v} for k, v in category_counts.items()
        ])
        fig = px.treemap(
            df_cat,
            path=['category'],
            values='count',
            color='count',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Salary Analysis
    st.markdown("---")
    st.markdown("## 💰 Salary Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Salary Range by Experience Level")
        salary_by_exp = {}
        for job in filtered_jobs:
            exp = job.get('experience_level', 'Unknown')
            if exp not in salary_by_exp:
                salary_by_exp[exp] = {'min': [], 'max': []}
            if job.get('salary_min'):
                salary_by_exp[exp]['min'].append(job['salary_min'])
            if job.get('salary_max'):
                salary_by_exp[exp]['max'].append(job['salary_max'])
        
        salary_data = []
        for exp, salaries in salary_by_exp.items():
            if salaries['min'] and salaries['max']:
                salary_data.append({
                    'Experience Level': exp,
                    'Avg Min Salary': sum(salaries['min']) / len(salaries['min']),
                    'Avg Max Salary': sum(salaries['max']) / len(salaries['max'])
                })
        
        if salary_data:
            df_salary = pd.DataFrame(salary_data)
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Min Salary',
                x=df_salary['Experience Level'],
                y=df_salary['Avg Min Salary'],
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                name='Max Salary',
                x=df_salary['Experience Level'],
                y=df_salary['Avg Max Salary'],
                marker_color='darkblue'
            ))
            fig.update_layout(
                barmode='group',
                height=400,
                yaxis_title='Salary (KES)',
                legend={'orientation': 'h', 'y': 1.1}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Salary Distribution")
        salaries = [j['salary_max'] for j in filtered_jobs if j.get('salary_max')]
        if salaries:
            fig = px.histogram(
                x=salaries,
                nbins=20,
                labels={'x': 'Salary (KES)', 'count': 'Number of Jobs'},
                color_discrete_sequence=['#006f3c']
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Jobs Table
    st.markdown("---")
    st.markdown("## 📋 Recent Job Postings")
    
    # Search
    search_term = st.text_input("🔍 Search jobs by title, company, or skills", "")
    
    # Filter by search
    display_jobs = filtered_jobs
    if search_term:
        search_lower = search_term.lower()
        display_jobs = [
            j for j in filtered_jobs
            if search_lower in j['title'].lower()
            or search_lower in j['company_name'].lower()
            or any(search_lower in s.lower() for s in j.get('skills', []))
        ]
    
    # Format for display
    df_display = pd.DataFrame([
        {
            'Title': j['title'],
            'Company': j['company_name'],
            'Location': j['location'],
            'Experience': j['experience_level'],
            'Salary Range': f"{format_salary(j['salary_min'])} - {format_salary(j['salary_max'])}" if j.get('salary_min') else 'Not specified',
            'Source': j['source'].title(),
            'Posted': j['posted_date'][:10] if j.get('posted_date') else 'N/A',
            'Skills': ', '.join(j.get('skills', [])[:5]),
        }
        for j in display_jobs[:100]
    ])
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400,
        column_config={
            "Skills": st.column_config.TextColumn(
                "Top Skills",
                width="medium"
            )
        }
    )
    
    st.markdown(f"**Showing {len(df_display)} of {len(filtered_jobs)} jobs matching your criteria**")
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🔗 Quick Links")
        st.markdown("""
        - [GitHub Repository](https://github.com/gondamol)
        - [Portfolio](https://gondamol.github.io)
        - [LinkedIn](https://linkedin.com/in/amollow)
        """)
    
    with col2:
        st.markdown("### 📧 Contact")
        st.markdown("""
        **Nicodemus Werre Amollo**  
        Research Data Manager & Data Scientist  
        📧 nichodemuswerre@gmail.com
        """)
    
    with col3:
        st.markdown("### 🛠️ Tech Stack")
        st.markdown("""
        - Python (BeautifulSoup, Scrapy)
        - PostgreSQL
        - Streamlit + Plotly
        - spaCy NLP
        """)
    
    st.markdown(
        "<center>Built with ❤️ by Nicodemus Werre | Kenya 🇰🇪</center>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
