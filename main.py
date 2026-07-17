import sys

from ollama_api import get_llm_response
from data_loader import load_all_data
from simulation import generate_users
from prompts import generate_prompts, system_prompt

# To call the program: python3 main.py
# + simulation_size (optional, any positive integer)
# + temperature (optional, 0 to 1)

script_name = sys.argv[0]
simulation_size = sys.argv[1]
temperature = sys.argv[2]

simulation_size = 10

data = load_all_data()
users = generate_users(dataset=data, count=simulation_size)
user_prompts = generate_prompts(users, count=simulation_size)
responses = []
for prompt in user_prompts:
    responses.append(
        get_llm_response(
            prompt,
            system_prompt,
            temperature,
            description=f"A user with the prompt: {prompt}"
        )
    )

print(responses)