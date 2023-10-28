import json
import openai

with open('../config/config.json', 'r') as file:
    config = json.load(file)
    openai.api_key = config["OPENAI_API_KEY"]
