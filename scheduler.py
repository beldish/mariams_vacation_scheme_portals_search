#!/usr/bin/env python3
"""
Scheduler for Vacation Scheme Search Agent

This script runs the search agent every Monday at 7:00 AM London time.
"""

import schedule
import time
import configparser
from datetime import datetime
from search_agent import VacationSchemeSearchAgent


def run_search_job():
    """Run the vacation scheme search job."""
    try:
        print(f"\n{'='*60}")
        print(f"Scheduled job triggered at {datetime.now()}")
        print(f"{'='*60}\n")
        
        agent = VacationSchemeSearchAgent()
        agent.run()
        
        print(f"\n{'='*60}")
        print(f"Job completed at {datetime.now()}")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"Error in scheduled job: {str(e)}")


def main():
    """Main scheduler function."""
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    # Get schedule settings
    schedule_time = config.get('search', 'schedule_time', fallback='07:00')
    schedule_day = config.get('search', 'schedule_day', fallback='monday').lower()
    timezone_str = config.get('search', 'timezone', fallback='Europe/London')
    
    print(f"Vacation Scheme Search Agent Scheduler")
    print(f"{'='*60}")
    print(f"Schedule: Every {schedule_day.title()} at {schedule_time} {timezone_str}")
    print(f"{'='*60}\n")
    
    # Schedule the job using dictionary mapping
    day_mapping = {
        'monday': schedule.every().monday,
        'tuesday': schedule.every().tuesday,
        'wednesday': schedule.every().wednesday,
        'thursday': schedule.every().thursday,
        'friday': schedule.every().friday,
        'saturday': schedule.every().saturday,
        'sunday': schedule.every().sunday
    }
    
    scheduler_obj = day_mapping.get(schedule_day)
    if scheduler_obj:
        scheduler_obj.at(schedule_time).do(run_search_job)
    else:
        print(f"Invalid schedule day: {schedule_day}. Defaulting to Monday.")
        schedule.every().monday.at(schedule_time).do(run_search_job)
    
    print(f"Scheduler started at {datetime.now()}")
    print("Waiting for scheduled time...")
    print("Press Ctrl+C to stop the scheduler\n")
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")


if __name__ == "__main__":
    main()
