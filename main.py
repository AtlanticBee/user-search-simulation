import random
import urllib.request
import urllib.error
import json

# Load data

def parse_csv(file_path,column_count,data_types):
   with open(file_path,mode='r',encoding='utf-8') as file:
      headers = [x.strip() for x in file.readline().split(',')]
      lines = list(file)
      if not lines:
         raise Exception(f'CSV {file_path} has no data. Aborting.')
      data = {i:[] for i in headers}
      data['size'] = len(lines)
      for row in lines:
         row_data = [elem.strip() for elem in row.split(',')]
         for i in range(column_count):
            data[headers[i]].append(data_types[i](row_data[i]))
      return data

def parse_txt_list(file_path,data_type):
   with open(file_path,mode='r',encoding='utf-8') as file:
      lines = [data_type(x.strip()) for x in file.readlines()]
      return lines

def get_text_file(file_path):
   with open(file_path,mode='r',encoding='utf-8') as file:
      return file.read()

def get_random_age(data):
   num = random.random()
   for idx,val in enumerate(data['cumulative_probability']):
      if num < val:
         return data['age'][idx]

def get_random_name(names,distribution,age,current_year=2026):
   # Each decade has 99 of the most popular names in order of popularity (descending)
   # We generate a random probability between 0 and 1 and extract the name
   num = random.random()
   decade = (current_year - age // 10) * 10
   if decade < 1930:
      decade = 1930
   if decade > 2020:
      decade = 2020
   for idx,val in enumerate(distribution):
      if num < val:
         return names[decade][idx]

def get_random_location(region_data,settlement_data):
   result = {}
   # Step 1 - pick region of England, gather text form and decide if city or rural
   num1 = random.random()
   for idx,val in enumerate(region_data['probability']):
      if num1 < val:
         result['region'] = region_data['region'][idx]
         result['text-form'] = region_data['text-form'][idx]
         num2 = random.random()
         result['isUrban'] =  num2 < region_data['urbanisation'][idx]
         break

   # If rural (non-city) pick settlement type:
   if result['isUrban']:
      result['settlement'] = 'city'
   else:
      num3 = random.random()
      for idx,val in enumerate(settlement_data['probability']):
         if num3 < val:
            result['settlement'] = settlement_data['location'][idx]
            break

   return result
   

age_distribution = parse_csv(file_path='data/age.csv',column_count=2,data_types=[int,float])
weekdays_list = parse_txt_list('data/weekdays.txt',str)
months_list = parse_txt_list('data/months.txt',str)
name_distribution = parse_txt_list('data/name_probabilities.txt',float)
name_decades = [1930,1940,1950,1960,1970,1980,1990,2000,2010,2020]
female_names = {decade:[] for decade in name_decades}
male_names = {decade:[] for decade in name_decades}
good_moods = parse_txt_list('data/moods_good.txt',str)
bad_moods = parse_txt_list('data/moods_bad.txt',str)
locations = parse_csv(file_path='data/england_regions.csv',column_count=4,data_types=[str,str,float,float])
settlement_types = parse_csv(file_path='data/non_city_settlements.csv',column_count=2,data_types=[str,float])
myprotein_homepage = get_text_file('data/homepage.txt')

for decade in name_decades:
   male_file = "data/male_names_" + str(decade) + ".txt"
   female_file = "data/female_names_" + str(decade) + ".txt"
   male_names[decade] = parse_txt_list(male_file,str)
   female_names[decade] = parse_txt_list(female_file,str)

simulation_size = 20
ages = []
sexes = []
months = []
weekdays = []
names = []
moods = []
home_locations = []

while len(ages) < simulation_size:
   val = get_random_age(age_distribution)
   if val > 15:         # Limiting lower age to 16
      ages.append(val)

while len(sexes) < simulation_size:
   sexes.append(random.choice(['M','F']))
   months.append(random.choice(months_list))
   weekdays.append(random.choice(weekdays_list))
   good_mood = random.choice(good_moods)
   bad_mood = random.choice(bad_moods)
   final_mood = random.choice([good_mood,bad_mood])
   moods.append(final_mood)
   home_locations.append(get_random_location(locations,settlement_types))

for i in range(0,simulation_size):
   if sexes[i] == 'M':
      names.append(get_random_name(male_names,name_distribution,ages[i]))
   else:
      names.append(get_random_name(female_names,name_distribution,ages[i]))

prompts = []

for i in range(simulation_size):
   context = (f"It's a {weekdays[i]} in {months[i]} and"
              f"a {ages[i]}-year-old called {names[i]} is on their phone."
              f" They live in a {home_locations[i]['settlement']} {home_locations[i]['text-form']}."
              f" They are browsing the internet and reach a fitness website that sells a range of protein nutritional products and sports clothing."
              f" They feel {moods[i]}. If you were in their position, what would you enter into the website search bar??"
   )
   prompts.append(context)

url = "http://localhost:11434/api/chat"
responses = []

# Define a strict system directive to control output behavior
system_instruction = (
    "You are an e-commerce user simulation engine. Your task is to output the exact search phrase "
    "a customer would type into a fitness website's search bar based on their demographic and emotional scenario.\n"
    "CRITICAL RULES:\n"
    "1. Output ONLY the raw query keywords.\n"
    "2. Never use conversational filler, pleasantries, introductory text, or explanations.\n"
    "3. Do not enclose the output in quotation marks, brackets, or markdown blocks.\n"
    "4. Prioritize natural, realistic user intent over technical specification codes (avoid prefixes like '100%' or '20g' unless natural)."
)

for idx, prompt in enumerate(prompts):
   
   # Build the structured message history array for the Chat API
   payload_messages = [
      {"role": "system", "content": system_instruction},
      
      # Few-shot Example 1
      {
         "role": "user", 
         "content": "It's a Monday in March and a 22-year-old called Leo is on their phone. They live in a city in London. They are browsing a fitness website that sells protein products and sports clothing. They feel motivated. If you were in their position, what would you enter into the website search bar??"
      },
      {"role": "assistant", "content": "vegan protein powder clearance"},
      
      # Few-shot Example 2
      {
         "role": "user", 
         "content": "It's a Friday in August and a 68-year-old called Margaret is on their tablet. They live in a village in Yorkshire. They are browsing a fitness website that sells protein products and sports clothing. They feel confused. If you were in their position, what would you enter into the website search bar??"
      },
      {"role": "assistant", "content": "comfortable walking shoes for seniors"},
      
      # Few-shot Example 3
      {
         "role": "user", 
         "content": "It's a Wednesday in October and a 34-year-old called Chloe is on their phone. They live in a town in the West Midlands. They are browsing a fitness website that sells protein products and sports clothing. They feel excited. If you were in their position, what would you enter into the website search bar??"
      },
      {"role": "assistant", "content": "gym clothes matching sets"},
      
      # The active execution prompt
      {"role": "user", "content": prompt}
   ]

   payload = {
      "model": "phi4-sim",
      "messages": payload_messages, # Pass the message thread history
      "stream": False,
      "options": {
         "temperature": 0.7,       # Bumping the variance yields realistic query distributions
         "num_predict": 12         # Cutoff limit protects against trailing structural leaks
      }
   }

   json_data = json.dumps(payload).encode('utf-8')

   req = urllib.request.Request(
      url,
      data=json_data,
      headers={"Content-Type": "application/json"},
      method="POST"
   )

   try:
      print(f"Simulating query {idx+1}/{len(prompts)} for {names[idx]}...")
      with urllib.request.urlopen(req, timeout=30) as response:
            raw_body = response.read().decode("utf-8")
            result = json.loads(raw_body)
            
            # The Chat API nests strings under message -> content
            model_message = result.get('message', {})
            clean_query = model_message.get('content', '').strip()
            
            # Sanitization step to clean out rogue punctuation marks or container wrappers
            clean_query = clean_query.split('\n')[0].replace('"', '').replace('[', '').replace(']', '').strip()
            
            responses.append(clean_query)
            print(f"  → Simulated Query: {clean_query}")
            
   except urllib.error.URLError as e:
      print(f"\n[ERROR] Connection failed: {e.reason}")
      break

# Write your updated results back out to the dataset
with open('data/result.csv', mode='w', encoding='utf-8') as file:
   for idx, val in enumerate(responses):
      file.write(f"{prompts[idx]}|{responses[idx]}\n")
print("\nSimulation dataset written successfully to data/result.csv")
