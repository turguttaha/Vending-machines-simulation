from db_connections.mongodb_connection import *


# get all data
def get_all_data():
    client = MongoClient("mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/ChatBotDB")
    db = client.get_database()
    collection = db["sales-0.1"]
    cursor = collection.find()
    return cursor

def print_all_data():
    datas = get_all_data()
    for data in datas:
        print(data)
