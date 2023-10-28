import os

if __name__ == "__main__":
    # check that OPENAI_API_KEY exists in environ
    if 'OPENAI_API_KEY' in os.environ:
        api_key = os.environ['OPENAI_API_KEY']
        print(f"OpenAI API Key exists already: {api_key}")
    else:
        print("OpenAI API Key is None")