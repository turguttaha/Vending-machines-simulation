import time

from data.openai_key import *

setup_openai_key()

if __name__ == "__main__":
    while True:
        user_message = input("You: ")
        user_message_timestamp = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        print("Bot: ", response["choices"][0]["message"]["content"])
        bot_response_timestamp = time.time()
        response_time = bot_response_timestamp - user_message_timestamp
        print(f"Response time: {response_time} seconds")
