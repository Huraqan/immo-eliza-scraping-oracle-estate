from scrapy.crawler import CrawlerProcess
from scraper.immo_spider import ImmoSpider


<<<<<<< HEAD
def deploy_crawler():
    # Specify the output file and format
    output_settings = {
=======
def deploy_crawler(save_links=False):
    # Specify the output file and format
    scrape_settings = {
>>>>>>> e348691068ab5448c9deefa3138d5cbc5d7544e1
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
<<<<<<< HEAD

    # Create a CrawlerProcess with the spider and output settings
    process = CrawlerProcess(settings=output_settings)
    process.crawl(ImmoSpider)
=======
    
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
>>>>>>> e348691068ab5448c9deefa3138d5cbc5d7544e1

    # Start the crawling process
    process.start()


