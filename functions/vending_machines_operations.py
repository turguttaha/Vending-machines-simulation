import matplotlib.pyplot as plt
from data import mongodb_data
from datetime import datetime


def payment_methode_analysis(payment_methode_str_array, payment_times_int_array, start_date=None, end_date=None):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    if start_date and end_date:
        # start_date_str = datetime.fromtimestamp(start_date).strftime('%Y-%m-%d')
        # end_date_str = datetime.fromtimestamp(end_date).strftime('%Y-%m-%d')
        plt.title(f"Betaalmethode Analiseren van {start_date} tot {end_date}")
    else:
        plt.title("Betaalmethode Analiseren")

    plt.bar(payment_methode_str_array, payment_times_int_array)
    plt.show()


def payment_methode_analysis_in_certain_period(start_date, end_date):

    # Parse the datetime string into a datetime object
    start_date_datetime = datetime.strptime(start_date, "%Y/%m/%d")
    end_date_datetime = datetime.strptime(end_date, "%Y/%m/%d")


    # Convert it to Epoch timestamp

    start_epoch_timestamp = start_date_datetime.timestamp()
    end_epoch_timestamp = end_date_datetime.timestamp()

    payment_method_str_array, payment_times_int_array = mongodb_data.get_payment_and_times_in_certain_period(start_epoch_timestamp,
                                                                                                             end_epoch_timestamp)
    payment_methode_analysis(payment_method_str_array, payment_times_int_array, start_date, end_date)
