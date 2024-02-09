from scrapy.crawler import CrawlerProcess
from scraper.immo_spider import ImmoSpider


def deploy_crawler(save_links=False):
    # Specify the output file and format
    scrape_settings = {
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
    
    # Setting for saving urls to txt
    url_settings = {
        "FEEDS": {
            "data/urls.json": {
                "format": "json",
                "overwrite": True,
            }
        }
        # "DOWNLOAD_DELAY": uniform(0.2, 0.9) # Set the delay 
    }

    # Create a CrawlerProcess with the spider and output settings
    process = CrawlerProcess(settings=url_settings if save_links else scrape_settings)
    process.crawl(ImmoSpider, save_links)

    # Start the crawling process
    process.start()


