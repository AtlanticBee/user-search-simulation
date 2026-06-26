# Given a CSV file path, number of columns and their data types, returns a dictionary with structure myData={header1:[col1],header2:[col2]...}

import random

def load_csv(file_path, data_types):
   with open(file_path, mode='r', encoding='utf-8') as file:

      # Split file into headers and remainder
      headers = [x.strip() for x in file.readline().split(',')]
      lines = list(file)
      if not headers or not lines:
         raise Exception(f'CSV {file_path} has no data. Aborting.')

      # Create dictionary (assumes headers are unique)
      data = {i:[] for i in headers}
      
      # Parse lines
      for line in lines:
         line_data = [col.strip() for col in line.split(',')]
         for i in range(len(headers)):
            data[headers[i]].append(data_types[i](line_data[i]))

      return data

# Given a textfile containing a list of values one per line, return the list.

def load_list(file_path, data_type):
   with open(file_path, mode='r', encoding='utf-8') as file:
      lines = [data_type(x.strip()) for x in file.readlines()]
      return lines

# Return contents of textfile

def load_text(file_path):
   with open(file_path,mode='r',encoding='utf-8') as file:
      return file.read()

# Pick random value(s) from list knowing the weights (cumulative probability) of each index
# If no weighting is given, all values are given equal weights
# If no values are given, the random number is returned instead
# To restrict the dataset, you can give it lower and upper bounds.
# Apparently this could be done more efficiently with a binary tree FYI
# Returns list.

def pick_random_values(values=[], cumulative_probabilities=[], quantity=1, lower_lim=0, upper_lim=1):
   result = []

   if not quantity or quantity < 0:
      return result

   if not values:
      while len(result) < quantity:
         result.append(random.random())
      return result

   if not cumulative_probabilities:
      while len(result) < quantity:
         result.append(random.choice(values))
      return result
   
   while len(result) < quantity:
      num = random.uniform(lower_lim, upper_lim)
      for idx,val in enumerate(cumulative_probabilities):
         if num < val:
            result.append(values[idx])

   return result
