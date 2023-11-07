from data import mongodb_data
from functions.data_convert import *


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