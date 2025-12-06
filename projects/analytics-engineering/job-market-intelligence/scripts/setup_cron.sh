#!/bin/bash
# ============================================================
# CRON JOB SETUP FOR JOB MARKET INTELLIGENCE SCRAPER
# ============================================================
#
# This script sets up automated scraping at regular intervals.
# 
# Default schedule: Every 6 hours (0:00, 6:00, 12:00, 18:00)
#
# Usage:
#   chmod +x scripts/setup_cron.sh
#   ./scripts/setup_cron.sh
#
# To view current cron jobs:
#   crontab -l
#
# To remove this cron job:
#   crontab -e  (then delete the line)
#
# ============================================================

set -e

# Get the absolute path to the project
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="${PROJECT_DIR}/venv/bin/python3"
SCRAPER_SCRIPT="${PROJECT_DIR}/scripts/run_all_scrapers.py"
LOG_DIR="${PROJECT_DIR}/logs"

echo "============================================================"
echo "🕐 Setting up Cron Job for Job Scraper"
echo "============================================================"
echo ""
echo "Project directory: ${PROJECT_DIR}"
echo "Python path: ${VENV_PYTHON}"
echo "Scraper script: ${SCRAPER_SCRIPT}"
echo ""

# Check if files exist
if [ ! -f "${VENV_PYTHON}" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

if [ ! -f "${SCRAPER_SCRIPT}" ]; then
    echo "❌ Scraper script not found!"
    exit 1
fi

# Create logs directory
mkdir -p "${LOG_DIR}"

# Define the cron job (every 6 hours)
CRON_SCHEDULE="0 */6 * * *"
CRON_COMMAND="cd ${PROJECT_DIR} && ${VENV_PYTHON} ${SCRAPER_SCRIPT} >> ${LOG_DIR}/cron_scraper.log 2>&1"

# Check if cron job already exists
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "run_all_scrapers.py" || true)

if [ -n "${EXISTING_CRON}" ]; then
    echo "⚠️  A cron job for this scraper already exists:"
    echo "   ${EXISTING_CRON}"
    echo ""
    read -p "Do you want to replace it? (y/n): " REPLACE
    if [ "${REPLACE}" != "y" ]; then
        echo "Keeping existing cron job."
        exit 0
    fi
    # Remove existing cron job
    crontab -l 2>/dev/null | grep -v "run_all_scrapers.py" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "${CRON_SCHEDULE} ${CRON_COMMAND}") | crontab -

echo ""
echo "✅ Cron job installed successfully!"
echo ""
echo "Schedule: Every 6 hours (0:00, 6:00, 12:00, 18:00)"
echo "Command:  ${CRON_COMMAND}"
echo ""
echo "Logs will be saved to: ${LOG_DIR}/cron_scraper.log"
echo ""
echo "To verify, run: crontab -l"
echo "To remove, run: crontab -e (and delete the line)"
echo ""
echo "============================================================"
echo ""

# Show current crontab
echo "Current cron jobs:"
crontab -l 2>/dev/null || echo "  (none)"
