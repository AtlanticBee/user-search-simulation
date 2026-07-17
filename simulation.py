import random

def age_filter(x):
    if (x < 16) or (x > 95):
        return False
    else:
        return True

def pick_weighted_value(values, qprobs, quantity, filter_func=None):
    result = []
    while len(result) < quantity:
        num = random.random()
        for idx,val in enumerate(qprobs):
            if num < val:
                selection = values[idx]
                if filter_func == None or filter_func(selection):
                    result.append(values[idx])
                break

    return result

def generate_users(dataset, count):

    ages = pick_weighted_value(dataset["ages"]["values"], dataset["ages"]["qprobs"], count, age_filter)
    sexes = []
    while len(sexes) < count:
        sexes.append(random.choice(['male','female']))
    # Name depends on age and sex - extract the decade they were born in and get random name from list.
    # Assumes it's 2026
    birth_decades = [str(((2026 - x) // 10) * 10) + "s" for x in ages]
    names = []
    for idx,decade in enumerate(birth_decades):
        names.append(pick_weighted_value(dataset["names"][decade][sexes[idx]], dataset["names"]["qprobs"], 1)[0])

    # Location (going to skip settlement for now)
    locations = pick_weighted_value(dataset["locations"]["conversational_names"], dataset["locations"]["qprobs"], count)

    # Mood
    mood_types = pick_weighted_value(dataset["mood_types"]["values"], dataset["mood_types"]["qprobs"], count)
    moods = []
    for i in mood_types:
        moods.append(random.choice(dataset["moods"][i]))

    user_data = {
        "ages":ages,
        "birth_decades":birth_decades,
        "sexes":sexes,
        "names":names,
        "locations":locations,
        "mood_types":mood_types,
        "moods":moods
    }

    return user_data