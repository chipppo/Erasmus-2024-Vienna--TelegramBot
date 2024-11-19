import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

class B72EventsSpider(scrapy.Spider):
    name = "b72_events"
    start_urls = ["https://www.b72.at/program"]

    def parse(self, response):
        # Get today's date in 'YYYY-MM-DD' format
        today = datetime.now().strftime("%Y-%m-%d")

        # Initialize lists for today's events and all events
        all_events = []
        today_events = []

        # Select event blocks
        events = response.css("div.col.l4.m6.s12.coming-up")

        for event in events:
            # Extract details
            title = event.css("h6.too-much-text a::text").get()
            date = event.css("h4::text").get()
            link = event.css("h6.too-much-text a::attr(href)").get()

            # Verify all required data is present
            if not (title and date and link):
                continue

            # Parse date to 'YYYY-MM-DD' format
            event_date = self.parse_date(date)
            full_link = response.urljoin(link)

            # Event data
            event_data = {
                "date": event_date,
                "title": title.strip(),
                "link": full_link,
                "location": "B72",  # Fixed location
            }

            # Add to all events
            all_events.append(event_data)

            # Add to today's events if the date matches
            if event_date == today:
                today_events.append(event_data)

        # Write all events to JSON
        self.write_to_json(all_events, "b72_all_events.json")

        # Write today's events to JSON
        self.write_to_json(today_events, "b72_events_today.json")

    def parse_date(self, date_text):
        """
        Convert date from 'DD.MM' format to 'YYYY-MM-DD', assuming the year is 2024.
        """
        try:
            return datetime.strptime(f"{date_text}.2024", "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            self.logger.error(f"Failed to parse date: {date_text}")
            return None

    def write_to_json(self, data, filename):
        """
        Write the given data to a JSON file.
        """
        import json
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

# Configure and run the Scrapy spider
process = CrawlerProcess(settings={
    "LOG_LEVEL": "INFO"
})

process.crawl(B72EventsSpider)
process.start()
