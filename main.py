from ollama_api import get_llm_response
from data_loader import load_all_data
from simulation import generate_users
from prompts import generate_prompts, system_prompt

simulation_size = 10

data = load_all_data()
users = generate_users(dataset=data, count=simulation_size)
user_prompts = generate_prompts(users, count=simulation_size)
responses = []
for prompt in user_prompts:
    responses.append(get_llm_response(prompt, system_prompt, description=f"A user with the prompt: {prompt}"))

print(responses)