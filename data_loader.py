# The majority of data consists of a list of values and corresponding list of cumulative probabilities (abbreviated to qprobs)

# To start off with we will use: age, name, location, mood + mood_types.

def load_list(file_path, data_type):
   with open(file_path, mode='r', encoding='utf-8') as file:
      lines = [data_type(x.strip()) for x in file.readlines()]
      return lines

def validate_qprobs(values, qprobs, name):
    if not values or not qprobs:
        raise Exception(f'Missing data while validating {name} qprobs.')
    if len(values) != len(qprobs):
        raise Exception(f'List of {name} values is of different length to qprobs.')
    if qprobs[0] == 0:
        raise Exception(f'Qprobs of {name} should not start at zero.')
    if qprobs[-1] != 1:
        raise Exception(f'Qprobs of {name} should end at one.')
    
# Straight forward data sets can use this method. Note default for values is a string.
def load_qprobs(base_path, name, values_type=str):
    values = load_list(base_path + "values.txt", values_type)
    qprobs = load_list(base_path + "qprobs.txt", float)
    validate_qprobs(values, qprobs, name)
    return values, qprobs

# Names are a bit more complex - depend on decade
def load_name_qprobs(base_path):
    decades = ["1930s","1940s","1950s","1960s","1970s","1980s","1990s","2000s","2010s","2020s"]
    name_data = {}
    name_data["qprobs"] = load_list(base_path + "qprobs.txt", float)
    for decade in decades:
        female_names = load_list(base_path + decade + "/female.txt", str)
        male_names = load_list(base_path + decade + "/male.txt", str)
        validate_qprobs(female_names, name_data["qprobs"], f"names of females for {decade}")
        validate_qprobs(male_names, name_data["qprobs"], f"names of males for {decade}")
        name_data[decade] = {
            "female":female_names,
            "male":male_names
        }
    return name_data

def load_location_data(base_path):
    vals, qprobs = load_qprobs(base_path, "locations")
    conv_names = load_list(base_path + "conversational_names.txt", str)
    urbanisation_probs = load_list(base_path + "urbanisation_probs.txt", str)
    validate_qprobs(conv_names, qprobs, "conversational region names")
    validate_qprobs(urbanisation_probs, qprobs, "urbanisation probabilities by region")
    location_data = {}
    location_data["values"] = vals
    location_data["qprobs"] = qprobs
    location_data["urbanisation_probs"] = urbanisation_probs
    location_data["conversational_names"] = conv_names
    return location_data

# Called by main.py
def load_all_data():
    dataset = {}

    # Get ages
    age_values, age_qprobs = load_qprobs("data/age/", "age", values_type=int)
    dataset["ages"] = {
        "values":age_values,
        "qprobs":age_qprobs
    }

    # Get names
    dataset["names"] = load_name_qprobs("data/names/")

    # Get locations
    dataset["locations"] = load_location_data("data/england_region/")

    # Get mood types
    mood_type_vals, mood_type_qprobs = load_qprobs("data/mood_types/", "mood types")
    dataset["mood_types"] = {
        "values":mood_type_vals,
        "qprobs":mood_type_qprobs
    }

    # Get moods (good, bad, neutral)
    dataset["moods"] = {}
    dataset["moods"]["good"] = load_list("data/moods/good.txt", str)
    dataset["moods"]["neutral"] = load_list("data/moods/neutral.txt", str)
    dataset["moods"]["bad"] = load_list("data/moods/bad.txt", str)

    return dataset