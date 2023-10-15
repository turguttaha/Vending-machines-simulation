client = MongoClient("mongodb://localhost:27017")
db = client["your_database_name"]


collection = db["products"]

# data toevoegen

data = {
    "product_id": 1,
    "product_name": "product 1",
    "price": 10.99
}

inserted_product = collection.insert_one(data)
print("toegevoegde product id :", inserted_product.inserted_id)

# data oproepen

query = {"product_name": "product 1"}
result = collection.find(query)

for product in result:
    print(product)

# update
query = {"product_name": "product 1"}
new_values = {"$set": {"price": 12.99}}
collection.update_one(query, new_values)

# verwideren
query = {"product_name": "product 1"}
collection.delete_one(query)