import scrapy
from scrapy.crawler import CrawlerProcess


class ImmoSpider(scrapy.Spider):
    name = "immoweb"
    allowed_domains = ["immoweb.be"]
    start_urls = []
    for x in range(1):
        start_urls.append(f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={x}&orderBy=postal_code")
        # start_urls.append(f"https://www.immoweb.be/en/search/appartement/for-sale?countries=BE&page={x}&orderBy=postal_code")
    
    def parse(self, response):
        for obj in response.css('a.card__title-link'):
            url = response.urljoin(obj.attrib["href"]) #normalize and convert probable relative urls to absolute
            yield response.follow(url, self.parse_property_page) #follow: automatically find urls(extracting hrefs) then sends a request to that URL and then calls the parse_property_page

    def parse_property_page(self, response):
        split_url = response.url[37:].split("/")
        price = response.css("p.classified__price span.sr-only::text").get()
        price = price.replace("€","")
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
    "house"
]

        property_type = "house" if split_url[0] in house_subtypes else "appartment"

        data = {
            "url": response.url,
            "id": int(split_url[4]),
            "locality name": split_url[2],
            "postal code": int(split_url[3]),
            "price": price,
            "property type": property_type,
            "property subtype": split_url[0],
            "type of sale": split_url[1],
        }
        for row in response.css("tbody.classified-table__body"):
            key = row.css("th.classified-table__header::text").get()
            value = row.css("td.classified-table__data::text").get()

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
        "FEED_FORMAT": "csv",
        "FEED_URI": "output.csv",
        "FEEDS": {
            "output.csv": {
                "format": "csv",
                "overwrite": True,
            }
        },
    }

    # Create a CrawlerProcess with the spider and output settings
    process = CrawlerProcess(settings=output_settings)
    process.crawl(ImmoSpider)

    # Start the crawling process
    process.start()

deploy_crawler()

