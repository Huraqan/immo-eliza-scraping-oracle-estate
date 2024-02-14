import re

house_subtypes = [
    "bungalow",
    "chalet",
    "castle",
    "farmhouse",
    "country-house",
    "exceptional-property",
    "apartment-block",
    "mixed-use-building",
    "town-house",
    "mansion",
    "villa",
    "other-properties",
    "manor-house",
    "pavilion",
    "house",
]

compiled_price_pattern = re.compile("[0-9]+")

def get_immo_dictionary(response) -> dict:
    split_url = response.url[37:].split("/")
    
    price = response.css("p.classified__price span.sr-only::text").get()
    # price = price.replace("€", "")
    price = int(compiled_price_pattern.findall(price)[0])
    
    property_type = "house" if split_url[0] in house_subtypes else "appartment"
    
    property_dictionary = {
        "Url": response.url,
        "Property ID": split_url[4],
        "Locality name": split_url[2],
        "Postal code": split_url[3],
        "Price": price,
        "Type of property": property_type,
        "Subtype of property": split_url[0],
        "Type of sale": split_url[1],
        "Bedrooms": None,
        "Living area": None,
        "Kitchen type": 1,
        "Furnished": 0,
        "How many fireplaces?": 0,
        "Terrace surface": None,
        "Garden surface": None,
        "Surface of the plot": None,
        "Number of frontages": None,
        "Swimming pool": 0,
        "Building condition": None,
    }
    
    return property_dictionary