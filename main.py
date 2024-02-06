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
        
        for i in range(333):
            print(f"Getting urls on page: {i}")
            scraper.scrape_property_urls(f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={i}&orderBy=postal_code")
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
    
    print("\nDONE GETTING URLS.")
    sleep(0.5)
    print("\nGETTING SPECS WITH SCRAPY...\n")
    sleep(0.5)
    
    t = perf_counter()
    deploy_crawler()
    
    with open("output.json", "r") as file:
        content = json.load(file)
        
        data = DataFrame.from_dict(content)
        
        # print(data)
    
    print("\nFinal time taken to scrape specs on 3000 properties:", perf_counter() - t)
        
        