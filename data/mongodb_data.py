from db_connections import mongodb_connection
from data.data_convert import *
# Connect to MongoDB once and reuse the connection
mongodb_instance = mongodb_connection.MongoDB("mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/ChatBotDB",
                                              "ChatBotDB")


def get_vm_by_filter(key, value):
    return mongodb_instance.get_data_by_filter("Vending-Machines-0.1", key=key, value=value)


def update_vm_attribute(id_key, record_id, attribute_key, new_value):
    return mongodb_instance.update_data("Vending-Machines-0.1", id_key, record_id, attribute_key, new_value)


def update_vm_product_attribute(parent_id_key, parent_record_id, child_id_key, child_record_id, list_name,
                                attribute_key, new_value):
    return mongodb_instance.update_nested_list_object("Vending-Machines-0.1",
                                                      parent_id_key,
                                                      parent_record_id,
                                                      child_id_key,
                                                      child_record_id, list_name,
                                                      attribute_key,
                                                      new_value
                                                      )


def add_sale(sale_object):
    return mongodb_instance.add_data("sales-0.1",sale_object)
# get all data
def get_all_sales():
    collection = mongodb_instance.db["sales-0.1"]
    cursor = collection.find({})
    return cursor


def get_all_vending_machines():
    collection = mongodb_instance.db["Vending-Machines-0.1"]
    cursor = collection.find({})
    return cursor


def get_vending_machine_data(machine_id):
    collection = mongodb_instance.db["Vending-Machines-0.1"]
    query = {"vendingMachineID": machine_id}

    vending_machine_data = collection.find_one(query)

    return vending_machine_data


def get_all_payment_methods_and_times():
    payment_method_str_array = []
    payment_times_int_array = []
    for data in get_all_sales():
        payment_method = data.get('paymentMethod')

        if payment_method not in payment_method_str_array:
            payment_method_str_array.append(payment_method)
            payment_times_int_array.append(1)

        else:
            index = payment_method_str_array.index(payment_method)
            payment_times_int_array[index] += 1
    return payment_method_str_array, payment_times_int_array


def get_payment_methods_and_times_in_certain_period(start_date, end_date):
    sales = get_data_between_two_date("sales-0.1", start_date, end_date)
    payment_count = {}

    for sale in sales:
        payment_method = sale.get('paymentMethod')
        payment_count[payment_method] = payment_count.get(payment_method, 0) + 1

    return list(payment_count.keys()), list(payment_count.values())


def get_data_between_two_date(collection, start_date, end_date):
    collection = mongodb_instance.db[collection]
    query = {
        "timestamp": {
            "$gte": convert_date_str_to_timestamp(start_date),
            "$lte": convert_date_str_to_timestamp(end_date)
        }
    }
    return list(collection.find(query))
