import openpyxl
from functions.data_convert import *
from data import mongodb_data
from tkinter import filedialog, Tk

def create_excel_in_certain_period(start_date, end_date):
    # Fetch data from the database
    collection = mongodb_data.mongodb_instance.db["sales-0.1"]
    results = fetch_data_from_db(collection, start_date, end_date)

    # Sort the results by timestamp, and then by product name
    results.sort(key=lambda x: (x["timestamp"], x["product"]["name"]))

    # Create a new excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "MySheet"

    # Create titles for columns
    titles = ["Timestamp", "Product ID", "Name", "Price", "Profit Percentage", "Description", "Payment Method",
              "Vending Machine ID"]
    for col_num, title in enumerate(titles, 1):
        ws.cell(row=1, column=col_num, value=title)

    # Write data to the sheet
    for row_num, record in enumerate(results, 2):
        ws.cell(row=row_num, column=1, value=datetime.fromtimestamp(record["timestamp"]).strftime("%Y/%m/%d"))
        ws.cell(row=row_num, column=2, value=record["product"]["productID"])
        ws.cell(row=row_num, column=3, value=record["product"]["name"])
        ws.cell(row=row_num, column=4, value=record["product"]["price"])
        ws.cell(row=row_num, column=5, value=record["product"]["profit percentage"])
        ws.cell(row=row_num, column=6, value=record["product"]["description"])
        ws.cell(row=row_num, column=7, value=record["paymentMethod"])
        ws.cell(row=row_num, column=8, value=record["vendingMachineID"])

    # Use tkinter to choose save location
    root = Tk()
    root.withdraw()
    filename = filedialog.asksaveasfilename(initialfile=f"gegeven_van_{start_date.replace('/', '_')}_tot_{end_date.replace('/', '_')}.xlsx", defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])

    if filename:
        wb.save(filename)