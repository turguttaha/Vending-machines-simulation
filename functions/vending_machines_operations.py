from multiprocessing.connection import Client

import matplotlib.pyplot as plt
import matplotlib
import pymongo

from data import mongodb_data
from datetime import datetime

from data.mongodb_data import get_vending_machine_data

matplotlib.use('TkAgg')


def analyze_payment_method_in_table(payment_methode_str_array, payment_times_int_array, start_date=None, end_date=None):
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['axes.unicode_minus'] = False

    if start_date and end_date:
        # start_date_str = datetime.fromtimestamp(start_date).strftime('%Y-%m-%d')
        # end_date_str = datetime.fromtimestamp(end_date).strftime('%Y-%m-%d')
        plt.title(f"Betaalmethode Analiseren van {start_date} tot {end_date}")
    else:
        plt.title("Betaalmethode Analiseren")

    plt.bar(payment_methode_str_array, payment_times_int_array)
    plt.show()


def analyze_payment_method_in_period(start_date, end_date):
    # Ensure the dates are in the correct format
    try:
        datetime.strptime(start_date, "%Y/%m/%d")
        datetime.strptime(end_date, "%Y/%m/%d")
    except ValueError:
        raise ValueError("The date format is incorrect. Expected format: %Y/%m/%d")

    # Fetch the payment methods and their counts for the given period using string dates
    payment_method_str_array, payment_times_int_array = mongodb_data.get_payment_and_times_in_certain_period(start_date,
                                                                                                             end_date)

    # Analyze the payment methods
    analyze_payment_method_in_table(payment_method_str_array, payment_times_int_array, start_date, end_date)
def quantity_low_message():

    client = pymongo.MongoClient("mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/")
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
    account_sid = 'AC40db2b8f896e5642cc81a0ca6ab7131e'
    auth_token = '2fc5915e3f00ae22279ea818bd0cc0fc'
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
             to='whatsapp:+32466162282'
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