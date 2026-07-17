system_prompt = """
    You are a working as a simulation assistant. The user is going to submit some personal details about themselves, their mood, their location and other factors. You must imagine that the user is currently browsing a sports website that sells the following items: exercise equipment, protein supplements and other nutritional items for sports, and sports clothing. Knowing these basic details about the user, and the website they are browsing, what do you think they would type into the search bar at the top of the page?

    Key Rules: Do not use any thinking tags, do not output internal reasoning, do not write or invent subsequent instructions. Respond only with the immediate answer of what the user would enter into the search bar. Remember, users do not typically enter complete phrases into a search bar, but rather a combination of keywords and descriptions. For now, assume their basic spelling and syntax is always correct.
"""

user_prompt_template = """
    Imagine I was browsing a sports E-commerce website. I'm called **name**, I'm **age** years old and I live **location**. Today, I'm feeling **mood**. I move my fingers to the keyboard and begin to type. What do I type in the search bar?
"""

def generate_prompts(user_data, count):
    prompts = []
    for i in range(count):
        new_prompt = (user_prompt_template
                        .replace("**name**",user_data["names"][i])
                        .replace("**age**",str(user_data["ages"][i]))
                        .replace("**location**",user_data["locations"][i])
                        .replace("**mood**",user_data["moods"][i])
        )
        prompts.append(new_prompt)
    return prompts