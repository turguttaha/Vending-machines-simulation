import json
import openai
from functions import sales_operations
from functions import vending_machines_operations
from functions import financial_operations
from datetime import datetime


def run_conversation(message):
    # Step 1: send the conversation and available functions to GPT
    messages = [
        {"role": "system", "content":
            """You are analyzer for vending machine database. Your name is analyzer.
            Currency is euro €.
            Our company operations has started on 2020/01/01.
            You will use predefined function to analyze them and answer to user. 
            Don't make assumptions about what values to plug into functions. 
            Ask for clarification if a user request is ambiguous.
            Today is""" + str(datetime.now().date())},
        {"role": "user", "content": message}]
    # Predefined functions
    functions = [
        # introduction of functions to AI
        {
            "name": "get_profit_certain_period",
            "description": "Get profit at the given date intervals.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date. Format: yyyy/MM/dd",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date Format: yyyy/MM/dd"
                    },
                },
                "required": ["start_date", "end_date"],
            },
        },  # 2. add a new functions
        {
            "name": "analyze_payment_method_in_period",
            "description": """Retrieve different types of payment methods and their respective count in a given date
                           range.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date. Format: yyyy/MM/dd",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date Format: yyyy/MM/dd",
                    },
                },
                "required": ["start_date", "end_date"],
            },
        },
        {
            "name": "create_excel_in_certain_period",
            "description": "Create an excel sheet for sales data within a given date interval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Start date. Format: yyyy/MM/dd",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date Format: yyyy/MM/dd"
                    },
                },
                "required": ["start_date", "end_date"],
            },
        },







    ]

    # Request to the gpt-3.5
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
            "analyze_payment_method_in_period": vending_machines_operations.analyze_payment_method_in_period,
            "create_excel_in_certain_period": financial_operations.create_excel_in_certain_period,
        }

        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])

        # execute function
        function_response = function_to_call(
            **function_args
        )

        if function_response is None:
            formatted_function_name = function_name.replace('_', ' ')
            return f"Loading function '{formatted_function_name}'..."
        else:
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
            second_response_message = second_response["choices"][0]["message"]
            return second_response_message.content

    else:
        return response_message.content
