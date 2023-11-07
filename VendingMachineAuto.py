# Vending machine data ophalen
from random import random

from main import product_list, example_sales_init


def automatic_purchase(product_id, quantity_to_buy, product_data=None):
    random_product_id = random.choice(product_list)["product_id"]

    if random_product_id:
        current_inventory = product_data.get("quantity", 0)

        if current_inventory >= quantity_to_buy:
            # Update the inventory with the new quantity
            updated_inventory = current_inventory - quantity_to_buy
            product_list.update_one(
                {"_id": product_id},
                {"$set": {"quantity": updated_inventory}}
            )

            # Perform the purchase process here (e.g., deduct payment)

            return f"Purchased {quantity_to_buy} units of {product_data['product_name']}."

    return "Product not available or insufficient inventory."


def analyze_products_sold(inventory_collection=None):
    # Connect to your MongoDB and retrieve sales data and product inventory
    product_list = ["product_"]

    # Query MongoDB to get sales data
    sales_data = example_sales_init()

    products_sold = {}

    for sale in sales_data:
        product_id = sale["product_id"]
        quantity_sold = sale["quantity_sold"]

        if product_id in products_sold:
            products_sold[product_id] += quantity_sold
        else:
            products_sold[product_id] = quantity_sold

    # Retrieve product names from the inventory collection and display results
    product_summary = []
    for product_id, quantity_sold in products_sold.items():
        product_data = inventory_collection.find_one({"_id": product_id})
        product_name = product_data["product_name"]
        product_summary.append(f"{product_name}: {quantity_sold} units sold")

    return product_summary
