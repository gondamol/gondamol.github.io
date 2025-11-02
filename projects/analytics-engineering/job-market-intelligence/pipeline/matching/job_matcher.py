"""
Job Matching Algorithm
Matches users to relevant jobs based on their preferences
"""
import logging
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from sqlalchemy import and_, or_
from ..database.connection import get_db
from ..database.models import Job, UserProfile, JobAlert, JobSkill, Skill

logger = logging.getLogger(__name__)


class JobMatcher:
    """Match users to relevant jobs"""
    
    def __init__(self):
        self.weights = {
            'title': 0.3,
            'location': 0.2,
            'salary': 0.2,
            'skills': 0.2,
            'recency': 0.1,
        }
    
    def calculate_title_score(self, job_title: str, desired_titles: List[str]) -> float:
        """Calculate title match score"""
        if not desired_titles:
            return 0.5  # Neutral score
        
        job_title_lower = job_title.lower()
        
        # Exact match
        for desired in desired_titles:
            if desired.lower() == job_title_lower:
                return 1.0
        
        # Partial match
        for desired in desired_titles:
            if desired.lower() in job_title_lower or job_title_lower in desired.lower():
                return 0.7
        
        # Keyword match
        job_keywords = set(job_title_lower.split())
        for desired in desired_titles:
            desired_keywords = set(desired.lower().split())
            overlap = job_keywords & desired_keywords
            if overlap:
                return 0.4 + (len(overlap) / max(len(job_keywords), len(desired_keywords))) * 0.3
        
        return 0.0
    
    def calculate_location_score(self, job_location: str, job_remote: str, 
                                 desired_locations: List[str], desired_remote: str) -> float:
        """Calculate location match score"""
        if not desired_locations and not desired_remote:
            return 0.5  # Neutral score
        
        score = 0.0
        
        # Remote preference match
        if desired_remote:
            if desired_remote.lower() == 'remote' and job_remote and 'remote' in job_remote.lower():
                score += 0.5
            elif desired_remote.lower() == 'hybrid' and job_remote and 'hybrid' in job_remote.lower():
                score += 0.4
            elif desired_remote.lower() == 'on-site' and (not job_remote or 'on-site' in job_remote.lower()):
                score += 0.3
        
        # Location match
        if desired_locations and job_location:
            job_loc_lower = job_location.lower()
            for desired_loc in desired_locations:
                if desired_loc.lower() in job_loc_lower or job_loc_lower in desired_loc.lower():
                    score += 0.5
                    break
        
        return min(score, 1.0)
    
    def calculate_salary_score(self, job_min: int, job_max: int, 
                               user_min: int) -> float:
        """Calculate salary match score"""
        if not user_min:
            return 0.5  # Neutral score
        
        if not job_min and not job_max:
            return 0.5  # Unknown salary
        
        # Use job_max if available, otherwise job_min
        job_salary = job_max if job_max else job_min
        
        if job_salary >= user_min:
            # Calculate how much above minimum
            excess_ratio = (job_salary - user_min) / user_min
            return min(0.5 + excess_ratio * 0.5, 1.0)
        else:
            # Calculate how much below minimum
            deficit_ratio = job_salary / user_min
            return max(deficit_ratio, 0.0)
    
    def calculate_recency_score(self, posted_date: datetime) -> float:
        """Calculate recency score (prefer newer jobs)"""
        if not posted_date:
            return 0.3
        
        days_old = (datetime.utcnow() - posted_date).days
        
        if days_old <= 1:
            return 1.0
        elif days_old <= 3:
            return 0.9
        elif days_old <= 7:
            return 0.7
        elif days_old <= 14:
            return 0.5
        elif days_old <= 30:
            return 0.3
        else:
            return 0.1
    
    def calculate_match_score(self, job: Job, user: UserProfile, 
                            job_skills: List[str] = None) -> Tuple[float, List[str]]:
        """
        Calculate overall match score between job and user
        
        Returns:
            Tuple of (score, reasons)
        """
        reasons = []
        
        # Title score
        title_score = self.calculate_title_score(job.title, user.desired_titles or [])
        if title_score > 0.7:
            reasons.append(f"Title matches your profile ({int(title_score * 100)}%)")
        
        # Location score
        location_score = self.calculate_location_score(
            job.location, job.remote_type,
            user.desired_locations or [], user.desired_remote
        )
        if location_score > 0.7:
            reasons.append(f"Location matches your preference ({int(location_score * 100)}%)")
        
        # Salary score
        salary_score = self.calculate_salary_score(
            job.salary_min, job.salary_max, user.min_salary
        )
        if salary_score > 0.7 and user.min_salary:
            reasons.append(f"Salary meets your requirement (≥{user.min_salary:,})")
        
        # Skills score
        skills_score = 0.5  # Default neutral
        if job_skills:
            # Would need to compare with user's skills
            # For now, just check if job has skills
            skills_score = 0.7
            reasons.append(f"{len(job_skills)} relevant skills identified")
        
        # Recency score
        recency_score = self.calculate_recency_score(job.posted_date)
        if recency_score > 0.7:
            reasons.append("Recently posted")
        
        # Calculate weighted total
        total_score = (
            title_score * self.weights['title'] +
            location_score * self.weights['location'] +
            salary_score * self.weights['salary'] +
            skills_score * self.weights['skills'] +
            recency_score * self.weights['recency']
        ) * 100
        
        return total_score, reasons
    
    def find_matches_for_user(self, user_id: int, min_score: float = 60.0, 
                             days_back: int = 7) -> List[Dict]:
        """
        Find matching jobs for a user
        
        Args:
            user_id: User database ID
            min_score: Minimum match score (0-100)
            days_back: Only consider jobs from last N days
            
        Returns:
            List of matching jobs with scores
        """
        try:
            with get_db() as db:
                # Get user
                user = db.query(UserProfile).filter_by(id=user_id).first()
                if not user or not user.is_active:
                    logger.warning(f"User {user_id} not found or inactive")
                    return []
                
                # Build job query
                cutoff_date = datetime.utcnow() - timedelta(days=days_back)
                query = db.query(Job).filter(
                    Job.is_active == True,
                    Job.posted_date >= cutoff_date
                )
                
                # Filter by employment type if specified
                if user.preferred_employment_types:
                    query = query.filter(
                        or_(*[Job.employment_type.ilike(f"%{t}%") 
                             for t in user.preferred_employment_types])
                    )
                
                jobs = query.all()
                logger.info(f"Found {len(jobs)} active jobs to match for user {user.email}")
                
                matches = []
                for job in jobs:
                    # Get job skills
                    job_skills = [js.skill.name for js in job.skills]
                    
                    # Calculate match score
                    score, reasons = self.calculate_match_score(job, user, job_skills)
                    
                    if score >= min_score:
                        matches.append({
                            'job': job,
                            'score': round(score, 2),
                            'reasons': reasons,
                        })
                
                # Sort by score (descending)
                matches.sort(key=lambda x: x['score'], reverse=True)
                
                logger.info(f"Found {len(matches)} matching jobs for user {user.email}")
                return matches
                
        except Exception as e:
            logger.error(f"Error finding matches for user {user_id}: {e}")
            return []
    
    def create_alerts(self, user_id: int, min_score: float = 70.0):
        """
        Create job alerts for matching jobs
        
        Args:
            user_id: User database ID
            min_score: Minimum match score to create alert
        """
        try:
            matches = self.find_matches_for_user(user_id, min_score)
            
            if not matches:
                logger.info(f"No matches found for user {user_id}")
                return
            
            with get_db() as db:
                for match in matches:
                    job = match['job']
                    
                    # Check if alert already exists
                    existing = db.query(JobAlert).filter_by(
                        user_id=user_id,
                        job_id=job.id
                    ).first()
                    
                    if not existing:
                        alert = JobAlert(
                            user_id=user_id,
                            job_id=job.id,
                            match_score=match['score'],
                            match_reasons=match['reasons'],
                        )
                        db.add(alert)
                
                db.commit()
                logger.info(f"Created {len(matches)} alerts for user {user_id}")
                
        except Exception as e:
            logger.error(f"Error creating alerts for user {user_id}: {e}")
    
    def bulk_match_all_users(self, min_score: float = 70.0):
        """Run matching for all active users"""
        try:
            with get_db() as db:
                users = db.query(UserProfile).filter_by(is_active=True).all()
                logger.info(f"Running matching for {len(users)} active users")
                
                for user in users:
                    self.create_alerts(user.id, min_score)
                    
        except Exception as e:
            logger.error(f"Error in bulk matching: {e}")


