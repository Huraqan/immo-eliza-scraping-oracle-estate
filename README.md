# ORACLE ● ESTATE

## Description

We're building a web scraper to extract property listings from real estate websites. Initially, we used Requests and BeautifulSoup for prototyping but later switched to Scrapy due to its speed and ease of use. We resolved duplicate link issues with Scrapy's built-in dupefilter. We're still addressing special character encoding issues in the dataset and implementing value mapping for data cleaning.


## Installation


## Usage


## Sources

### Learning resources
- https://gist.github.com/Alinaprotsyuk/3d58f8cd52eb03a11283d64beb0e083e
- https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial

### Markdown goodies
- https://medium.com/swlh/how-to-make-the-perfect-readme-md-on-github-92ed5771c061
- https://www.alt-codes.net/circle-symbols
- https://daringfireball.net/projects/markdown/syntax#html

## Contributors

<div style="display: flex; align-items: center;">
    <a href="https://github.com/Huraqan">
        <img src="https://github.com/Huraqan.png" alt="Sebastiaan Indesteege" style="border-radius: 50%; width: 200px; height: 200px; margin-right: 10px;">
    </a>
    <a href="https://github.com/Lucky-sketch">
        <img src="https://github.com/Lucky-sketch.png" alt="Mark Shevchenko" style="border-radius: 50%; width: 200px; height: 200px; margin-right: 10px;">
    </a>
    <a href="https://github.com/neverforgetthisusername">
        <img src="https://github.com/neverforgetthisusername.png" alt="Cédric" style="border-radius: 50%; width: 200px; height: 200px;">
    </a>
</div>

## Timeline

- thing done
- another thing done
- yet some more
- yetsum morum
- yetsum moprum
- letsem miprum
- lorem iprum
- lorem ipsum
- nailed it

# DEV LOG

## Cracking the code

### Scraping search-result pages for property urls
- Using simple session requests, with small sleep timeout
- Leveraging the power of immoweb's own search query
- Scraping 333 pages with 60 urls each
- BeautifulSoup to extract relevant urls
- Storing urls to `TXT` file

### Scraping property pages for specs
- Custom ImmoSpider class inheriting Spider class from Scrapy module
- Launching Scrapy from within the script
- Storing specs to `JSON` file as a list of dictionaries

## Preparing for unforseen consequences...

### Duplicates

<img src="duplicates.png" align="left" width="200px"/>
<p>
The presence of duplicates may be attributed to the occurrence of identical listings across different pages of search results, often marked as "new" (as illustrated in the image on the left). To resolve this issue, we can simply add URLs to a set, ensuring the elimination of duplicates.
</p>
<br clear="left"/>

```python
    def scrape_property_urls(self, url: str):
        ...

        links_set = set()
        
        for property_url in property_urls:
            ...
            
            links_set.add(property_url["href"])

        self.property_urls.update(links_set)
```

## Unveiling the Matrix

Prepare to journey into the heart of the data as we decode the patterns, uncover hidden insights, and unlock the potential within. Our quest will involve harnessing the power of pandas and numpy, matplotlib or possibly ggplot2 and any other libraries that might be relevant. Get ready to witness the transformation as we reveal the matrix's secrets.


## What's next?

Our trajectory continues with optimization, machine learning exploration, and scalability enhancements. Stay tuned for our next tech leap.
