import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime

class ViperRoomEventsSpider(scrapy.Spider):
    name = "viper_room_events"
    start_urls = ["https://www.viper-room.at/veranstaltungen"]

    def parse(self, response):
        # Get today's date in 'YYYY-MM-DD' format
        today = datetime.now().strftime("%Y-%m-%d")

        # Select each event block
        events = response.css("li")

        for event in events:
            # Extract event details
            link = event.css("h2.event_title a::attr(href)").get()
            title = event.css("h2.event_title a::text").get()
            date_day = event.css("div.event_date_day::text").get()
            date_monthyear = event.css("div.event_date_monthyear::text").get()
            start_time = event.css("div.event_time_start::text").get()

            # Verify all required data is present
            if not (link and title and date_day and date_monthyear):
                continue

            # Transform the date format and check if it matches today
            event_date = self.parse_date(date_day, date_monthyear)
            if event_date != today:
                continue  # Skip events that are not scheduled for today

            # Construct the full URL for the event link
            full_link = response.urljoin(link)

            # Yield the event data for today's events only, including the fixed location
            yield {
                    "date": event_date,
                    "title": title.strip(),
                    "link": full_link,
                    "location": "Viper Room",  # Fixed location value
            }

    def parse_date(self, date_day, date_monthyear):
        """
        Parse the date text in the format "DD.MM.YY" and return it as "YYYY-MM-DD".
        Assumes year 2024.
        """
        try:
            # Combine day and month/year and append the assumed year
            full_date_text = f"{date_day}.{date_monthyear} 2024"
            # Convert to 'YYYY-MM-DD' format
            event_date_obj = datetime.strptime(full_date_text, "%d.%m.%Y")
            return event_date_obj.strftime("%Y-%m-%d")
        except ValueError:
            self.logger.error(f"Date parsing failed for: {date_day} {date_monthyear}")
            return None

# Configure Scrapy to output to a JSON file for today's events only
process = CrawlerProcess(settings={
    "FEEDS": {
        "viper_room_events_today.json": {
            "format": "json",
            "encoding": "utf8",
            "overwrite": True,
        },
    },
    "LOG_LEVEL": "INFO"
})

process.crawl(ViperRoomEventsSpider)
process.start()
