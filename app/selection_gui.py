import tkinter as tk
from tkinter import filedialog, messagebox
from app.chat_gui import *
from functions import financial_operations
from pymongo import MongoClient

class SelectionGUI:
    def __init__(self, master, username, bedrijfname):
        self.master = master
        self.current_username = username
        self.current_bedrijfname = bedrijfname
        self.master.title('Selection Panel')

        # Clear previous UI
        for widget in self.master.winfo_children():
            widget.destroy()

        # Add button
        tk.Button(self.master, text="Chat", command=self.open_chat_ui).grid(row=0, column=0, padx=20, pady=10)
        tk.Button(self.master, text="Upload File", command=self.upload_file).grid(row=0, column=1, padx=20, pady=10)

    def open_chat_ui(self):
        # Create Chat UI
        chat_ui = ChatGUI(self.master, self.current_username, self.current_bedrijfname)
        return chat_ui

    def upload_file(self):
        mongo_uri = "mongodb+srv://yasir:chatBot@chatbot.nrdo6xw.mongodb.net/ChatBotDB"
        bedrijfname = self.current_bedrijfname

        # Get EXCEL data
        data = financial_operations.read_excel_and_convert_to_dict()

        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client.ChatBotDB

        # Check if the collection of bedrijfname exists, create it if it does not exist
        if bedrijfname not in db.list_collection_names():
            db.create_collection(bedrijfname)

        # Get collection
        collection = db[bedrijfname]

        # If the data is not empty, upload it to MongoDB
        if data:
            collection.insert_many(data)

        # Close MongoDB connection
        client.close()