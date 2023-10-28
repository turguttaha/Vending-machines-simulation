from db_connections.mongodb_connection import *


def get_profit_certain_period(start_date,end_date):
        collection = db["sales-0.1"]

        query = {
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }
        }
        total_profit = 0
        for sale in list(collection.find(query)):
            total_profit += sale["product"]["price"]* sale["product"]["profit percentage"]

        return str(total_profit)
