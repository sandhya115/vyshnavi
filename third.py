# store_user_details_gui.py

import sqlite3
import tkinter as tk
from tkinter import messagebox

def create_table():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            email TEXT,
            phone TEXT,
            age INTEGER,
            dob TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_details():
    name = name_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    age = age_entry.get()
    dob = dob_entry.get()

    if not all([name, email, phone, age, dob]):
        messagebox.showwarning("Missing Data", "Please fill in all fields.")
        return

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (name, email, phone, age, dob)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, age, dob))
        conn.commit()
        messagebox.showinfo("Success", "Details saved successfully!")
        clear_fields()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "User with this name already exists.")
    finally:
        conn.close()

def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    dob_entry.delete(0, tk.END)

# GUI setup
create_table()

app = tk.Tk()
app.title("Store User Details")

tk.Label(app, text="Name").grid(row=0, column=0, pady=5)
tk.Label(app, text="Email").grid(row=1, column=0, pady=5)
tk.Label(app, text="Phone Number").grid(row=2, column=0, pady=5)
tk.Label(app, text="Age").grid(row=3, column=0, pady=5)
tk.Label(app, text="Date of Birth (YYYY-MM-DD)").grid(row=4, column=0, pady=5)

name_entry = tk.Entry(app)
email_entry = tk.Entry(app)
phone_entry = tk.Entry(app)
age_entry = tk.Entry(app)
dob_entry = tk.Entry(app)

name_entry.grid(row=0, column=1)
email_entry.grid(row=1, column=1)
phone_entry.grid(row=2, column=1)
age_entry.grid(row=3, column=1)
dob_entry.grid(row=4, column=1)

tk.Button(app, text="Save", command=save_details).grid(row=5, column=0, columnspan=2, pady=10)

app.mainloop()
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
