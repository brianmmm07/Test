"""Scheduler for running daily paper summaries."""
import schedule
import time
from datetime import datetime
from config import Config
from main import run_daily_summary

def job():
    """Wrapper for the daily summary job."""
    print(f"\nStarting scheduled job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        run_daily_summary()
    except Exception as e:
        print(f"Error in scheduled job: {e}")

def main():
    """Run the scheduler."""
    try:
        Config.validate()
        print("arXiv Paper Summarizer - Scheduler")
        print(f"Scheduled to run daily at {Config.SCHEDULE_TIME}")
        print("Press Ctrl+C to stop\n")

        # Schedule the job
        schedule.every().day.at(Config.SCHEDULE_TIME).do(job)

        # Run immediately on start
        print("Running initial summary...")
        job()

        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    except KeyboardInterrupt:
        print("\nScheduler stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
