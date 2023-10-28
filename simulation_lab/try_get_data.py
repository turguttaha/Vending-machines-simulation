from functions.sales_operations import *
from db_connections.mongodb_connection import *

if __name__ == "__main__":
    print(get_profit_certain_period(2021, 2022)) # out put 0
    for i in get_all_data():
        print(i)

