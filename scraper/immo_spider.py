import logging

import scrapy
from scraper.utils import get_immo_dictionary
from scraper.data_processing import fill_attributes


search_pages_to_scrape = 5

url_head = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
url_tail = "&orderBy=postal_code"

class ImmoSpider(scrapy.Spider):
    def __init__(self):
        # Suppress massive amounts of annoying log messages
        logging.getLogger("scrapy").setLevel(logging.ERROR)
        self.scrape_counter = 0
    
    name = "immospider"
    allowed_domains = ["immoweb.be"]
    start_urls = []

    for x in range(1, search_pages_to_scrape + 1):
        start_urls.append(url_head + str(x) + url_tail)

    def parse(self, response):
        print("Parsing search-results page:", response.url)
        
        for obj in response.css("a.card__title-link"):
            # Convert possible relative urls to absolute
            url = response.urljoin(obj.attrib["href"])
            
            # Skip buildings with various separate listings
            if (
                "new-real-estate-project-apartments" in url
                or "new-real-estate-project-houses" in url
            ):
                continue

            # Followup request that calls parse_property_page()
            yield response.follow(url, self.parse_property_page)

    def parse_property_page(self, response):
        self.scrape_counter += 1
        print("Parsing property page:", self.scrape_counter, "url:", response.url)

        property_dictionary = get_immo_dictionary(response)
                
        fill_attributes(response, property_dictionary)
        
        yield property_dictionary

