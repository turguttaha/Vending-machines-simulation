from pymongo import MongoClient

client = MongoClient("mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/ChatBotDB")
db = client.get_database()

# data toevoegen

# data = {
#     "product_id": 1,
#     "product_name": "product 1",
#     "price": 10.99
# }
def add_data(collection_name,data):
    collection = db[collection_name]
    inserted_product = collection.insert_one(data)
    print("toegevoegde product id :", inserted_product.inserted_id)

# data oproepen
def call_data(collection_name,id_key ,id):
    collection = db[collection_name]
    query = {id_key: id}
    result = collection.find(query)
    return result

# update data
def update_data(collection_name,id_key ,id,update_key_id,new_value):
    collection = db[collection_name]
    query = {id_key: id}
    new_values = {"$set": {update_key_id: new_value}}
    collection.update_one(query, new_values)



# verwideren
def delete_data(collection_name,id_key ,id):
    collection = db[collection_name]
    query = {id_key: id}
    collection.delete_one(query)