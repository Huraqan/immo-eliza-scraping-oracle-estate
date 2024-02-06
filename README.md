# ORACLE ● ESTATE

## Description

This is a regular paragraph.

This is another regular paragraph.

## Installation


## Usage


## Sources

### Learning resources
- https://gist.github.com/Alinaprotsyuk/3d58f8cd52eb03a11283d64beb0e083e
- https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial

### Markdown goodies
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
<div style="display: flex;">
    <div style="
        width: 200px;
        height: 200px;
        background-image: url('duplicates.png');
        background-size: cover;
        border-radius: 10px;
        box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.5);"
    ></div>
    <div style="flex: 1; padding-left: 10px;">
        <p>The presence of duplicates may be attributed to the occurrence of identical listings across different pages of search results, often marked as "new" (as illustrated in the image on the left). To resolve this issue, we can simply add URLs to a set, ensuring the elimination of duplicates.</p>
        <code style="display: block;">links_set.add([property_url["href"] for property_url in property_urls])</code>
        <br><code style="display: block;">self.property_urls_set.update(links_set)</code></br>
    </div>
</div>

## Unveiling the Matrix



## What's next?


