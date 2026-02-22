-- Job Market Intelligence Database Schema
-- PostgreSQL 14+

-- Extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop tables if they exist (for clean setup)
DROP TABLE IF EXISTS job_applications CASCADE;
DROP TABLE IF EXISTS job_alerts CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;
DROP TABLE IF EXISTS job_skills CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS jobs CASCADE;
DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS scraping_logs CASCADE;

-- Companies table
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    website VARCHAR(500),
    industry VARCHAR(100),
    company_size VARCHAR(50),
    headquarters_location VARCHAR(255),
    description TEXT,
    logo_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name)
);

CREATE INDEX idx_companies_name ON companies(name);

-- Jobs table
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    job_id VARCHAR(255) UNIQUE NOT NULL,  -- Unique ID from source
    source VARCHAR(50) NOT NULL,  -- linkedin, indeed, glassdoor, etc.
    source_url VARCHAR(1000) NOT NULL,
    
    -- Job Details
    title VARCHAR(500) NOT NULL,
    company_id INTEGER REFERENCES companies(id),
    company_name VARCHAR(255),  -- Denormalized for quick access
    
    -- Location
    location VARCHAR(255),
    remote_type VARCHAR(50),  -- Remote, Hybrid, On-site
    country VARCHAR(100),
    city VARCHAR(100),
    
    -- Job Info
    description TEXT,
    requirements TEXT,
    responsibilities TEXT,
    
    -- Compensation
    salary_min INTEGER,
    salary_max INTEGER,
    salary_currency VARCHAR(10) DEFAULT 'KES',
    salary_period VARCHAR(20),  -- Yearly, Monthly, Hourly
    
    -- Job Type
    employment_type VARCHAR(50),  -- Full-time, Part-time, Contract
    experience_level VARCHAR(50),  -- Entry, Mid, Senior, Lead
    
    -- Dates
    posted_date TIMESTAMP,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    applications_count INTEGER DEFAULT 0,
    
    -- Metadata
    metadata JSONB,  -- Store additional unstructured data
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_jobs_title ON jobs(title);
CREATE INDEX idx_jobs_company ON jobs(company_id);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date DESC);
CREATE INDEX idx_jobs_source ON jobs(source);
CREATE INDEX idx_jobs_active ON jobs(is_active);
CREATE INDEX idx_jobs_experience ON jobs(experience_level);

-- Skills master table
CREATE TABLE skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),  -- Programming, Database, Tool, Cloud, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_skills_name ON skills(name);
CREATE INDEX idx_skills_category ON skills(category);

-- Job-Skills junction table
CREATE TABLE job_skills (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    is_required BOOLEAN DEFAULT FALSE,
    years_required INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_id, skill_id)
);

CREATE INDEX idx_job_skills_job ON job_skills(job_id);
CREATE INDEX idx_job_skills_skill ON job_skills(skill_id);

-- User profiles table (for job seekers)
CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY,
    user_id UUID DEFAULT uuid_generate_v4() UNIQUE,
    email VARCHAR(255) UNIQUE NOT NULL,
    telegram_id VARCHAR(100),
    
    -- Profile Info
    full_name VARCHAR(255),
    current_title VARCHAR(255),
    years_experience INTEGER,
    location VARCHAR(255),
    
    -- Preferences
    desired_titles TEXT[],  -- Array of job titles
    desired_locations TEXT[],
    desired_remote_type VARCHAR(50),
    min_salary INTEGER,
    preferred_employment_types TEXT[],
    
    -- Notification Settings
    email_notifications BOOLEAN DEFAULT TRUE,
    telegram_notifications BOOLEAN DEFAULT TRUE,
    notification_frequency VARCHAR(20) DEFAULT 'daily',  -- instant, daily, weekly
    
    -- Profile Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON user_profiles(email);
CREATE INDEX idx_users_telegram ON user_profiles(telegram_id);
CREATE INDEX idx_users_active ON user_profiles(is_active);

-- Job alerts table
CREATE TABLE job_alerts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    
    match_score DECIMAL(5,2),  -- 0-100 score
    match_reasons TEXT[],  -- Why this job matched
    
    -- Alert Status
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    was_opened BOOLEAN DEFAULT FALSE,
    opened_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_alerts_user ON job_alerts(user_id);
CREATE INDEX idx_alerts_job ON job_alerts(job_id);
CREATE INDEX idx_alerts_sent ON job_alerts(sent_at DESC);

-- Job applications tracking
CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES user_profiles(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
    
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'applied',  -- applied, interviewing, rejected, accepted
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, job_id)
);

CREATE INDEX idx_applications_user ON job_applications(user_id);
CREATE INDEX idx_applications_job ON job_applications(job_id);
CREATE INDEX idx_applications_status ON job_applications(status);

-- Scraping logs table
CREATE TABLE scraping_logs (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    status VARCHAR(20),  -- running, completed, failed
    
    jobs_scraped INTEGER DEFAULT 0,
    jobs_new INTEGER DEFAULT 0,
    jobs_updated INTEGER DEFAULT 0,
    
    error_message TEXT,
    metadata JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_source ON scraping_logs(source);
CREATE INDEX idx_logs_started ON scraping_logs(started_at DESC);
CREATE INDEX idx_logs_status ON scraping_logs(status);

-- Insert common skills
INSERT INTO skills (name, category) VALUES
    -- Programming
    ('Python', 'Programming'),
    ('R', 'Programming'),
    ('SQL', 'Programming'),
    ('JavaScript', 'Programming'),
    ('Java', 'Programming'),
    ('Scala', 'Programming'),
    
    -- Databases
    ('PostgreSQL', 'Database'),
    ('MySQL', 'Database'),
    ('MongoDB', 'Database'),
    ('Redis', 'Database'),
    
    -- BI Tools
    ('Power BI', 'BI Tool'),
    ('Tableau', 'BI Tool'),
    ('Looker', 'BI Tool'),
    ('Excel', 'Office Suite'),
    
    -- Big Data
    ('Apache Spark', 'Big Data'),
    ('Apache Kafka', 'Big Data'),
    ('Apache Airflow', 'Orchestration'),
    ('Hadoop', 'Big Data'),
    
    -- Cloud
    ('AWS', 'Cloud'),
    ('Azure', 'Cloud'),
    ('GCP', 'Cloud'),
    
    -- ML/AI
    ('Machine Learning', 'ML/AI'),
    ('Deep Learning', 'ML/AI'),
    ('TensorFlow', 'ML/AI'),
    ('PyTorch', 'ML/AI'),
    ('scikit-learn', 'ML/AI'),
    
    -- Other
    ('Git', 'Version Control'),
    ('Docker', 'DevOps'),
    ('Kubernetes', 'DevOps'),
    ('Statistics', 'Analytics'),
    ('A/B Testing', 'Analytics')
ON CONFLICT (name) DO NOTHING;

-- Create view for job statistics
CREATE OR REPLACE VIEW job_statistics AS
SELECT 
    source,
    COUNT(*) as total_jobs,
    COUNT(*) FILTER (WHERE posted_date >= CURRENT_DATE - INTERVAL '7 days') as jobs_last_week,
    COUNT(*) FILTER (WHERE posted_date >= CURRENT_DATE - INTERVAL '30 days') as jobs_last_month,
    AVG(salary_min) as avg_salary_min,
    AVG(salary_max) as avg_salary_max
FROM jobs
WHERE is_active = TRUE
GROUP BY source;

-- Create view for top skills
CREATE OR REPLACE VIEW top_skills AS
SELECT 
    s.name,
    s.category,
    COUNT(js.id) as job_count,
    ROUND(COUNT(js.id) * 100.0 / (SELECT COUNT(*) FROM jobs WHERE is_active = TRUE), 2) as percentage
FROM skills s
LEFT JOIN job_skills js ON s.id = js.skill_id
LEFT JOIN jobs j ON js.job_id = j.id
WHERE j.is_active = TRUE
GROUP BY s.id, s.name, s.category
ORDER BY job_count DESC
LIMIT 50;

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_job_applications_updated_at BEFORE UPDATE ON job_applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


