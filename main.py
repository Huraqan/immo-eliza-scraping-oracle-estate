from time import perf_counter

from scraper.deployment import deploy_crawler


if __name__ == "__main__":
    print(
        "\n"
        + "\n================================================================="
        + "\n||                        ORACLE-ESTATE                        ||"
        + "\n================================================================="
        + "\n"
    )

    t = perf_counter()
    

    deploy_crawler()
    
    print("\nFinal time taken to scrape specs on all the properties:", perf_counter() - t)
        
        