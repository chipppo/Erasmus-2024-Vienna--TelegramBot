import scrapy
from scrapy.crawler import CrawlerProcess
import re
import json
from datetime import datetime

class ViperRoomEventsSpider(scrapy.Spider):
    name = "viperroom_events"
    start_urls = ["https://www.viper-room.at/veranstaltungen"]

    def parse(self, response):
        # Get today's date in 'YYYY-MM-DD' format
        today = datetime.now().strftime("%Y-%m-%d")

        # Initialize lists for today's events and all events
        all_events = []
        today_events = []

        # Select event blocks (li tags)
        events = response.css("li")

        for event in events:
            # Extract details from the event
            title = event.css("div.event_text h2.event_title a::text").get()
            date_text = event.css("div.event_datetime div.event_date_monthyear::text").get()
            link = event.css("div.event_text h2.event_title a::attr(href)").get()

            # Verify all required data is present
            if not (title and date_text and link):
                continue

            # Parse the date using regex
            event_date = self.parse_date(date_text.strip())
            if not event_date:
                continue

            full_link = response.urljoin(link)

            # Event data structure
            event_data = {
                "date": event_date,
                "title": title.strip(),
                "link": full_link,
                "location": "Viper Room",  # Fixed location
            }

            # Add to all events
            all_events.append(event_data)

            # Add to today's events if the date matches
            if event_date == today:
                today_events.append(event_data)

        # Write all events to JSON
        self.write_to_json(all_events, "viperroom_all_events.json")

        # Write today's events to JSON
        self.write_to_json(today_events, "viperroom_events_today.json")

    def parse_date(self, date_text):
        """
        Extracts and converts a date from 'DD.MM.YY' format to 'YYYY-MM-DD' using regex.
        """
        match = re.match(r"(\d{2})\.(\d{2})\.(\d{2})", date_text)
        if match:
            day, month, year = match.groups()
            year_full = f"20{year}"  # Convert 'YY' to '20YY'
            return f"{year_full}-{month}-{day}"  # Return 'YYYY-MM-DD'
        else:
            self.logger.error(f"Failed to parse date: {date_text}")
            return None

    def write_to_json(self, data, filename):
        """
        Write the given data to a JSON file.
        """
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# Configure and run the Scrapy spider
process = CrawlerProcess(settings={
    "LOG_LEVEL": "INFO"
})

process.crawl(ViperRoomEventsSpider)
process.start()
