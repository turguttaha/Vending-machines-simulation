from data import mongodb_data
from functions.data_convert_operations import *


def get_profit_certain_period(start_date, end_date):
    sales = fetch_data_from_db(mongodb_data.mongodb_instance.db["sales-0.1"], start_date, end_date)
    return str(sum(sale["product"]["price"] * sale["product"]["profit percentage"] / 100 for sale in sales))

    # # Parse the datetime string into a datetime object
    # start_date_datetime = datetime.strptime(start_date, "%Y/%m/%d")
    # end_date_datetime = datetime.strptime(end_date, "%Y/%m/%d")
    #
    # # Convert it to Epoch timestamp
    #
    # start_epoch_timestamp = start_date_datetime.timestamp()
    # end_epoch_timestamp = end_date_datetime.timestamp()
    #
    # collection = mongodb_data.mongodb_instance.db["sales-0.1"]
    #
    # query = {
    #     "timestamp": {
    #         "$gte": start_epoch_timestamp,
    #         "$lte": end_epoch_timestamp
    #     }
    # }
    # total_profit = 0
    # for sale in list(collection.find(query)):
    #     total_profit += sale["product"]["price"] * sale["product"]["profit percentage"] / 100
    #
    # return str(total_profit)


###########################################
def get_most_sold_items(start_date, end_date):
    sales = fetch_data_from_db(mongodb_data.mongodb_instance.db["sales-0.1"], start_date, end_date)

    product_sales_count = {}
    for sale in sales:
        product = sale.get("product")
        if product and "id" in product:
            product_id = product["id"]
            if product_id in product_sales_count:
                product_sales_count[product_id] += 1
            else:
                product_sales_count[product_id] = 1

    most_sold_products = [k for k, v in product_sales_count.items() if v == max(product_sales_count.values())]

    return most_sold_products


def get_most_profitable_product(start_date, end_date):
    sales = fetch_data_from_db(mongodb_data.mongodb_instance.db["sales-0.1"], start_date, end_date)

    product_profits = {}
    for sale in sales:
        product = sale.get("product")
        if product and "id" in product:
            product_id = product["id"]
            profit = product["price"] * product["profit percentage"] / 100
            if product_id in product_profits:
                product_profits[product_id] += profit
            else:
                product_profits[product_id] = profit

    most_profitable_product_id = max(product_profits, key=product_profits.get)

    return most_profitable_product_id

###########################################
def calculate_most_profitable_machine(start_date, end_date ):
    start_date_datetime = datetime.strptime(start_date, "%Y/%m/%d")
    end_date_datetime = datetime.strptime(end_date, "%Y/%m/%d")

    # Convert it to Epoch timestamp

    start_epoch_timestamp = start_date_datetime.timestamp()
    end_epoch_timestamp = end_date_datetime.timestamp()

    sales_collection = mongodb_data.mongodb_instance.db["sales-0.1"]

    most_profitable_machine = None
    max_profit = 0

    for vendingMachineID in sales_collection.distinct("vendingMachineID"):
        # Calculate profit for the specified time period
        cursor = sales_collection.find({
            "vendingMachineID": vendingMachineID,
            "timestamp": {"$gte": start_epoch_timestamp, "$lte": end_epoch_timestamp}
        })
        profit = sum(doc["product"]["price"] * doc["product"]["profit percentage"] /100 for doc in cursor)

        if profit > max_profit:
            max_profit = profit
            most_profitable_machine = vendingMachineID

    vending_machine_collection = mongodb_data.mongodb_instance.db["Vending-Machines-0.1"]

    found_vm = vending_machine_collection.find({"vendingMachineID": most_profitable_machine})
    location = found_vm[0]["location"]


    return f"Vending Machine Located in : {location},with the given ID  :{most_profitable_machine},has Profit of :{max_profit}"
# can be this as well profit = sum(doc["sales_amount"] * 0.3 for doc in cursor)
#Most profitable machine is located:{location}

