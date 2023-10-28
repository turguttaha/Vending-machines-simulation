status = ["working","under maintenance","out of order"]
alerts = ["none","low inventory","maintenance required"]
payment_methodes = ["cash","creditcard","bankcontact"]
locations = ["UCLL Hertogstraat","UCLL Proximus","ING","Leuven Public Library","KU Leuven Library","KBC"]
product_list = [
                {
                    "productID": "P001",
                    "name": "Soda",
                    "price": 1.5,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "without aroma"
                },
                {
                    "productID": "P002",
                    "name": "Cola",
                    "price": 2.1,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "zero"
                },
                {
                    "productID": "P003",
                    "name": "Twix",
                    "price": 1.3,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "120 gr"
                },
                {
                    "productID": "P004",
                    "name": "Nutella B-ready",
                    "price": 1.7,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "white chocolate"
                },
                {
                    "productID": "P005",
                    "name": "Lays",
                    "price": 2.6,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "spicy"
                },
                {
                    "productID": "P006",
                    "name": "Water",
                    "price": 0.9,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "without sparkling"
                }
            ]
vendingMachineIDs = ["VM001","VM002","VM003","VM004","VM005","VM006"]

#products = {"P001":"Soda","P002":"Cola","P003":"Twix","P004":"Nutella B-ready"}

# example of the vending machine data and sales data

vending_machines_data = {
    "vendingMachineID": "VM001",
    "location": "KBC", # UCLL hertogstraat, UCLL proximus,ING, Leuven public library, KU Leuven library
    "status": "working", # other options under maintenance, out of order
    "alert": "none", # other options low inventory, maintenance required
    "temp":12.5,
    "humidity":70,
    "products": [
        {
            "productID": "P001",
            "name": "Soda",
            "price": 1.5,
            "quantity": 10,
            "description": "without aroma"
        },
        {
            "productID": "P002",
            "name": "Cola",
            "price": 2.1,
            "quantity": 10,
            "description": "zero"
        },
        {
            "productID": "P003",
            "name": "Twix",
            "price": 1.3,
            "quantity": 10,
            "description": "120 gr"
        },
        {
            "productID": "P004",
            "name": "Nutella B-ready",
            "price": 1.7,
            "quantity": 10,
            "description": "white chocolate"
        },
        {
            "productID": "P005",
            "name": "Lays",
            "price": 2.6,
            "quantity": 10,
            "description": "spicy"
        },
        {
            "productID": "P006",
            "name": "Water",
            "price": 0.9,
            "quantity": 10,
            "description": "without sparkling"
        }



    ]
}

sales_Data = {
    "timestamp":"1697358096", # e datetime in UNIX epoch time.
    "product":{
                    "productID": "P001",
                    "name": "Soda",
                    "price": 1.5,
                    "profit percentage": 30,
                    "quantity": 10,
                    "description": "without aroma"
                },
    "paymentMethod": "cash", # other option creditcard / bankcontact
    "vendingMachineID": "VM001"
}