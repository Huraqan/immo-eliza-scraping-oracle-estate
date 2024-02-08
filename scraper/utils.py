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

def data_set(response):
    split_url = response.url[37:].split("/")
    price = response.css("p.classified__price span.sr-only::text").get()
    price = price.replace("€", "")
    property_type = "house" if split_url[0] in house_subtypes else "appartment"
    data = {
        # "url": response.url,
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
    return data


def get_attributes(response, data):
    for row in response.css("tr.classified-table__row"):
        key = row.css("th.classified-table__header::text").get()
        value = row.css("td.classified-table__data::text").get()

        if not (key and value):
            continue

        key = key.replace("\n", "").strip()
        value = value.replace("\n", "").strip()

        if not (key and value):
            continue

        try:
            value = int(value)
        except:
            # Define the dictionary mapping
            value_mapping = {"Yes": 1, "No": 0, "Not specified": None}

            # Convert value using the dictionary mapping
            value = value_mapping.get(value, value)

        if key == "Kitchen type":
            value = 0 if value == "Not installed" else 1
        if key == "How many fireplaces?":
            value = 1 if value > 0 else 0

        if key in data.keys():
            data[key] = value
