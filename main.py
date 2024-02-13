from time import perf_counter
<<<<<<< HEAD

from scraper.data_processing import restructure_data
from scraper.deployment import deploy_crawler
=======

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
>>>>>>> e348691068ab5448c9deefa3138d5cbc5d7544e1

if __name__ == "__main__":
    print(
        "\n"
        + "\n================================================================="
        + "\n||                        ORACLE-ESTATE                        ||"
        + "\n================================================================="
        + "\n"
    )

<<<<<<< HEAD
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
=======
    scrape()
>>>>>>> e348691068ab5448c9deefa3138d5cbc5d7544e1
    
    restructure_data()

    print("\n\nThank you for choosing ORACLE-ESTATE!\n\n")
