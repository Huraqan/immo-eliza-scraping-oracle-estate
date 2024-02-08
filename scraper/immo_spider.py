import logging

import scrapy
from scrapy.crawler import CrawlerProcess

url_head = "https://www.immoweb.be/en/search/house/for-sale?countries=BE&page="
url_tail = "&orderBy=postal_code"

house_subtypes = [
    "cungalow",
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

value_mapping = {
    "Yes": 1,
    "No": 0,
    "Not specified": None
}


class ImmoSpider(scrapy.Spider):
    def __init__(self):
        # Suppress massive amounts of annoying log messages
        logging.getLogger("scrapy").setLevel(logging.ERROR)
        self.scrape_counter = 0
    
    name = "immospider"
    allowed_domains = ["immoweb.be"]
    start_urls = []

    for x in range(1, 3):
        start_urls.append(url_head + str(x) + url_tail)

    def parse(self, response):
        print("Parsing search-results page:", response.url)
        
        for obj in response.css("a.card__title-link"):
            # Convert possible relative urls to absolute
            url = response.urljoin(obj.attrib["href"])

            # Followup request that calls parse_property_page()
            yield response.follow(url, self.parse_property_page)

    def parse_property_page(self, response):
        self.scrape_counter += 1
        print("Parsing property page:", self.scrape_counter, "url:", response.url)
        
        split_url = response.url[37:].split("/")
        price = response.css("p.classified__price span.sr-only::text").get()
        price = price.replace("€", "")
        
        property_type = "house" if split_url[0] in house_subtypes else "appartment"

        data = {
            "Url": response.url,
            "Id": int(split_url[4]),
            "Locality name": split_url[2],
            "Postal code": int(split_url[3]),
            "Price": price,
            "Property type": property_type,
            "Property subtype": split_url[0],
            "Type of sale": split_url[1],
            "Fireplaces:": 0,
            "Swimming pool": 0,
            "Kitchen type:": 0,
            "Swimming pool": 0,
        }

        for row in response.css("tr.classified-table__row"):
            key = row.css("th.classified-table__header::text").get()
            value = row.css("td.classified-table__data::text").get()

            if not (key and value):
                continue

            key = key.replace("\n", "").strip()
            value = value.replace("\n", "").strip()

            if not (key and value):
                continue
            
            # Conversions
            try:
                value = int(value)
            except:
                value = value_mapping.get(value, value)
        
            if key == "Kitchen type":
                value = 0 if value == "Not installed" else 1
        
            if key == "How many fireplaces?":
                key = "Fireplaces"
                value = 0 if value == 0 else 1
            
            # Storing data
            data[key] = value
        
        yield data


def deploy_crawler():
    # Specify the output file and format
    output_settings = {
        "FEEDS": {
            "output.json": {
                "format": "json",
                "overwrite": True,
            },
            "output.csv": {
                "format": "csv",
                "overwrite": True,
                "fields_to_export": None,  # No specific field means export all fields
                "export_empty_fields": True,  # Include null values for missing fields
            },
        },
    }

    # Create a CrawlerProcess with the spider and output settings
    process = CrawlerProcess(settings=output_settings)
    process.crawl(ImmoSpider)

    # Start the crawling process
    process.start()