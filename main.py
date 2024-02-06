import json
from random import uniform
from time import perf_counter, sleep

from pandas import DataFrame
from requests import Session

from scraper.scraper import ImmoWebScraper
from scrapy_test import deploy_crawler


def scrape_urls():
    with Session() as session:
        scraper = ImmoWebScraper(session)
        
        for i in range(10):
            print(f"Getting urls on page: {i}")
            scraper.scrape_property_urls(f"https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&page={i}&orderBy=postal_code")
            sleep(uniform(0.2, 0.9))
    
    scraper.property_urls_to_txt()
    
    return scraper

if __name__ == "__main__":
    print(
        "\n"
        + "\n================================================================="
        + "\n||                        ORACLE-ESTATE                        ||"
        + "\n================================================================="
        + "\n"
    )
    
    scraper = scrape_urls()
    
    print(f"\nDONE GETTING URLS. TOTAL PROPERTY URL COUNT: {len(scraper.property_urls)}")
    sleep(0.5)
    print("\nGETTING SPECS WITH SCRAPY...\n")
    sleep(0.5)
    
    t = perf_counter()
    deploy_crawler()
    
    with open("output.json", "r") as json_file:
        json_content = json.load(json_file)
        
        with open("output.csv", "w", newline="", encoding="utf-8") as csv_file:
            scraper.to_csv_file(json_content, csv_file)
        
        data = DataFrame.from_dict(json_content)
        
        # print(data)
    
    
    print(f"\nFinal time taken to scrape and parse specs on {len(scraper.property_urls)} properties:", perf_counter() - t)
        
        