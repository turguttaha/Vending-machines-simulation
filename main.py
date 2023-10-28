# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#libraries of the python
import random
import time
# another class to connect db and add, get, update, delete some objects
from db_connections import mongodb_connection
from funcions.openai_operations import run_conversation


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

        #adding object to db using mongodb_connection.py(parameters collection name , newData to add)
        mongodb_connection.add_data("ChatBotDB-Release-0.1", vending_machines_data)

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


        mongodb_connection.add_data("sales-0.1", sales_Data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # vending_machines_init()
    #  example_sales_init()
    while True:
        message = input("Gebruiker:")
        print(run_conversation(message))


