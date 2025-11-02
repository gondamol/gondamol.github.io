#!/usr/bin/env python3
"""
CLI script to extract skills from job descriptions
"""
import sys
import logging
import argparse
from pathlib import Path

# Add pipeline to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.nlp.skill_extractor import SkillExtractor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Extract skills from job descriptions')
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of jobs to process'
    )
    
    args = parser.parse_args()
    
    logger.info("Starting skill extraction")
    
    try:
        extractor = SkillExtractor()
        extractor.bulk_process_jobs(limit=args.limit)
        logger.info("Skill extraction completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error during skill extraction: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())





