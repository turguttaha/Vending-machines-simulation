from datetime import time

from data import mongodb_data

vending_machine_state = mongodb_data.mongodb_instance.db["ChatBotDB.ChatBotDB-Release-0.1"]


def update_vending_machine_state(machine_id, new_state):
    vending_machine_state.update_one({"vendingMachineID": machine_id}, {"$set": {"status": new_state}})


def create_new_sales_object(machine_id, products, paymentmethod):
    sales = mongodb_data.mongodb_instance.db["sales-0.1"]
    sales.insert_one({
        "timestamp": int(time.time()),
        "vendingMachineID": machine_id,
        "product": products,
        "paymentMethod": paymentmethod,

    })


def get_new_state_from_machine(machine_id):
    vending_machine_state.find(machine_id)
    timestamp = machine["timestamp"]
    current_time = int(time.time())

    time_difference = current_time - timestamp

    # Define the time intervals for each state
    sold_time_interval = 30
    dispensed_time_interval = 15
    dispensing_time_interval = 5
    idle_time_interval = 60

    # Determine the state of the vending machine based on the time difference
    if time_difference < sold_time_interval:
        return "SOLD"
    elif time_difference < dispensed_time_interval:
        return "DISPENSED"
    elif time_difference < dispensing_time_interval:
        return "DISPENSING"
    elif time_difference < idle_time_interval:
        return "IDLE"
    else:
        return "OUT_OF_ORDER"


while True:
    machine_lists = list(vending_machine_state.find())

    for machine in machine_lists:
        machine_id = machine["vendingMachineID"]
        new_state = get_new_state_from_machine(machine)
        update_vending_machine_state(machine_id, new_state)

        # Check if a sale has been made
        if new_state == "SOLD":
            # product_name, price = get_product_name_and_price_from_machine(machine)
            create_new_sales_object(machine_id)

    # Wait for 15 minutes before updating the vending machines again
    time.sleep(900)
