import scrapy

class EventsSpider(scrapy.Spider):
    name = "events"
    start_urls = ["https://www.daswerk.org/programm/"]


    def parse(self, response):
        # Select each event block based on the HTML structure
        events = response.css("div.col-lg-10")

        for event in events:
            yield {
                "date": event.css("ul.preview-item--information li::text").get(),  # Extracts the first list item as the date
                "title": event.css("h2.preview-item--headline::text").get(),  # Gets the title from the h2 element
                "link": event.css("a.preview-item--link::attr(href)").get(),  # Gets the href attribute for the link
            }