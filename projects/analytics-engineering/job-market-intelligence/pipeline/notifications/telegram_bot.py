"""
Telegram Bot for Job Notifications
"""
import logging
from typing import List
from telegram import Bot
from telegram.error import TelegramError
from ..config import TELEGRAM_CONFIG
from ..database.connection import get_db
from ..database.models import UserProfile, JobAlert, Job

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Send job notifications via Telegram"""
    
    def __init__(self):
        self.bot = None
        if TELEGRAM_CONFIG['enabled']:
            try:
                self.bot = Bot(token=TELEGRAM_CONFIG['bot_token'])
                logger.info("Telegram bot initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Telegram bot: {e}")
    
    def format_job_message(self, job: Job, match_score: float, 
                          match_reasons: List[str]) -> str:
        """Format job information as Telegram message"""
        salary_text = ""
        if job.salary_min or job.salary_max:
            if job.salary_min and job.salary_max:
                salary_text = f"\n💰 Salary: {job.salary_currency} {job.salary_min:,} - {job.salary_max:,} ({job.salary_period})"
            elif job.salary_min:
                salary_text = f"\n💰 Salary: {job.salary_currency} {job.salary_min:,}+ ({job.salary_period})"
        
        location_text = f"\n📍 Location: {job.location}"
        if job.remote_type:
            location_text += f" ({job.remote_type})"
        
        reasons_text = "\n\n✅ Match Reasons:\n" + "\n".join([f"  • {r}" for r in match_reasons])
        
        message = f"""
🎯 **New Job Match: {int(match_score)}%**

**{job.title}**
🏢 Company: {job.company_name}{location_text}{salary_text}

📅 Posted: {job.posted_date.strftime('%Y-%m-%d') if job.posted_date else 'Recently'}
{reasons_text}

🔗 Apply: {job.source_url}
"""
        return message
    
    def send_message(self, telegram_id: str, message: str) -> bool:
        """
        Send message to Telegram user
        
        Args:
            telegram_id: Telegram user ID
            message: Message text
            
        Returns:
            True if successful, False otherwise
        """
        if not self.bot:
            logger.warning("Telegram bot not initialized")
            return False
        
        try:
            self.bot.send_message(
                chat_id=telegram_id,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=False
            )
            logger.info(f"Sent Telegram message to {telegram_id}")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
    
    def send_job_alert(self, user_id: int, job_id: int):
        """Send job alert to user via Telegram"""
        try:
            with get_db() as db:
                # Get user
                user = db.query(UserProfile).filter_by(id=user_id).first()
                if not user or not user.telegram_id or not user.telegram_notifications:
                    return
                
                # Get alert
                alert = db.query(JobAlert).filter_by(
                    user_id=user_id,
                    job_id=job_id
                ).first()
                
                if not alert:
                    return
                
                job = alert.job
                
                # Format and send message
                message = self.format_job_message(
                    job, 
                    float(alert.match_score),
                    alert.match_reasons
                )
                
                success = self.send_message(user.telegram_id, message)
                
                if success:
                    alert.sent_at = db.func.now()
                    db.commit()
                    
        except Exception as e:
            logger.error(f"Error sending job alert: {e}")
    
    def send_daily_digest(self, user_id: int):
        """Send daily digest of new job matches"""
        try:
            with get_db() as db:
                # Get user
                user = db.query(UserProfile).filter_by(id=user_id).first()
                if not user or not user.telegram_id or not user.telegram_notifications:
                    return
                
                # Get unsent alerts
                alerts = db.query(JobAlert).filter(
                    JobAlert.user_id == user_id,
                    JobAlert.was_opened == False
                ).order_by(JobAlert.match_score.desc()).limit(10).all()
                
                if not alerts:
                    logger.info(f"No new alerts for user {user.email}")
                    return
                
                # Format digest message
                message = f"📊 **Daily Job Digest for {user.full_name or user.email}**\n\n"
                message += f"You have **{len(alerts)} new job matches**:\n\n"
                
                for i, alert in enumerate(alerts, 1):
                    job = alert.job
                    message += f"{i}. **{job.title}** at {job.company_name}\n"
                    message += f"   Match: {int(alert.match_score)}% | Location: {job.location}\n"
                    message += f"   🔗 {job.source_url}\n\n"
                
                self.send_message(user.telegram_id, message)
                
        except Exception as e:
            logger.error(f"Error sending daily digest: {e}")
    
    def bulk_send_digests(self):
        """Send daily digests to all users"""
        try:
            with get_db() as db:
                users = db.query(UserProfile).filter(
                    UserProfile.is_active == True,
                    UserProfile.telegram_notifications == True,
                    UserProfile.notification_frequency == 'daily'
                ).all()
                
                logger.info(f"Sending daily digests to {len(users)} users")
                
                for user in users:
                    self.send_daily_digest(user.id)
                    
        except Exception as e:
            logger.error(f"Error in bulk digest sending: {e}")


