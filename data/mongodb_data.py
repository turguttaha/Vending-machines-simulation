from db_connections import mongodb_connection

# Connect to MongoDB once and reuse the connection
mongodb_instance = mongodb_connection.MongoDB("mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/ChatBotDB", "ChatBotDB")


# get all data
def get_all_data():
    collection = mongodb_instance.db["sales-0.1"]
    cursor = collection.find({})
    return cursor

def get_all_payment_and_times():
    payment_method_str_array = []
    payment_times_int_array = []
    for data in get_all_data():
        payment_method = data.get('paymentMethod')

        if payment_method not in payment_method_str_array:
            payment_method_str_array.append(payment_method)
            payment_times_int_array.append(1)
        else:
            index = payment_method_str_array.index(payment_method)
            payment_times_int_array[index] += 1
    return payment_method_str_array, payment_times_int_array

def print_all_data():
    datas = get_all_data()
    for data in datas:
        print(data)

