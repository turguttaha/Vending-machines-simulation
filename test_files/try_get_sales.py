from services.sales_operations import *
import time

if __name__ == "__main__":
    while True:
        user_input_start_date = input("Give a start date: ")
        user_input_end_date = input("Give a end date: ")
        user_message_timestamp = time.time()

        print("Profit: ", get_profit_certain_period(user_input_start_date, user_input_end_date))
        bot_response_timestamp = time.time()
        response_time = bot_response_timestamp - user_message_timestamp
        print(f"Response time: {response_time} seconds")