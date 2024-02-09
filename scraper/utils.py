

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


def get_immo_dictionary(response) -> dict:
    split_url = response.url[37:].split("/")
    
    price = response.css("p.classified__price span.sr-only::text").get()
    price = price.replace("€", "")
    
    property_type = "house" if split_url[0] in house_subtypes else "appartment"
    
    property_dictionary = {
        "url": response.url,
        "Property ID": int(split_url[4]),
        "Locality name": split_url[2],
        "Postal code": int(split_url[3]),
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
        "Garden surface": None,  # sometimes in description only
        "Surface of the plot": None,
        "Number of facades": None,  # from description
        "Swimming pool": 0,
        "Building condition": None,
    }
    
    return property_dictionary