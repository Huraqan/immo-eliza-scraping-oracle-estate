# import csv
from re import compile

import selenium
from bs4 import BeautifulSoup
from pandas import DataFrame
from requests import Session


class ImmoWebScraper:
    """
    ImmoWebScraper class for scraping data from the real-estate website www.immoweb.be.
    """

    def __init__(self, session: Session):
        self.base_url: str = "www.immoweb.be/"
        self.data_dict: dict = {}
        self.session: Session = session
        # self.cookie: object = self.request_cookie()
    
    def make_simple_request(self, url: str):
        return self.session.get(url)

    def get_data(self, url: str) -> None:
        pass

    def to_csv_file(self, filename: str):
        """
        Stores the data structure into a CSV file with the specified name.
        """
        leaders_summary: list = []

        for country, leaders in self.leaders_data.items():
           for leader in leaders:
                leaders_summary.append({
                        "Country": country,
                        "Leader": f"{leader["first_name"]} {leader["last_name"]}",
                        "First Paragraph": leader["paragraph"],
                    }
                )

        df = DataFrame.from_dict(leaders_summary)
        df.to_csv(filename, index=False, header=True)
