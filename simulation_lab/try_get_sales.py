from functions.sales_operations import *

if __name__ == "__main__":
    while True:
        user_input_start_date = input("Give a start date: ")
        user_input_end_date = input("Give a end date: ")

        print("Profit: ", get_profit_certain_period(user_input_start_date, user_input_end_date))
