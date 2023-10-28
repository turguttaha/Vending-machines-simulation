from pymongo import MongoClient


# client = MongoClient("mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/ChatBotDB")
# db = client.get_database()

# data toevoegen
# data = {
#     "product_id": 1,
#     "product_name": "product 1",
#     "price": 10.99
# }


class MongoDB:
    def __init__(self, connection_string, db_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

    def add_data(self, collection_name, data):
        collection = self.db[collection_name]
        inserted_product = collection.insert_one(data)
        print("Added product id:", inserted_product.inserted_id)

    # data oproepen
    def call_data(self, collection_name, id_key, record_id):
        collection = self.db[collection_name]
        query = {id_key: record_id}
        result = collection.find(query)
        return result

    # update data
    def update_data(self, collection_name, id_key, record_id, update_key_id, new_value):
        collection = self.db[collection_name]
        query = {id_key: record_id}
        new_values = {"$set": {update_key_id: new_value}}
        collection.update_one(query, new_values)

    # update products attributes which is in the vending machine object

    # db["ChatBotDB-Release-0.1"].update_one({"vendingMachineID":"VM001" },{"$set": {"products.$[elem].quantity": 9}},
    # array_filters=[{"elem.productID":"P001"}])
    # verwideren
    def delete_data(self, collection_name, id_key, record_id):
        collection = self.db[collection_name]
        query = {id_key: record_id}
        collection.delete_one(query)
