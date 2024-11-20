import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import json

class OClubEventsSpider(scrapy.Spider):
    name = "oclub_events"
    start_urls = ["https://o-klub.at/events/"]

    # Month mapping from abbreviation to numeric value
    month_mapping = {
        "JAN": "01",
        "FEB": "02",
        "MAR": "03", 
        "APR": "04",
        "MAI": "05",  
        "JUN": "06",
        "JUL": "07",
        "AUG": "08",
        "SEPT": "09",
        "OCT": "10",  
        "NOV": "11",
        "DEZ": "12",  
    }

    def parse(self, response):
        # Get today's date in 'YYYY-MM-DD' format
        today = datetime.now().strftime("%Y-%m-%d")

        # Initialize lists for today's events and all events
        all_events = []
        today_events = []

        # Initialize a set to track already added events (to avoid duplicates)
        seen_events = set()

        # Select event blocks (adjusting XPath based on the provided structure)
        events = response.xpath('//div[contains(@class, "e-con-inner")]')

        for event in events:
            # Extract title, day, and month using XPath
            title = event.xpath('.//h3[contains(@class, "elementor-heading-title")]/text()').get()
            day = event.xpath('.//div[@id="day"]//div[contains(@class, "elementor-widget-container")]/text()').get()
            month = event.xpath('.//div[@id="month"]//div[contains(@class, "elementor-widget-container")]/text()').get()
            link = event.xpath('.//a[contains(@class, "elementor-button-link")]/@href').get()

            # Check if all necessary data is present
            if not (title and day and month and link):
                continue

            # Clean up the extracted data
            title = title.strip()
            day = day.strip()
            month = month.strip()

            # Format the event date as 'YYYY-MM-DD'
            event_date = self.format_date(day, month)
            full_link = response.urljoin(link)

            # Create a unique identifier for each event (title + date)
            event_identifier = (title, event_date)

            # Check if the event has already been seen (duplicate check)
            if event_identifier in seen_events:
                continue  # Skip this event if it's a duplicate

            # Add the event identifier to the seen set to track it
            seen_events.add(event_identifier)

            # Event data
            event_data = {
                "date": event_date,
                "title": title,
                "link": full_link,
                "location": "O-Club",  # Fixed location
            }

            # Add to all events
            all_events.append(event_data)

            # Add to today's events if the date matches
            if event_date == today:
                today_events.append(event_data)

        # Write all events to JSON
        self.write_to_json(all_events, "oclub_all_events.json")

        # Write today's events to JSON
        self.write_to_json(today_events, "oclub_events_today.json")

    def format_date(self, day, month):
        """
        Format the event date into 'YYYY-MM-DD' based on the month.
        Assumes year 2024 for NOV and DEC, else 2025.
        """
        # Map month abbreviation to the numeric month
        month_number = self.month_mapping.get(month.upper(), None)
        if not month_number:
            self.logger.error(f"Invalid month abbreviation: {month}")
            return None

        # Determine the year
        current_year = datetime.now().year
        if month in ["NOV", "DEZ"]:
            year = 2024  # Assume 2024 for November and December
        else:
            year = 2025  # Assume 2025 for other months

        # Format the date to 'YYYY-MM-DD'
        try:
            event_date = datetime.strptime(f"{day}.{month_number}.{year}", "%d.%m.%Y").strftime("%Y-%m-%d")
            return event_date
        except ValueError:
            self.logger.error(f"Failed to parse date: {day}.{month_number}.{year}")
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

process.crawl(OClubEventsSpider)
process.start()
