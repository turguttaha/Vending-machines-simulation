import json
from datetime import datetime

import openai

from services import financial_operations
from services import sales_operations
from services import vending_machines_operations


def run_conversation(message):
    # Step 1: send the conversation and available functions to GPT
    messages = [
        {
            "role": "system",
            "content":
                f"""
                    Your name is analyzer.
                    You are a friendly analyzer for the vending machine database.
                    Always respond to the user with an appropriate emoticon that reflects the sentiment of their message.
                    Your response format should be an emoticon followed by a colon and space, then your reply in this manner "(😊): Your reply".
                    The currency is in euros €.
                    Our company operations started on 2020/01/01.
                    Do not make assumptions about what values to plug into functions.
                    Ask for clarification if a user's request is ambiguous.
                    Today is {str(datetime.now().date())}
                """
        },
        {"role": "user", "content": "(😊): " + message}]
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

        {
            "name": "get_most_sold_items",
            "description": "Get the most sold items with amount in the given date interval.",
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

        {
            "name": "get_most_profitable_product",
            "description": "Get the most profitable item in the given date interval.",
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
        {
            "name": "calculate_most_profitable_machine",
            "description": "Calculate the most profitable vending machine within a specified date range.",
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
            "name": "quantity_low_message",
            "description": """ Check the database for vending machines with products quantities <= 5
                              """,
            "parameters": {
                "type": "object",
                "properties": {

                },

            },
        },
        {
            "name": "change_status_vm_to_out_of_order",
            "description": "It changes status of the vending machine as out of order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "vendingMachineID": {
                        "type": "string",
                        "description": "Vending machine id which is provided by user!",
                    },
                },
                "required": ["vendingMachineID"],
            },
        },
        {
            "name": "change_status_vm_to_working",
            "description": "It changes status of the vending machine as working.",
            "parameters": {
                "type": "object",
                "properties": {
                    "vendingMachineID": {
                        "type": "string",
                        "description": "Vending machine id which is provided by user!",
                    },
                },
                "required": ["vendingMachineID"],
            },
        },

        {
            "name": "get_vending_machine_info",
            "description": "Get the temperature, humidiy and state of a vending machine using it's unique ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "machine_id": {
                        "type": "string",
                        "description": "Unique ID of a vending machine",
                    },
                },
                "required": ["machine_id"],
            },
        },
    ]

    # Request to the gpt-3.5
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
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
            "analyze_payment_method_in_period": sales_operations.analyze_payment_method_in_period,
            "create_excel_in_certain_period": financial_operations.create_excel_in_certain_period,
            "get_vending_machine_info": vending_machines_operations.get_vending_machine_info,
            "change_status_vm_to_out_of_order": vending_machines_operations.change_status_vm_to_out_of_order,
            "change_status_vm_to_working": vending_machines_operations.change_status_vm_to_working,
            "get_most_sold_items": sales_operations.get_most_sold_items,
            "get_most_profitable_product": sales_operations.get_most_profitable_product,
            "calculate_most_profitable_machine": sales_operations.calculate_most_profitable_machine,
            "quantity_low_message": vending_machines_operations.quantity_low_message,
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
                model="gpt-4-1106-preview",
                messages=messages,
            )  # get a new response from GPT where it can see the function response
            second_response_message = second_response["choices"][0]["message"]
            return second_response_message.content

    else:
        return response_message.content
