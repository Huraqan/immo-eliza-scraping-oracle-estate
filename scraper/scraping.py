import scrapy
import scraper.utils



class ImmoSpider(scrapy.Spider):
    pages = 2
    name = "immoweb"
    allowed_domains = ["immoweb.be"]
    start_urls = []
    for i in range(1,pages):
        start_urls.append(f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={i}&orderBy=relevance")
    
    async def parse(self, response):
        for obj in response.css('a.card__title-link'):            
            url = response.urljoin(obj.attrib["href"]) #normalize and convert probable relative urls to absolute
            if "new-real-estate-project-apartments" in url  or "new-real-estate-project-houses" in url: continue
            yield response.follow(url, self.parse_property_page) #follow: automatically find urls(extracting hrefs) then sends a request to that URL and then calls the parse_property_page

    def parse_property_page(self, response):

        data = scraper.utils.data_set(response)

        scraper.utils.get_attributes(response,data)


        yield data
