from pymongo import MongoClient


class MongoDB:
    def __init__(self, connection_string, db_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

    def add_data(self, collection_name, data):
        collection = self.db[collection_name]
        #inserted_product = collection.insert_one(data)
        return collection.insert_one(data)
        #print("Added product id:", inserted_product.inserted_id)

    # data oproepen
    def get_data_by_filter(self, collection_name, key, value):
        collection = self.db[collection_name]
        query = {key: value}
        result = collection.find(query)
        return result

    # update data
    def update_data(self, collection_name, id_key, record_id, attribute_key, new_value):
        collection = self.db[collection_name]
        query = {id_key: record_id}
        new_values = {"$set": {attribute_key: new_value}}
        return collection.update_one(query, new_values)

    # update products attributes which is in the vending machine object
    def update_nested_list_object(self, collection_name,
                                  parent_id_key,
                                  parent_record_id,
                                  child_id_key,
                                  child_record_id, list_name,
                                  attribute_key,
                                  new_value):

        collection = self.db[collection_name]
        filter = {parent_id_key: parent_record_id,
                  f"{list_name}.{child_id_key}": child_record_id }
        collection.update_one(
            filter=filter,
            update={"$set": {f"{list_name}.$.{attribute_key}": new_value}})

    # verwideren
    def delete_data(self, collection_name, id_key, record_id):
        collection = self.db[collection_name]
        query = {id_key: record_id}
        collection.delete_one(query)
