from twilio.rest import Client
import matplotlib.pyplot as plt
import matplotlib
import pymongo

from data import mongodb_data
from datetime import datetime

from data.mongodb_data import get_vending_machine_data

matplotlib.use('TkAgg')

def change_status_vm_to_out_of_order(vendingMachineID):
    check= mongodb_data.update_vm_attribute("vendingMachineID",vendingMachineID,"status","out of order")
    if check.modified_count ==1:
        return f"Vending machine with id {vendingMachineID} is now out of order! "
    else:
        return "No vending machine matching this id number was found"
def change_status_vm_to_working(vendingMachineID):
    check= mongodb_data.update_vm_attribute("vendingMachineID",vendingMachineID,"status","working")
    if check.modified_count ==1:
        return f"Vending machine with id {vendingMachineID} is now working! "
    else:
        return "No vending machine matching this id number was found"


def quantity_low_message():

    collection = mongodb_data.mongodb_instance.db["Vending-Machines-0.1"]

    # Define the aggregation pipeline
    pipeline = [
        {
            "$unwind": "$products"
        },
        {
            "$match": {
                "products.quantity": {"$lte": 5}
            }
        },
        {
            "$project": {
                "vendingMachineID": 1,
                "products.name": 1,
                "products.quantity": 1
            }
        },
        {
            "$group": {
                "_id": "$vendingMachineID",
                "products": {
                    "$push": {
                        "name": "$products.name",
                        "quantity": "$products.quantity"
                    }
                }
            }
        }
    ]

    # Execute the aggregation query
    result = list(collection.aggregate(pipeline))
    account_sid = 'ACb01999e9dfdd51a3f26e1c4076777e7f'
    auth_token = '7a0077352b970daa2f65fe27667ed130'
    client = Client(account_sid, auth_token)

    for info in result:
        print(info)
        vending_machineid = info["_id"]
        products_info = info["products"]  # Rename to avoid conflict with outer loop
        print(f"{vending_machineid} contains the following products with quantities <= 5:")
        for product in products_info:  # Rename to avoid conflict with outer loop
            print(f"{product['name']}: {product['quantity']}")

        # twilio if you don't comment it's going to send messages to my phone XD
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Product quantity is low: ' + ', '.join(
                [f"{vending_machineid}:{product['name']}: {product['quantity']}" for product in products_info]),
             to='whatsapp:+32493350344'
        )

        print("Quantity low message sent. SID:", message.sid)
    return f"You are going to just say I checked your stocks  "

def get_vending_machine_info(machine_id):
    vending_machine_data = get_vending_machine_data(machine_id)

    if vending_machine_data:
        temperature = vending_machine_data.get('temp')
        humidity = vending_machine_data.get('humidity')
        status = vending_machine_data.get('status')

        if temperature is not None and humidity is not None:
            info = f"Machine ID: {machine_id}\nTemperature: {temperature}°C, Humidity: {humidity}%, Status: {status}"
            return info
        else:
            # Handle the case where temperature, humidity, or status data is missing
            return "Data not available or incomplete."
    else:
        return f"Machine with ID {machine_id} not found."