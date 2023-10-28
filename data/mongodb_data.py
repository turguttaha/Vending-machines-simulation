from db_connections.mongodb_connection import *

# Connect to MongoDB once and reuse the connection
mongodb_instance = MongoDB("mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/ChatBotDB", "ChatBotDB")

# get all data
def get_all_data():
    collection = mongodb_instance.db["sales-0.1"]
    cursor = collection.find()
    return cursor

def print_all_data():
    datas = get_all_data()
    for data in datas:
        print(data)
