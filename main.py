from time import perf_counter

from scraper.data_processing import restructure_data
from scraper.deployment import deploy_crawler

def scrape():
    t = perf_counter()

    deploy_crawler()

    t = perf_counter() - t

    print(
        "\n\nFinal time taken to scrape specs on all the properties:",
        t // 60,
        "minutes and",
        t % 60,
        "seconds.",
    )

if __name__ == "__main__":
    print(
        "\n"
        + "\n================================================================="
        + "\n||                        ORACLE-ESTATE                        ||"
        + "\n================================================================="
        + "\n"
    )

    scrape()
    
    restructure_data()

    print("\n\nThank you for choosing ORACLE-ESTATE!\n\n")
