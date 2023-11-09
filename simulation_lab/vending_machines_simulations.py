from data.mongodb_data import *
import random
import time

payment_methods = ["cash", "creditcard", "bankcontact"]

def sell_item_from_all_vm():
    vendingMachineIDs = ["VM001", "VM002", "VM003", "VM004", "VM005", "VM006"]
    for vm_id in vendingMachineIDs:
        sell_item_from_vm(vm_id)
    check_low_inventory()

def sell_item_from_vm(vm_id):
    vm_object = get_vm_by_filter("vendingMachineID",vm_id)[0]
    # controle and change alert if it is needed with new function

    # controle vm status
    if vm_object["status"] == "working":
        random_product = random.choice(vm_object["products"])
        if random_product["quantity"] != 0:
            quantity = random_product["quantity"] - 1
            update_vm_product_attribute("vendingMachineID", vm_id, "productID", random_product["productID"],
                                    "products", "quantity", quantity)
            del random_product["quantity"]
            random_payment_method = random.choice(payment_methods)
            # create new sale object
            created_sale = create_new_sales_object(vm_id,random_product,random_payment_method)
            #print(created_sale.inserted_id)
            update_hum_temp(vm_id)
        else:
            pass


def update_hum_temp(vm_id):
    random_temp=random.uniform(10.0,15.5)
    update_vm_attribute("vendingMachineID",vm_id,"temp",random_temp)
    random_hum = random.randint(60, 75)
    update_vm_attribute("vendingMachineID", vm_id, "humidity", random_hum)


def create_new_sales_object(machine_id, product, payment_method):
    return add_sale({
        "timestamp": int(time.time()),
        "vendingMachineID": machine_id,
        "product": product,
        "paymentMethod": payment_method,

    })


def check_low_inventory():
    collection = mongodb_instance.db["Vending-Machines-0.1"]

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

    for r in result:
        update_vm_attribute("vendingMachineID",r["_id"],"alert","low inventory")

def reload_vm():
    vendingMachineIDs = ["VM001", "VM002", "VM003", "VM004", "VM005", "VM006"]
    for id in vendingMachineIDs:
        vm = get_vending_machine_data(id)
        if vm["alert"] == "low inventory":
            for p in vm["products"]:
                update_vm_product_attribute("vendingMachineID", vm["vendingMachineID"], "productID", p["productID"],
                                        "products", "quantity", 10)
            update_vm_attribute("vendingMachineID",vm["vendingMachineID"],"alert","none")
