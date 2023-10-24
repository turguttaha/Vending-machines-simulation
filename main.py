# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#libraries of the python
import random
import time
# another class to connect db and add, get, update, delete some objects
import connection_mongoDB
import os
import openai
import json


#lists which are using during foreach loop
locations = ["UCLL Hertogstraat","UCLL Proximus","ING","Leuven Public Library","KU Leuven Library","KBC"]
payment_methodes = ["cash","creditcard","bankcontact"]
product_list = [
                {
                    "productID": "P001",
                    "name": "Soda",
                    "price": 1.5,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "without aroma"
                },
                {
                    "productID": "P002",
                    "name": "Cola",
                    "price": 2.1,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "zero"
                },
                {
                    "productID": "P003",
                    "name": "Twix",
                    "price": 1.3,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "120 gr"
                },
                {
                    "productID": "P004",
                    "name": "Nutella B-ready",
                    "price": 1.7,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "white chocolate"
                },
                {
                    "productID": "P005",
                    "name": "Lays",
                    "price": 2.6,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "spicy"
                },
                {
                    "productID": "P006",
                    "name": "Water",
                    "price": 0.9,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "without sparkling"
                }
            ]
vendingMachineIDs = ["VM001","VM002","VM003","VM004","VM005","VM006"]

#Functions that add the first sample objects to the database
def vending_machines_init():
    counter =1
    #foreach loop
    for l in locations:
        #sample vendingmachine data to update its properties in each cycle and save it in the database
        vending_machines_data = {
            "vendingMachineID": "VM001",
            "location": "KBC",  # UCLL hertogstraat, UCLL proximus,ING, Leuven public library, KU Leuven library
            "status": "working",  # other options under maintenance, out of order
            "alert": "none",  # other options low inventory, maintenance required
            "temp": 12.5,
            "humidity": 70,
            "products": [
                {
                    "productID": "P001",
                    "name": "Soda",
                    "price": 1.5,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "without aroma"
                },
                {
                    "productID": "P002",
                    "name": "Cola",
                    "price": 2.1,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "zero"
                },
                {
                    "productID": "P003",
                    "name": "Twix",
                    "price": 1.3,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "120 gr"
                },
                {
                    "productID": "P004",
                    "name": "Nutella B-ready",
                    "price": 1.7,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "white chocolate"
                },
                {
                    "productID": "P005",
                    "name": "Lays",
                    "price": 2.6,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "spicy"
                },
                {
                    "productID": "P006",
                    "name": "Water",
                    "price": 0.9,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "without sparkling"
                }
            ]
        }

        #set new properties
        vending_machines_data['vendingMachineID'] = f"VM00{counter}"
        vending_machines_data['location'] = l
        #print(vending_machines_data)

        #adding object to db using connection_mongoDB.py(parameters collection name , newData to add)
        connection_mongoDB.add_data("ChatBotDB-Release-0.1",vending_machines_data)

        counter +=1
def example_sales_init():
    for i in range(1000):
        sales_Data = {
            "timestamp": "1697358096",  # e datetime in UNIX epoch time.
            "product": {
                "productID": "P001",
                "name": "Soda",
                "price": 1.5,
                "profit percentage": 30,
                "quantity": 10,
                "description": "without aroma"
            },
            "paymentMethod": "cash",  # other option creditcard / bankcontact
            "vendingMachineID": "VM001"
        }
        sales_Data['vendingMachineID'] = random.choice(vendingMachineIDs)

        # Define a range for the random timestamp (e.g., from January 1, 2022, to December 31, 2022)
        start_time = time.mktime(time.strptime("2020-01-01", "%Y-%m-%d"))
        end_time = time.mktime(time.strptime("2023-10-19", "%Y-%m-%d"))
        # Generate a random timestamp within the specified range
        random_timestamp = random.randint(start_time, end_time)

        sales_Data['timestamp'] = random_timestamp

        #rondom.choice(list) --> it select rondom item from list
        sales_Data['paymentMethod'] = random.choice(payment_methodes)
        sales_Data['product'] = random.choice(product_list)


        connection_mongoDB.add_data("sales-0.1", sales_Data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #vending_machines_init()
    #example_sales_init()
    # example of the update database using update_data funtion from connection_mongoDB class
    # we will use it to update vendingmachines data per 15 min(it can be shorter or longer period)
    # connection_mongoDB.update_data("ChatBotDB-Release-0.1",
    #                                "vendingMachineID",
    #                                "VM001",
    #                                "temp",
    #                                15)



    # Example dummy function hard coded to return the same weather
    # In production, this could be your backend API or an external API
    openai.api_key = "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"


    # Example dummy function hard coded to return the same weather
    # In production, this could be your backend API or an external API
    def get_current_weather(location, unit="fahrenheit"):
        """Get the current weather in a given location"""
        weather_info = {
            "location": location,
            "temperature": "60",
            "unit": unit,
            "forecast": ["Cloudy", "windy"],
        }
        return json.dumps(weather_info)


    def run_conversation():
        # Step 1: send the conversation and available functions to GPT
        messages = [{"role": "user", "content": "Hoe is het weer in Leuven?"}]
        functions = [
            {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
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
                "get_current_weather": get_current_weather,
            }  # only one function in this example, but you can have multiple
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
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


    print(run_conversation())
