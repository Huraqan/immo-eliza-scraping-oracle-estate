import scrapy
from scrapy.crawler import CrawlerProcess


class ImmoSpider(scrapy.Spider):
    name = "immoweb"
    allowed_domains = ["immoweb.be"]
    start_urls = []
    for x in range(333):
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
            "Bedrooms": None,
            "Living area" : None,
            "Kitchen type": 1,
            "Furnished": 0,
            "Open fire": 0,
            "Terrace surface": None,
            "Garden surface": None,#sometimes in description only
            "Surface of the plot": None,
            "Number of facades": None, #from description
            "Swimming pool": 0,
            "Building condition": None

        }
        for row in response.css("tr.classified-table__row"):
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
                    "Not specified": None,

                }

                # Convert value using the dictionary mapping
                value = value_mapping.get(value, value)
            if key == "Kitchen type":
                value = 0 if value == "Not installed" else 1

            if key in data.keys():
                data[key] = value


            print(f"Key: {key}, Value: {value}")

        yield data
        
def deploy_crawler():
    # Specify the output file and format
    output_settings = {
        "FEEDS": {
            "output.csv": {
                "format": "csv",
                "overwrite": True,
                "fields_to_export": None,  # Export all fields
                "export_empty_fields": True,  # Include null values for missing fields
            },
            "output.json": {
                "format": "json",
                "overwrite": True,
            },
        },
        "DOWNLOAD_DELAY": 2,  # Set the delay to 2 seconds between requests
    }

    # Create a CrawlerProcess with the spider and output settings
    process = CrawlerProcess(settings=output_settings)
    process.crawl(ImmoSpider)

    # Start the crawling process
    process.start()