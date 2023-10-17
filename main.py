# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
import pymongo
from pymongo import MongoClient
import connection_mongoDB

# client = MongoClient("mongodb://localhost:27017")
# db = client["your_database_name"]
# collection = db["vendingMachines"]

client = MongoClient("mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/ChatBotDB")
db = client.get_database()

locations = ["UCLL Hertogstraat","UCLL Proximus","ING","Leuven Public Library","KU Leuven Library","KBC"]


def vending_machines_init():
    counter =1
    for l in locations:
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
        vending_machines_data['vendingMachineID'] = f"VM00{counter}"
        vending_machines_data['location'] = l
        print(vending_machines_data)
        connection_mongoDB.add_data("ChatBotDB-Release-0.1",vending_machines_data)
        #inserted_vending_machine = collection.insert_one(vending_machines_data)
        #print("toegevoegde product id :", inserted_vending_machine.inserted_id)
        counter +=1


#def sales_simulation():

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #connection_mongoDB.add_data("ChatBotDB-Release-0.1", vending_machines_data)

    #vending_machines_init()
    #
    # connection_mongoDB.update_data("ChatBotDB-Release-0.1",
    #                                "vendingMachineID",
    #                                "VM001",
    #                                "temp",
    #                                15)


    ##update products attributes

    db["ChatBotDB-Release-0.1"].update_one({"vendingMachineID":"VM001" },{"$set": {"products.$[elem].quantity": 9}},array_filters=[{"elem.productID":"P001"}])








