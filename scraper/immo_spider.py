import logging

import scrapy
from scraper.utils import get_immo_dictionary
from scraper.data_processing import fill_attributes

<<<<<<< HEAD

search_pages_to_scrape = 5
=======
search_pages_to_scrape = 100
>>>>>>> e348691068ab5448c9deefa3138d5cbc5d7544e1

url_head = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
url_tail = "&orderBy=postal_code"

class ImmoSpider(scrapy.Spider):
<<<<<<< HEAD
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
=======
    name = "immospider"
    allowed_domains = ["immoweb.be"]
    start_urls = [url_head + str(i) + url_tail for i in range(search_pages_to_scrape)]
        
    # for x in range(1, search_pages_to_scrape + 1):
    #     start_urls.append(url_head + str(x) + url_tail)
    
    def __init__(self, save_links):
        # Suppress massive amounts of annoying log messages
        logging.getLogger("scrapy").setLevel(logging.ERROR)
        self.page_scrape_counter = 0
        self.scrape_counter = 0
        self.save_links = save_links

    def parse(self, response):
        self.page_scrape_counter += 1
        print(f"Parsing search-results page {self.page_scrape_counter}: {response.url}")
>>>>>>> e348691068ab5448c9deefa3138d5cbc5d7544e1
        
        for obj in response.css("a.card__title-link"):
            # Convert possible relative urls to absolute
            url = response.urljoin(obj.attrib["href"])
            
            # Skip buildings with various separate listings
            if (
                "new-real-estate-project-apartments" in url
                or "new-real-estate-project-houses" in url
            ):
                continue
<<<<<<< HEAD

=======
            
            if self.save_links:
                yield url
                continue
            
>>>>>>> e348691068ab5448c9deefa3138d5cbc5d7544e1
            # Followup request that calls parse_property_page()
            yield response.follow(url, self.parse_property_page)

    def parse_property_page(self, response):
        self.scrape_counter += 1
<<<<<<< HEAD
        print("Parsing property page:", self.scrape_counter, "url:", response.url)

=======
        print(f"Parsing property page {self.scrape_counter}, url: {response.url}")
        
>>>>>>> e348691068ab5448c9deefa3138d5cbc5d7544e1
        property_dictionary = get_immo_dictionary(response)
                
        fill_attributes(response, property_dictionary)
        
        yield property_dictionary

