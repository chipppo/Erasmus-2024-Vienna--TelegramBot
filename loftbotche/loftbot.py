import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import re

class TheLoftEventsSpider(scrapy.Spider):
    name = "theloft_events"
    start_urls = ["https://theloft.at"]

    def parse(self, response):
        # Define today's date in `YYYY-MM-DD` format for comparison
        today = datetime.today().strftime("%Y-%m-%d")

        # Select each event block
        events = response.css("a[href*='theloft.at']")

        for event in events:
            # Extract date, title, and link
            date_text = event.css("div.datum::text").get()
            title = event.css("div.content-middle::text").get()
            link = event.css("::attr(href)").get()

            # Transform date_text to a comparable format
            event_date = None
            event_day = None
            start_date = None
            start_time = None
            end_time = None
            lineup = None  # Optional: lineup or artist list, if available

            if date_text:
                # Remove weekday prefix
                date_text = re.sub(r'^[A-Za-z]{2,}\.\s*', '', date_text)
                try:
                    event_date_obj = datetime.strptime(date_text, "%d.%m.%Y")
                    event_date = event_date_obj.strftime("%Y-%m-%d")
                    event_day = event_date_obj.strftime("%A")
                    start_date = event_date
                except ValueError:
                    self.logger.error(f"Date format error for: {date_text}")

            # Check if today's date matches the event date
            if event_date == today and title and link:
                # Assuming time and lineup info might be available in other tags, modify as needed
                start_time = event.css("span.open::text").get() or "TBA"
                end_time = "Late"  # Default if not provided
                lineup = event.css("div.lineup::text").get() or "Various Artists"  # Adjust based on actual HTML structure

                # Output event data with all required fields
                yield {
                    "title": title,
                    "event_day": event_day,
                    "start_date": start_date,
                    "start_time": start_time,
                    "end_time": end_time,
                    "lineup": lineup,
                    "location": "SASS Music Club",  # Static info
                    "link": link,
                }

# Configure Scrapy to output results to a JSON file
process = CrawlerProcess(settings={
    "FEEDS": {
        "theloft_today_events.json": {
            "format": "json",
            "encoding": "utf8",
            "overwrite": True,
        },
    },
    "LOG_LEVEL": "ERROR"
})

process.crawl(TheLoftEventsSpider)
process.start()
