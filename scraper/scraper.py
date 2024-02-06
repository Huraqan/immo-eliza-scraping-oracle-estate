from csv import DictWriter
from bs4 import BeautifulSoup

# from pandas import DataFrame
from requests import Session


class ImmoWebScraper:
    """
    ImmoWebScraper class for scraping data from the real-estate website www.immoweb.be.
    """

    def __init__(self, session: Session):
        self.base_url: str = "www.immoweb.be/"
        self.data_dict: dict = {}
        self.property_urls: set = set()
        self.session: Session = session

    def make_simple_request(self, url: str):
        print("url:", url)
        return self.session.get(url)

    def scrape_property_urls(self, url: str) -> None:
        req = self.make_simple_request(url)

        if req.status_code != 200:
            print("\nPAGE NOT FOUND!!!\n")

        soup = BeautifulSoup(req.content, "html.parser")

        property_urls = soup.find_all(
            name="a", attrs={"class": "card__title-link"}, href=True
        )

        links_set = set()
        for property_url in property_urls:
            if "new-real-estate-project-apartments" in property_url:
                continue

            links_set.add(property_url["href"])

        print("Total links scraped: ", len(links_set))

        self.property_urls.update(links_set)

    def property_urls_to_txt(self):
        with open("urls.txt", "w") as file:
            for property_url in self.property_urls:
                file.write(property_url + "\n")

    def to_csv_file(self, json_content, csv_file):
        """
        Stores the data structure into a CSV file with the specified name.
        """
        print("\nSaving to csv file...")

        parsed_json = json_content

        set_of_field_names = set()
        for dictionary in parsed_json:
            set_of_field_names.update(dictionary.keys())

        field_names = list(set_of_field_names)

        writer = DictWriter(csv_file, fieldnames=field_names)

        writer.writeheader()

        # for country, leaders in self.leaders_data.items():
        #     for leader in leaders:
        #         writer.writerow({"Country": country, **leader})

        print("Done saving CSV file.\n")
