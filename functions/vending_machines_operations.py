import matplotlib.pyplot as plt


def payment_methode_analysis(payment_methode_str_array, payment_times_int_array):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    plt.bar(payment_methode_str_array, payment_times_int_array)
    plt.title("Betaalmethode Analiseren")
    plt.show()
