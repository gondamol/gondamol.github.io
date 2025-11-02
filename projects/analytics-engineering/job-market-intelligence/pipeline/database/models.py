"""
SQLAlchemy ORM models for Job Market Intelligence
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, DECIMAL,
    ForeignKey, ARRAY, JSON, UniqueConstraint, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    website = Column(String(500))
    industry = Column(String(100))
    company_size = Column(String(50))
    headquarters_location = Column(String(255))
    description = Column(Text)
    logo_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    jobs = relationship('Job', back_populates='company')
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"


class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(String(255), unique=True, nullable=False)
    source = Column(String(50), nullable=False)
    source_url = Column(String(1000), nullable=False)
    
    # Job Details
    title = Column(String(500), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company_name = Column(String(255))
    
    # Location
    location = Column(String(255))
    remote_type = Column(String(50))
    country = Column(String(100))
    city = Column(String(100))
    
    # Job Info
    description = Column(Text)
    requirements = Column(Text)
    responsibilities = Column(Text)
    
    # Compensation
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    salary_currency = Column(String(10), default='KES')
    salary_period = Column(String(20))
    
    # Job Type
    employment_type = Column(String(50))
    experience_level = Column(String(50))
    
    # Dates
    posted_date = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # Status
    is_active = Column(Boolean, default=True)
    applications_count = Column(Integer, default=0)
    
    # Metadata
    metadata = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    company = relationship('Company', back_populates='jobs')
    skills = relationship('JobSkill', back_populates='job', cascade='all, delete-orphan')
    alerts = relationship('JobAlert', back_populates='job', cascade='all, delete-orphan')
    applications = relationship('JobApplication', back_populates='job', cascade='all, delete-orphan')
    
    # Indexes
    __table_args__ = (
        Index('idx_jobs_title', 'title'),
        Index('idx_jobs_company', 'company_id'),
        Index('idx_jobs_location', 'location'),
        Index('idx_jobs_posted_date', 'posted_date'),
        Index('idx_jobs_source', 'source'),
        Index('idx_jobs_active', 'is_active'),
    )
    
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company_name}')>"


class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job_skills = relationship('JobSkill', back_populates='skill')
    
    def __repr__(self):
        return f"<Skill(id={self.id}, name='{self.name}', category='{self.category}')>"


class JobSkill(Base):
    __tablename__ = 'job_skills'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id', ondelete='CASCADE'), nullable=False)
    is_required = Column(Boolean, default=False)
    years_required = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship('Job', back_populates='skills')
    skill = relationship('Skill', back_populates='job_skills')
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('job_id', 'skill_id', name='uq_job_skill'),
        Index('idx_job_skills_job', 'job_id'),
        Index('idx_job_skills_skill', 'skill_id'),
    )
    
    def __repr__(self):
        return f"<JobSkill(job_id={self.job_id}, skill_id={self.skill_id})>"


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    email = Column(String(255), unique=True, nullable=False)
    telegram_id = Column(String(100))
    
    # Profile Info
    full_name = Column(String(255))
    current_title = Column(String(255))
    years_experience = Column(Integer)
    location = Column(String(255))
    
    # Preferences
    desired_titles = Column(ARRAY(Text))
    desired_locations = Column(ARRAY(Text))
    desired_remote_type = Column(String(50))
    min_salary = Column(Integer)
    preferred_employment_types = Column(ARRAY(Text))
    
    # Notification Settings
    email_notifications = Column(Boolean, default=True)
    telegram_notifications = Column(Boolean, default=True)
    notification_frequency = Column(String(20), default='daily')
    
    # Profile Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    alerts = relationship('JobAlert', back_populates='user', cascade='all, delete-orphan')
    applications = relationship('JobApplication', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<UserProfile(id={self.id}, email='{self.email}')>"


class JobAlert(Base):
    __tablename__ = 'job_alerts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    
    match_score = Column(DECIMAL(5, 2))
    match_reasons = Column(ARRAY(Text))
    
    # Alert Status
    sent_at = Column(DateTime, default=datetime.utcnow)
    was_opened = Column(Boolean, default=False)
    opened_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship('UserProfile', back_populates='alerts')
    job = relationship('Job', back_populates='alerts')
    
    def __repr__(self):
        return f"<JobAlert(id={self.id}, user_id={self.user_id}, job_id={self.job_id})>"


class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_profiles.id', ondelete='CASCADE'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    
    applied_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='applied')
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('UserProfile', back_populates='applications')
    job = relationship('Job', back_populates='applications')
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'job_id', name='uq_user_job_application'),
    )
    
    def __repr__(self):
        return f"<JobApplication(id={self.id}, user_id={self.user_id}, job_id={self.job_id}, status='{self.status}')>"


class ScrapingLog(Base):
    __tablename__ = 'scraping_logs'
    
    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False)
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime)
    status = Column(String(20))
    
    jobs_scraped = Column(Integer, default=0)
    jobs_new = Column(Integer, default=0)
    jobs_updated = Column(Integer, default=0)
    
    error_message = Column(Text)
    metadata = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ScrapingLog(id={self.id}, source='{self.source}', status='{self.status}')>"

