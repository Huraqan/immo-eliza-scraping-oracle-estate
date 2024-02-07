# # import csv
# import re

# import selenium
# from bs4 import BeautifulSoup
# from pandas import DataFrame
# from requests import Session
# from time import sleep
# from random import uniform


# class ImmoWebScraper:
#     """
#     ImmoWebScraper class for scraping data from the real-estate website www.immoweb.be.
#     """

#     def __init__(self, session: Session):
#         self.base_url: str = "https://www.immoweb.be/en/search/"
#         self.houses_url: str = "house/"
#         self.appartement_url: str = "apartment/"
#         self.session: Session = session
#         self.property_links = []
#         self.property_data = {}
        
    


    
#     def get_links(self, url: str):
#         prop = self.session.get(url)    

#         if prop.status_code != 200:
#             print("\nPAGE NOT FOUND!!!\n")

#         soup = BeautifulSoup(prop.text, "html.parser")
#         for tag in soup.find_all(name = "a", attrs = {"class": "card__title-link"}, href = True):
#             self.property_links.append(tag.get('href')) 
 

#     def get_property_info(self, link):
#         page_of_property = self.session.get(link)

#         soup = BeautifulSoup(page_of_property.text, "html.parser")
#         # for tag in soup.find("div", class_ = "classified__header--immoweb-code"):
#         #     print(tag.text.split(":")[1].strip())

#         price_row = soup.find('p', class_="classified__price")
#         price_splitted = price_row.text.split()
#         price_parts = [price for price in price_splitted if price[0] == '€'  or '-' in price]
#         price_range = ' '.join(price_parts)
#         print("Price:", price_range)

#         # Extract the city name (Deinze)
#         # city_name = address_row.contents[-1].strip()
#         # print("City Name:", city_name)
#         #         # tags.append(tag)
#         #         # tag = tags[1]
         
#         #         # amenities_data["Locality:"] = tag.text.strip()
#         #         # print(amenities_data)
#                 #     for tag in soup.find("div", class_ = "classified__header--immoweb-code"):
#                 # self.property_data[tag.text.split(":")[1].strip()] = amenities_data




#     def get_data(self, url: str) -> None:
#         pass

#     def to_csv_file(self, filename: str):
#         """
#         Stores the data structure into a CSV file with the specified name.
#         """
#         leaders_summary: list = []

#         df = DataFrame.from_dict(leaders_summary)
#         df.to_csv(filename, index=False, header=True)




from re import compile

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
        self.property_urls: set = set()
        self.session: Session = session
        # self.cookie: object = self.request_cookie()
    
    def make_simple_request(self, url: str):
        print("url:", url)
        return self.session.get(url)

    def get_links(self, url: str) -> None:
        req = self.make_simple_request(url)
        
        if req.status_code != 200:
            print("\nPAGE NOT FOUND!!!\n")
        
        soup = BeautifulSoup(req.content, "html.parser")
        
        property_urls = soup.find_all(
            name = "a",
            attrs = {"class": "card__title-link"},
            href = True
        )
        
        links_set = set()

        for property_url in property_urls:

            links_set.add(property_url['href'])
        for tag in soup.find_all(
            name = "a",
            attrs = {"class": "card__title-link"},
            href = True
        ):
            property_urls = tag["href"]
        
        print("Total links scraped: ", len(links_set))
            
        self.property_urls.update(links_set)
            
    def property_urls_to_txt(self):
        with open("urls.txt", "w") as file:
            for property_url in self.property_urls:
                file.write(property_url + "\n")

    def to_csv_file(self, filename: str):
        """
        Stores the data structure into a CSV file with the specified name.
        """
        leaders_summary: list = []  

        df = DataFrame.from_dict(leaders_summary)
        df.to_csv(filename, index=False, header=True)

test = ImmoWebScraper(Session())
#make request to houses
for i in range(333):
    print(f"Getting urls on page: {i}")
    test.get_links(f"https://www.immoweb.be/en/search/{test.houses_url}for-sale?countries=BE&page={i}&orderBy=postal_code")
    # sleep(uniform(0.2, 0.9))
#make request to appartements
for i in range(333):
    print(f"Getting urls on page: {i}")
    test.get_links(f"https://www.immoweb.be/en/search/{test.appartement_url}for-sale?countries=BE&page={i}&orderBy=postal_code")
    # sleep(uniform(0.2, 0.9))
print(len(test.property_links))
test.get_links(f"{test.base_url}{test.houses_url}{test.end_url}")
for link in test.property_links:
    test.get_property_info(link)
