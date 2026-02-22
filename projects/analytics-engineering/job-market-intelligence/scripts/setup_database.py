#!/usr/bin/env python3
"""
Setup database schema
"""
import sys
import logging
from pathlib import Path

# Add pipeline to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pipeline.database.connection import init_db

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    logger.info("Initializing database...")
    
    try:
        init_db()
        logger.info("✓ Database initialized successfully")
        logger.info("Tables created and ready for use")
        return 0
    except Exception as e:
        logger.error(f"✗ Error initializing database: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())






