import logging

import scrapy
import re


search_pages_to_scrape = 333

url_head = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
url_tail = "&orderBy=postal_code"

value_mapping = {
    "Yes": 1,
    "No": 0,
    "Not specified": None
}

house_subtypes = [
    "bungalow",
    "chalet",
    "castle",
    "farmhouse",
    "country-house",
    "exceptional-property",
    "apartment-block",
    "mixed-use-building",
    "town-house",
    "mansion",
    "villa",
    "other-properties",
    "manor-house",
    "pavilion",
    "house",
]

compiled_price_pattern = re.compile("[0-9]+")

class ImmoSpider(scrapy.Spider):
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
        
        for obj in response.css("a.card__title-link"):
            # Convert possible relative urls to absolute
            url = response.urljoin(obj.attrib["href"])
            
            # Skip buildings with various separate listings
            if (
                "new-real-estate-project-apartments" in url
                or "new-real-estate-project-houses" in url
            ):
                continue
            
            if self.save_links:
                yield url
                continue
            
            # Followup request that calls parse_property_page()
            yield response.follow(url, self.parse_property_page)

    def parse_property_page(self, response):
        self.scrape_counter += 1
        print(f"Parsing property page {self.scrape_counter}, url: {response.url}")
        
        property_dictionary = self.get_immo_dictionary(response)
                
        self.fill_attributes(response, property_dictionary)
        
        yield property_dictionary

    # classified__information--address-row ???? dynamically loaded
    
    def get_immo_dictionary(self, response) -> dict:
        split_url = response.url[37:].split("/")
        
        price = response.css("p.classified__price span.sr-only::text").get()
        # price = int(compiled_price_pattern.findall(price)[0])
        
        property_type = "house" if split_url[0] in house_subtypes else "apartment"
        
        property_dictionary = {
            "Url": response.url,
            "Property ID": split_url[4],
            "Locality name": split_url[2],
            "Postal code": split_url[3],
            "Price": price,
            "Type of property": property_type,
            "Subtype of property": split_url[0],
            "Type of sale": split_url[1],
            "Bedrooms": None,
            "Living area": None,
            "Kitchen type": 1,
            "Furnished": 0,
            "How many fireplaces?": 0,
            "Terrace surface": None,
            "Garden surface": None,
            "Surface of the plot": None,
            "Number of frontages": None,
            "Swimming pool": 0,
            "Building condition": None,
        }
        
        return property_dictionary
    
    def fill_attributes(self, response, property_dictionary):
        
        for row in response.css("tr.classified-table__row"):
            key = row.css("th.classified-table__header::text").get()
            value = row.css("td.classified-table__data::text").get()

            if not (key and value):
                continue

            key = key.replace("\n", "").strip()
            value = value.replace("\n", "").strip()

            if not (key and value):
                continue

            try:
                value = int(value) if key not in ["Property ID", "Postal code", "External reference"] else value
            except ValueError:
                value = value_mapping.get(value, value)
            
            if key == "Kitchen type":
                value = 0 if value == "Not installed" else 1
            
            if key == "How many fireplaces?":
                value = 0 if value == 0 else 1

            # if key in allowed_field_names:
            property_dictionary[key] = value
            
            