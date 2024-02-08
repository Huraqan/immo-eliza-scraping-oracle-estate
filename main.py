import json
from time import perf_counter

from scraper.immo_spider import deploy_crawler
from scraper.structure_data import structure_dictionaries, extract_field_names


def structure_data():
    with open("output.json", "r") as file:
        json_content = json.load(file)
        extract_field_names(json_content)
        structure_dictionaries(json_content)


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

    structure_data()

    t = perf_counter() - t

    print(
        "\n\nFinal time taken to scrape specs on all the properties:",
        t // 60,
        "minutes and",
        (t % 60),
        "seconds.",
    )
    print("\n\nThank you for scraping ImmoWeb, they're scammers anyway!\n\n")
