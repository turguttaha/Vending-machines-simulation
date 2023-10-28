import json
import openai
from functions import sales_operations

# API key
openai.api_key = "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"


def run_conversation(message):
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content":message}]
    functions = [
        # introduction of functions to ai
        {
            "name": "get_profit_certain_period",
            "description": "Get profit at the given date intervals. with python codes",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "integer",
                        "description": "Start date Epoch timestamp in seconds",
                    },
                    "end_date": {
                        "type": "integer",
                        "description": "End date Epoch timestamp in seconds"
                    },
                },
                "required": ["start_date", "end_date"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_profit_certain_period": sales_operations.get_profit_certain_period,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            start_date=function_args.get("start_date"),
            end_date=function_args.get("end_date"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response
    else:
        return response_message.content

