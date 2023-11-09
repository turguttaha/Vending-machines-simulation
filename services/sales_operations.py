from matplotlib import pyplot as plt
from datetime import datetime
from data import mongodb_data

def get_profit_certain_period(start_date, end_date):
    sales = mongodb_data.get_data_between_two_date("sales-0.1", start_date, end_date)
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
def get_most_sold_items(start_date, end_date):
    sales = mongodb_data.get_data_between_two_date("sales-0.1", start_date, end_date)

    product_sales_count = {}
    product_name_list = {}
    for sale in sales:
        product = sale.get("product")
        product_id = product["productID"]
        if product_id in product_sales_count:
            product_sales_count[product_id] += 1
        else:
            product_sales_count[product_id] = 1
        if product_id not in product_name_list:
            product_name_list[product_id] = product["name"]

    # Find the key-value pair with the highest value type will be tupples
    max_pair = max(product_sales_count.items(), key=lambda item: item[1])

    highest_key, highest_value = max_pair

    product_name = product_name_list[highest_key]

    return f"{product_name} is most sold product with amount {highest_value}"

def get_most_profitable_product(start_date, end_date):
    sales = mongodb_data.get_data_between_two_date("sales-0.1", start_date, end_date)

    product_profits = {}
    product_name_list = {}
    for sale in sales:
        product = sale.get("product")
        product_id = product["productID"]
        profit = product["price"] * product["profit percentage"] / 100
        if product_id in product_profits:
            product_profits[product_id] += profit
        else:
            product_profits[product_id] = profit
        if product_id not in product_name_list:
            product_name_list[product_id] = product["name"]

    # Find the key-value pair with the highest value type will be tupples
    max_pair = max(product_profits.items(), key=lambda item: item[1])

    highest_key, highest_value = max_pair

    product_name = product_name_list[highest_key]

    return f"{product_name} is most profitable product with profit {highest_value}"

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
    payment_method_str_array, payment_times_int_array = mongodb_data.get_payment_methods_and_times_in_certain_period(start_date,
                                                                                                                     end_date)

    # Analyze the payment methods
    analyze_payment_method_in_table(payment_method_str_array, payment_times_int_array, start_date, end_date)
