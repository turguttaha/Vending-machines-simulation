import openai
import tkinter as tk
from functions.openai_operations import *
from functions.sales_operations import *
from functions.vending_machines_operations import *
import os
import data.openai_key

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")

        # Create chat history text box
        self.chat_history = tk.Text(root, state=tk.DISABLED)
        self.chat_history.pack()

        # Create the Frame where the user input box and send button are located
        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.BOTH)

        # Create user input box
        self.user_input = tk.Entry(input_frame)
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a send button
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def send_message(self):
        user_message = self.user_input.get()
        self.user_input.delete(0, tk.END)

        self.update_chat_history(f"You: {user_message}")
        # if "payment" or "analist" in user_message.lower():
        #     # use payment_methode_analysis to show table
        #     payment_methode_str_array = ["Cash", "Credit Card", "Mobile Payment"]
        #     payment_times_int_array = [20, 35, 15]
        #     payment_methode_analysis(payment_methode_str_array, payment_times_int_array)


        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_response = response.choices[0].message["content"]
        self.update_chat_history(f"Bot: {bot_response}")




    def update_chat_history(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()