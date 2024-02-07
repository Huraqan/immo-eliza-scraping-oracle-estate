import json
from random import uniform
from time import perf_counter, sleep

from pandas import DataFrame
from requests import Session


from scraper.scrapy_test import deploy_crawler


if __name__ == "__main__":
    print(
        "\n"
        + "\n================================================================="
        + "\n||                        ORACLE-ESTATE                        ||"
        + "\n================================================================="
        + "\n"
    )

    t = perf_counter()
    # for x in range(333):
    #     start_urls.append(f"https://www.immoweb.be/en/search/house/for-sale?countries=BE&page={x}&orderBy=postal_code")
    #     # start_urls.append(f"https://www.immoweb.be/en/search/appartement/for-sale?countries=BE&page={x}&orderBy=postal_code")

    # deploy_crawler()

    # for x in range(333):
    #     start_urls.append(f"https://www.immoweb.be/en/search/appartement/for-sale?countries=BE&page={x}&orderBy=postal_code")

    deploy_crawler()
    
    with open("output.json", "r") as file:
        content = json.load(file)
        
        data = DataFrame.from_dict(content)
        
        # print(data)
    
    print("\nFinal time taken to scrape specs on all the properties:", perf_counter() - t)
        
        