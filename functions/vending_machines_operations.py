import matplotlib.pyplot as plt
from data import mongodb_data
from datetime import datetime


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
