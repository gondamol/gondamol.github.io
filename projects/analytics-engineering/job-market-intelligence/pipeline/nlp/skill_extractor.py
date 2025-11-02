"""
NLP Skill Extraction from Job Descriptions
"""
import re
import logging
from typing import List, Dict, Set
import spacy
from ..config import TARGET_SKILLS, NLP_CONFIG
from ..database.connection import get_db
from ..database.models import Skill, Job, JobSkill

logger = logging.getLogger(__name__)


class SkillExtractor:
    """Extract skills from job descriptions using NLP"""
    
    def __init__(self):
        try:
            self.nlp = spacy.load(NLP_CONFIG['spacy_model'])
        except OSError:
            logger.warning(f"spaCy model '{NLP_CONFIG['spacy_model']}' not found. Run: python -m spacy download {NLP_CONFIG['spacy_model']}")
            self.nlp = None
        
        # Convert target skills to lowercase for matching
        self.target_skills = {skill.lower(): skill for skill in TARGET_SKILLS}
        
        # Common skill variations
        self.skill_variations = {
            'python': ['python', 'python3', 'py'],
            'sql': ['sql', 'structured query language', 't-sql', 'pl/sql', 'mysql', 'postgresql', 'postgres'],
            'r': ['r programming', 'r language'],
            'javascript': ['javascript', 'js', 'node.js', 'nodejs'],
            'power bi': ['power bi', 'powerbi', 'power-bi'],
            'tableau': ['tableau', 'tableau desktop'],
            'machine learning': ['machine learning', 'ml', 'predictive modeling'],
            'deep learning': ['deep learning', 'dl', 'neural networks'],
            'aws': ['aws', 'amazon web services'],
            'azure': ['azure', 'microsoft azure'],
            'gcp': ['gcp', 'google cloud', 'google cloud platform'],
        }
    
    def normalize_skill(self, skill_text: str) -> str:
        """Normalize skill text to standard form"""
        skill_lower = skill_text.lower().strip()
        
        # Check if it's a known variation
        for standard_skill, variations in self.skill_variations.items():
            if skill_lower in variations:
                # Return the original case from TARGET_SKILLS
                for original_skill, _ in self.target_skills.items():
                    if original_skill == standard_skill:
                        return self.target_skills[original_skill]
        
        # Check if it's in target skills
        if skill_lower in self.target_skills:
            return self.target_skills[skill_lower]
        
        return None
    
    def extract_skills_regex(self, text: str) -> Set[str]:
        """Extract skills using regex patterns"""
        if not text:
            return set()
        
        text_lower = text.lower()
        found_skills = set()
        
        # Check each target skill
        for skill_lower, skill_original in self.target_skills.items():
            # Create pattern with word boundaries
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill_original)
        
        # Check skill variations
        for standard_skill, variations in self.skill_variations.items():
            for variation in variations:
                pattern = r'\b' + re.escape(variation) + r'\b'
                if re.search(pattern, text_lower):
                    # Add the standard form
                    if standard_skill in self.target_skills:
                        found_skills.add(self.target_skills[standard_skill])
                    break
        
        return found_skills
    
    def extract_skills_nlp(self, text: str) -> Set[str]:
        """Extract skills using spaCy NLP"""
        if not self.nlp or not text:
            return set()
        
        doc = self.nlp(text)
        found_skills = set()
        
        # Extract noun chunks and entities
        for chunk in doc.noun_chunks:
            skill = self.normalize_skill(chunk.text)
            if skill:
                found_skills.add(skill)
        
        for ent in doc.ents:
            skill = self.normalize_skill(ent.text)
            if skill:
                found_skills.add(skill)
        
        return found_skills
    
    def extract_skills(self, text: str) -> Set[str]:
        """
        Extract skills from text using both regex and NLP
        
        Args:
            text: Job description or requirements text
            
        Returns:
            Set of extracted skill names
        """
        if not text:
            return set()
        
        # Combine regex and NLP results
        skills_regex = self.extract_skills_regex(text)
        skills_nlp = self.extract_skills_nlp(text)
        
        return skills_regex | skills_nlp
    
    def extract_years_experience(self, text: str) -> Dict[str, int]:
        """
        Extract years of experience for skills
        
        Returns:
            Dict mapping skill names to years required
        """
        if not text:
            return {}
        
        text_lower = text.lower()
        skill_years = {}
        
        # Pattern: "X+ years of Python" or "Python (X years)"
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience\s+)?(?:with\s+)?(\w+)',
            r'(\w+)\s*\((\d+)\+?\s*(?:years?|yrs?)\)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                if len(match.groups()) == 2:
                    years_str, skill_text = match.groups()
                    try:
                        years = int(years_str)
                    except ValueError:
                        # Swap if order is reversed
                        years_str, skill_text = skill_text, years_str
                        try:
                            years = int(years_str)
                        except ValueError:
                            continue
                    
                    skill = self.normalize_skill(skill_text)
                    if skill:
                        skill_years[skill] = years
        
        return skill_years
    
    def process_job(self, job_id: int):
        """
        Extract and save skills for a job
        
        Args:
            job_id: Database ID of the job
        """
        try:
            with get_db() as db:
                # Get job
                job = db.query(Job).filter_by(id=job_id).first()
                if not job:
                    logger.warning(f"Job {job_id} not found")
                    return
                
                # Extract skills from description and requirements
                text = f"{job.description or ''} {job.requirements or ''}"
                skills = self.extract_skills(text)
                years_map = self.extract_years_experience(text)
                
                logger.info(f"Extracted {len(skills)} skills for job {job.title}")
                
                # Save skills
                for skill_name in skills:
                    # Get or create skill
                    skill = db.query(Skill).filter_by(name=skill_name).first()
                    if not skill:
                        # Determine category
                        category = self.get_skill_category(skill_name)
                        skill = Skill(name=skill_name, category=category)
                        db.add(skill)
                        db.flush()
                    
                    # Check if job-skill relationship exists
                    existing = db.query(JobSkill).filter_by(
                        job_id=job.id,
                        skill_id=skill.id
                    ).first()
                    
                    if not existing:
                        job_skill = JobSkill(
                            job_id=job.id,
                            skill_id=skill.id,
                            years_required=years_map.get(skill_name)
                        )
                        db.add(job_skill)
                
                db.commit()
                logger.info(f"Saved skills for job {job.title}")
                
        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}")
    
    def get_skill_category(self, skill_name: str) -> str:
        """Determine skill category"""
        skill_lower = skill_name.lower()
        
        if skill_lower in ['python', 'r', 'sql', 'javascript', 'java', 'scala', 'c++', 'c#']:
            return 'Programming'
        elif skill_lower in ['postgresql', 'mysql', 'mongodb', 'redis', 'cassandra', 'oracle']:
            return 'Database'
        elif skill_lower in ['power bi', 'tableau', 'looker', 'qlik', 'excel']:
            return 'BI Tool'
        elif skill_lower in ['aws', 'azure', 'gcp', 'snowflake', 'databricks']:
            return 'Cloud'
        elif 'machine learning' in skill_lower or 'deep learning' in skill_lower or \
             skill_lower in ['tensorflow', 'pytorch', 'scikit-learn', 'xgboost']:
            return 'ML/AI'
        elif skill_lower in ['spark', 'hadoop', 'kafka', 'airflow']:
            return 'Big Data'
        elif skill_lower in ['git', 'docker', 'kubernetes', 'jenkins']:
            return 'DevOps'
        else:
            return 'Other'
    
    def bulk_process_jobs(self, limit: int = None):
        """Process all jobs without skills"""
        try:
            with get_db() as db:
                # Find jobs without skills
                query = db.query(Job).outerjoin(JobSkill).filter(
                    JobSkill.id == None,
                    Job.is_active == True
                )
                
                if limit:
                    query = query.limit(limit)
                
                jobs = query.all()
                logger.info(f"Processing {len(jobs)} jobs for skill extraction")
                
                for job in jobs:
                    self.process_job(job.id)
                    
        except Exception as e:
            logger.error(f"Error in bulk processing: {e}")


