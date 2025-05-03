import schedule
import time
import subprocess

def run_scraper():
    print("🔄 Running scraper...")
    # Run the scraper script
    subprocess.run(["python", "scraper/scraper.py"])
    print("✅ Scraper run complete.")

# Schedule the scraper to run once every 24 hours
schedule.every(24).hours.do(run_scraper)

print("🔔 Scheduler started. Scraper will run every 24 hours.")

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
