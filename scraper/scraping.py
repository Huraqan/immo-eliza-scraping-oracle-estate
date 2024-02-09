import scrapy
from scraper.utils import get_dictionary, fill_attributes


pages = 2


class ImmoSpider(scrapy.Spider):
    name = "immoweb"
    allowed_domains = ["immoweb.be"]
    start_urls = []
    for i in range(1, pages):
        start_urls.append(
            f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={i}&orderBy=relevance"
        )

    async def parse(self, response):
        for obj in response.css("a.card__title-link"):
            url = response.urljoin(
                obj.attrib["href"]
            )
             # normalize and convert probable relative urls to absolute
            if (
                "new-real-estate-project-apartments" in url
                or "new-real-estate-project-houses" in url
            ):
                continue
            # follow: automatically find urls(extracting hrefs) then sends a request to that URL and then calls the parse_property_page
            yield response.follow(
                url, self.parse_property_page
            ) 

    def parse_property_page(self, response):
        property_dictionary = get_dictionary(response)

        fill_attributes(response, property_dictionary)

        yield property_dictionary
