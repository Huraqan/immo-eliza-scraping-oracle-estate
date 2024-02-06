import logging

import scrapy
from scrapy.crawler import CrawlerProcess


class ImmoSpider(scrapy.Spider):
    name = "immoweb"
    
    def __init__(self, ):
        logging.getLogger('scrapy').setLevel(logging.CRITICAL)
        
        with open("urls.txt") as f:
            self.start_urls = f.readlines()

    def parse(self, response):
        print("Parsing:", response.url)
        split_url = response.url[37:].split("/")
        
        price = response.css("p.classified__price span.sr-only::text").get()
        price = price.replace("€","")
        
        data = {
            "url": response.url,
            "id": int(split_url[4]),
            "locality name": split_url[2],
            "postal code": int(split_url[3]),
            "price": price,
            "property type": split_url[0],
            "property subtype": "",
            "type of sale": split_url[1],
        }
        
        for quote in response.css("tr.classified-table__row"):
            key = quote.css("th.classified-table__header::text").get()
            value = quote.css("td.classified-table__data::text").get()
            
            if not (key and value): continue
            
            key = key.replace("\n", "").strip()
            value = value.replace("\n", "").strip()
            
            if not (key and value): continue
            
            try:
                value = int(value)
            except:
                # Define the dictionary mapping
                value_mapping = {
                    "Yes": 1,
                    "No": 0,
                    "Not specified": None
                }

                # Convert value using the dictionary mapping
                value = value_mapping.get(value, value)

            data[key] = value
        
        yield data

def deploy_crawler():
    # Specify the output file and format
    output_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": "output.json",
        "FEEDS": {
            "output.json": {
                "format": "json",
                "overwrite": True,
            }
        },
    }

    # Create a CrawlerProcess with the spider and output settings
    process = CrawlerProcess(settings=output_settings)
    process.crawl(ImmoSpider)

    # Start the crawling process
    process.start()
