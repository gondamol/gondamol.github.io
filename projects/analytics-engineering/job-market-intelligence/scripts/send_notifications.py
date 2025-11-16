#!/usr/bin/env python3
"""
CLI script to send job notifications
"""
import sys
import logging
import argparse
from pathlib import Path

# Add pipeline to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.notifications.telegram_bot import TelegramNotifier

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Send job notifications')
    parser.add_argument(
        '--digest',
        action='store_true',
        help='Send daily digests instead of individual alerts'
    )
    
    args = parser.parse_args()
    
    logger.info("Starting notification sending")
    
    try:
        notifier = TelegramNotifier()
        
        if args.digest:
            logger.info("Sending daily digests")
            notifier.bulk_send_digests()
        else:
            logger.info("Individual alerts not implemented yet")
            logger.info("Use --digest to send daily digests")
        
        logger.info("Notification sending completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error sending notifications: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())






