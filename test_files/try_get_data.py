from data.mongodb_data import *
from simulation_lab.vending_machines_simulations import *
from services.vending_machines_operations import *
# def print_all_data():
#     datas = get_payment_methods_and_times_in_certain_period("2021/1/1", "2022/1/1")
#     teller = 0
#     for data in datas:
#         print(data)
#         teller += 1
#     print("Totaal: ", teller)
if __name__ == "__main__":
    #print(get_payment_methods_and_times_in_certain_period("2021/1/1", "2022/1/1"))
    #print_all_data()
    # filtered_list= mongodb_instance.get_data_by_id("sales-0.1","paymentMethod","cash")
    #
    # for data in filtered_list:
    #     print(data)
    #sell_item_from_vm("VM001")
    #check_low_inventory()
    reload_vm()
