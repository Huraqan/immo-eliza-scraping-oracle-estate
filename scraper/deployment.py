from scrapy.crawler import CrawlerProcess
from scraper.immo_spider import ImmoSpider


def deploy_crawler():
    # Specify the output file and format
    output_settings = {
        "FEEDS": {
            "data/raw/output.csv": {
                "format": "csv",
                "overwrite": True,
                "fields_to_export": None,  # Export all fields
                "export_empty_fields": True,  # Include null values for missing fields
            },
            "data/raw/output.json": {
                "format": "json",
                "overwrite": True,
            }
        }
        # "DOWNLOAD_DELAY": uniform(0.2, 0.9) # Set the delay 
    }

    # Create a CrawlerProcess with the spider and output settings
    process = CrawlerProcess(settings=output_settings)
    process.crawl(ImmoSpider)

    # Start the crawling process
    process.start()


