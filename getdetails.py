# get_user_details_gui.py

import sqlite3
import tkinter as tk
from tkinter import messagebox

def fetch_details():
    name = name_entry.get()

    if not name:
        messagebox.showwarning("Input Error", "Please enter a name.")
        return

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email, phone, age, dob FROM users WHERE name = ?', (name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        email, phone, age, dob = result
        output_text.set(f"Email: {email}\nPhone: {phone}\nAge: {age}\nDOB: {dob}")
    else:
        output_text.set("Details do not exist.")

# GUI setup
app = tk.Tk()
app.title("Get User Details")

tk.Label(app, text="Enter Name").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(app)
name_entry.grid(row=0, column=1, padx=10)

tk.Button(app, text="Search", command=fetch_details).grid(row=1, column=0, columnspan=2, pady=10)

output_text = tk.StringVar()
output_label = tk.Label(app, textvariable=output_text, justify="left", fg="blue")
output_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

app.mainloop()