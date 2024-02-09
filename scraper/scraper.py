from csv import DictWriter
from bs4 import BeautifulSoup

from requests import Session


class ImmoWebScraper:
    """
    ImmoWebScraper class for scraping data from the real-estate website www.immoweb.be.
    """

    def __init__(self, session: Session):
        self.base_url: str = "www.immoweb.be/"
        self.data_dict: dict = {}
        self.property_urls: set = set()
        self.property_urls_l: list = list()
        self.session: Session = session

    def try_except_decorator(function):
        def decorated(*args, **kwargs):
            while True:
                try:
                    return function(*args, **kwargs)
                except:
                    if input("\nCONNECTION ERROR! Try again? 'n' to quit : ") == "n":
                        exit()

        return decorated

    @try_except_decorator
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
        links_list = list()
        
        for property_url in property_urls:
            if "new-real-estate-project-apartments" in property_url:
                continue
            
            links_list.append(property_url["href"])
            links_set.add(property_url["href"])

        print(f"Total links scraped: set: {len(links_set)}, list: {len(links_list)}")

        self.property_urls.update(links_set)
        self.property_urls_l += links_list
        
        from collections import Counter
        print("\nList duplicates:", [k for k,v in Counter(links_list).items() if v>1])
        # print("list:\n", sorted(links_list))
        # print("set:\n", sorted(links_set))

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

        sorted_field_names = sorted(list(set_of_field_names))

        writer = DictWriter(csv_file, fieldnames=sorted_field_names)

        writer.writeheader()
        
        # write rows
        for dictionary in parsed_json:
            row = {}
            for field_name in sorted_field_names:
                row[field_name] = dictionary.get(field_name, None)
            writer.writerow(row)

        print("Done saving CSV file.\n")