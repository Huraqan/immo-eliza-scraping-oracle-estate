import json


allowed_field_names = [
    "Address",
    "Age of annuitant",
    "Age of annuitants",
    "Agent's name",
    "Armored door",
    "As built plan",
    "Attic",
    "Attic surface",
    "Available as of",  # Possibly the same?
    "Available date",  #
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
    "Fireplace",
    "Indexed annuity",
    "Isolated",
    "Kitchen surface",
    "Kitchen type",
    "Land is facing street",
    "Land price excluding taxes",
    # "Latest land use designation",
    # "Laundry room",
    # "Living area",
    # "Living room",
    # "Living room surface",
    "Maximum duration of annuity",
    "Neighbourhood or locality",
    # "Number of annexes",
    # "Number of annuitants",
    # "Number of floors",
    "Number of frontages",
    # "Obligation to build",
    # "Office,Office surface",
    # "Outdoor parking spaces",
    # "Percentage rented",
    # "Phone number",
    # "Photovoltaic solar panels",
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

def extract_field_names(data: list) -> list:
    set_of_field_names = set()

    for dictionary in data:
        set_of_field_names.update(dictionary.keys())

    # Sort fields (optional)
    sorted_field_names = sorted(list(set_of_field_names))
    
    with open("data/raw/field_names.json", "w") as file:
        json.dump(sorted_field_names, file)
    
    return sorted_field_names

def structure_data():
    with open("data/raw/output.json", "r") as file:
        json_content = json.load(file)
        extract_field_names(json_content)
        structure_dictionaries(json_content)

def structure_dictionaries(data: list) -> list:
    print("\nStructuring data...")

    final_dictionaries = []
    field_name_occurences = {field_name: 0 for field_name in allowed_field_names}

    for dictionary in data:
        new_dictionary = dict()
        for field_name in allowed_field_names:
            if field_name in dictionary.keys():
                field_name_occurences[field_name] += 1
            
            new_dictionary[field_name] = dictionary.get(field_name, None)

        final_dictionaries.append(new_dictionary)

    print("Done structuring data.\n")

    print("\nField occurences:")
    # keys = list(dict.keys())
    # values = list(dict.values())
    # sorted_value_index = field_name_occurences.argsort(values)
    # field_name_occurences = {keys[i]: values[i] for i in sorted_value_index}
    
    field_name_occurences = dict(
        sorted(field_name_occurences.items(), key=lambda item: item[1])
        # Item is a tuple (key, value)
    )

    with open("field_name_occurences.json", "w") as file:
        json.dump(field_name_occurences, file)

    print(field_name_occurences)

    return final_dictionaries
