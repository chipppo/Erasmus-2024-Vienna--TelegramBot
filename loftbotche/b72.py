import scrapy
from scrapy.crawler import CrawlerProcess
import re
from datetime import datetime

class B72EventsSpider(scrapy.Spider):
    name = "b72_events"
    start_urls = ["https://www.b72.at/program"]

    def parse(self, response):
        # Get today's date in 'YYYY-MM-DD' format
        today = datetime.now().strftime("%Y-%m-%d")

        # Select each event block
        events = response.css("div.col.l4.m6.s12.coming-up")

        for event in events:
            # Extract event details
            link = event.css("a::attr(href)").get()
            title = event.css("h6.too-much-text a::text").get()
            date_text = event.css("h4::text").get()  # Date format DD.MM

            # Verify all required data is present
            if not (link and title and date_text):
                continue

            # Transform the date format and check if it matches today
            event_date = self.parse_date(date_text)
            if event_date != today:
                continue  # Skip events that are not scheduled for today

            # Construct the full URL for the event link
            full_link = response.urljoin(link)

            # Yield the event data for today's events only
            yield {
                "date": event_date,
                "title": title.strip(),
                "link": full_link
            }

    def parse_date(self, date_text):
        """
        Parse the date text in the format "DD.MM" and return it as "YYYY-MM-DD".
        Assumes year 2024.
        """
        try:
            # Append the assumed year
            full_date_text = f"{date_text}.2024"
            # Convert to 'YYYY-MM-DD' format
            event_date_obj = datetime.strptime(full_date_text, "%d.%m.%Y")
            return event_date_obj.strftime("%Y-%m-%d")
        except ValueError:
            self.logger.error(f"Date parsing failed for: {date_text}")
            return None

# Configure Scrapy to output to a JSON file for today's events only
process = CrawlerProcess(settings={
    "FEEDS": {
        "b72_events_today.json": {
            "format": "json",
            "encoding": "utf8",
            "overwrite": True,
        },
    },
    "LOG_LEVEL": "INFO"
})

process.crawl(B72EventsSpider)
process.start()
