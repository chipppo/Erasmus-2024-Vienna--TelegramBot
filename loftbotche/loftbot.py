import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import re
import json

class TheLoftEventsSpider(scrapy.Spider):
    name = "theloft_events"
    start_urls = ["https://theloft.at"]

    def __init__(self):
        # Initialize lists to store event data
        self.all_events = []
        self.today_events = []

    def parse(self, response):
        # Define today's date in `YYYY-MM-DD` format for comparison
        today = datetime.today().strftime("%Y-%m-%d")

        # Select each event block
        events = response.css("a[href*='theloft.at']")

        for event in events:
            # Extract relevant fields
            date_text = event.css("div.datum::text").get()
            title = event.css("div.content-middle::text").get()
            link = event.css("::attr(href)").get()

            # Initialize variables
            event_date = None
            event_day = None
            start_date = None
            start_time = None
            end_time = "Late"  # Default if not provided
            lineup = "Various Artists"  # Default if not provided

            if date_text:
                # Remove weekday prefix and parse date
                date_text = re.sub(r'^[A-Za-z]{2,}\.\s*', '', date_text)
                try:
                    event_date_obj = datetime.strptime(date_text, "%d.%m.%Y")
                    event_date = event_date_obj.strftime("%Y-%m-%d")
                    event_day = event_date_obj.strftime("%A")
                    start_date = event_date
                except ValueError:
                    self.logger.error(f"Date format error for: {date_text}")

            # Skip invalid events
            if not (event_date and title and link):
                continue

            # Build event dictionary
            event_data = {
                "title": title.strip(),
                "event_day": event_day,
                "start_date": start_date,
                "start_time": event.css("span.open::text").get(default="TBA").strip(),
                "end_time": end_time,
                "lineup": event.css("div.lineup::text").get(default=lineup).strip(),
                "location": "The Loft",
                "link": response.urljoin(link),
            }

            # Add to the all events list
            self.all_events.append(event_data)

            # Add to today's events list if the date matches
            if event_date == today:
                self.today_events.append(event_data)

    def close(self, reason):
        # Save all events to a JSON file
        with open("theloft_all_events.json", "w", encoding="utf-8") as all_events_file:
            json.dump(self.all_events, all_events_file, ensure_ascii=False, indent=4)

        # Save today's events to a separate JSON file
        with open("theloft_today_events.json", "w", encoding="utf-8") as today_events_file:
            json.dump(self.today_events, today_events_file, ensure_ascii=False, indent=4)

# Configure Scrapy and run the spider
process = CrawlerProcess(settings={
    "LOG_LEVEL": "ERROR"  # Suppress unnecessary log messages
})

process.crawl(TheLoftEventsSpider)
process.start()
