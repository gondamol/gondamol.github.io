#!/usr/bin/env python3
"""
CLI script to run job matching for users
"""
import sys
import logging
import argparse
from pathlib import Path

# Add pipeline to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.matching.job_matcher import JobMatcher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run job matching for users')
    parser.add_argument(
        '--min-score',
        type=float,
        default=70.0,
        help='Minimum match score (0-100)'
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting job matching (min score: {args.min_score})")
    
    try:
        matcher = JobMatcher()
        matcher.bulk_match_all_users(min_score=args.min_score)
        logger.info("Job matching completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error during job matching: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())






