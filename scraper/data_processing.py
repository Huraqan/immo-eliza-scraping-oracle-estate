# import pandas as pd
import json


# to rename columns if needed

    # df = pd.read_csv('output.csv')
    # df2 = df.rename(columns = {'id':"Property ID"}, inplace = False)
    # df2.to_csv("output.csv")


allowed_field_names = [
    "AAddress 1",
    "AAddress 2",
    "AAddress 3",
    "Address",
    "Age of annuitant",
    "Age of annuitants",
    "Agent's name",
    "Armored door",
    "As built plan",
    "Attic",
    "Attic surface",
    "Available as of",#### Possibly the same?
    "Available date",########################
    "Bare ownership sale",
    "Basement",
    "Basement surface",
    "Bathrooms",
    "Bedroom 1 surface",
    "Bedroom 2 surface",
    "Bedroom 3 surface",
    "Bedroom 4 surface",
    "Bedroom 5 surface",
    "Bedrooms",
    "Building VAT",
    "Building condition",
    "Building price excluding VAT",
    "CO₂ emission",
    "Common water heater",
    "Conformity certification for fuel tanks",
    "Connection to sewer network",
    "Construction year",
    "Covered parking spaces",
    "Current monthly revenue",
    "Dining room",
    "Double glazing",
    "Dressing room",
    "E-level (overall energy performance)",
    "EPC description",
    "Energy class",
    "External reference",
    "Extra information",
    "Flat land",
    "Flood zone type",
    "Floor",
    "Furnished",
    "Garden",
    "Garden orientation",
    "Garden surface",
    "Gas, water & electricity",
    "Heat pump",
    "Heating type",
    "How many fireplaces?",
    "Indexed annuity",
    "Isolated",
    "Kitchen surface",
    "Kitchen type",
    "Land is facing street",
    "Land price excluding taxes",
    "Latest land use designation",
    "Laundry room",
    "Living area",
    "Living room",
    "Living room surface",
    "Maximum duration of annuity",
    "Neighbourhood or locality",
    "Number of annexes",
    "Number of annuitants",
    "Number of floors",
    "Number of frontages",
    "Obligation to build",
    "Office,Office surface",
    "Outdoor parking spaces",
    "Percentage rented",
    "Phone number",
    "Photovoltaic solar panels",
    "Planning permission obtained",
    "Plot at rear",
    "Possible priority purchase right",
    "Primary energy consumption",
    "Proceedings for breach of planning regulations",
    "Professional space",
    "Professional space surface",
    "Property name",
    "Reference number of the EPC report",
    "Reversionary annuity",
    "Sea view",
    "Shower rooms",
    "Single session",
    "Street frontage width",
    "Subdivision permit",
    "Surface of the plot",
    "Surroundings type",
    "Taxes related to land",
    "Tenement building",
    "Terms of visit",
    "Terrace",
    "Terrace orientation",
    "Terrace surface",
    "Thermic solar panels",
    "Toilets",
    "Total ground floor buildable",
    "Total price including taxes*",
    "Type of building",
    "Wooded land",
    "Yearly theoretical total energy consumption",
    "Id",
    "Locality name",
    "Postal code",
    "Price",
    "Property subtype",
    "Property type",
    "Type of sale",
    "Url",
]


value_mapping = {
    "Yes": 1,
    "No": 0,
    "Not specified": None
}

# classified__information--address-row ???? dynamically loaded

def fill_attributes(response, property_dictionary):
    address_index = 1
    print("searching for span")
    for span in response.css("span.classified__information--address-row"):
        print("span found")
        span_text = span.css("::text").get()
        print(type(span_text), span_text)
        property_dictionary["AAddress " + str(address_index)] = span_text.replace("\n", "").strip()
        address_index +=1
    
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
        except ValueError:
            value = value_mapping.get(value, value)
        
        if key == "Kitchen type":
            value = 0 if value == "Not installed" else 1
        
        if key == "How many fireplaces?":
            # key = "Fireplaces"
            value = 0 if value == 0 else 1

        # if key in property_dictionary.keys():
        if key in allowed_field_names:
            property_dictionary[key] = value


def restructure_data():
    print("\nRestructuring data...")
    with open("data/raw/output.json", "r") as file:
        list_of_dictionaries = json.load(file)
        list_of_dictionaries = filter_duplicates(list_of_dictionaries)
        extract_field_names(list_of_dictionaries)
        structure_dictionaries(list_of_dictionaries)
    print("\nDONE.")

def filter_duplicates(data: list) -> list:
    print("\nFiltering duplicates... ")
    new_data = []
    list_of_adresses = list()
    list_of_tuples = list()
    
    for dictionary in data:
        address = dictionary.get("Address")
        reference = dictionary.get("External reference")
        
        if not address:
            print("No adress:", dictionary["url"])
            if not reference:
                print("Also no reference... skipping this one.")
                continue
        
        # if address not in list_of_adresses:
        #     list_of_adresses.append(address)
        #     new_data.append(dictionary)
        if (address, reference) not in list_of_tuples:
            list_of_tuples.append((address, reference))
            new_data.append(dictionary)
        else:
            print("Duplicate found! Ext ref:", dictionary.get("External reference"), "address:", address, dictionary["url"])
    
    return new_data
        

def extract_field_names(data: list):# -> list:
    print("\nExtracting field names... ")
    set_of_field_names = set()

    for dictionary in data:
        set_of_field_names.update(dictionary.keys())

    # Sort fields (optional)
    sorted_field_names = sorted(list(set_of_field_names))
    
    with open("data/field_names.json", "w") as file:
        json.dump(sorted_field_names, file)
    
    # return sorted_field_names

def structure_dictionaries(data: list):# -> list:
    print("\nStructuring dictionaries... ")

    final_dictionaries = []
    field_name_occurences = {field_name: 0 for field_name in allowed_field_names}

    for dictionary in data:
        new_dictionary = dict()
        for field_name in allowed_field_names:
            if field_name in dictionary.keys():
                field_name_occurences[field_name] += 1
            
            new_dictionary[field_name] = dictionary.get(field_name, None)

        final_dictionaries.append(new_dictionary)

    # This commented code could be faster but hey... Sometimes you just gotta chill
    #
    # keys = list(dict.keys())
    # values = list(dict.values())
    # sorted_value_index = field_name_occurences.argsort(values)
    # field_name_occurences = {keys[i]: values[i] for i in sorted_value_index}
    
    field_name_occurences = dict(
        sorted(field_name_occurences.items(), key=lambda item: item[1])
        # Item is a tuple (key, value)
    )

    with open("data/field_name_occurences.json", "w") as file:
        json.dump(field_name_occurences, file)

    with open("data/cleaned/output.json", "w") as file:
        json.dump(final_dictionaries, file)

    # return final_dictionaries
