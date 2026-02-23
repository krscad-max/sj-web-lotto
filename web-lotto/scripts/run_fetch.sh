#!/bin/bash
# Run the magayo fetcher (intended for cron)
# Load .env if present so TELEGRAM_BOT_TOKEN/CHAT_ID are available
cd "$(dirname "$0")"
if [ -f ../.env ]; then
  export $(grep -v '^#' ../.env | xargs)
fi
python3 fetch_magayo.py >> ../logs/fetch_magayo.log 2>&1
