import sqlite3
import re
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry  # You might need to install this: pip install tkcalendar

class UserRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Registration Form")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Setup database
        self.setup_database()
        
        # Create UI elements
        self.create_widgets()
        
    def setup_database(self):
        """Create database and table if they don't exist"""
        try:
            self.conn = sqlite3.connect('user_data.db')
            self.cursor = self.conn.cursor()
            
            # Create table if it doesn't exist
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                age INTEGER NOT NULL,
                dob TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            self.conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
    
    def create_widgets(self):
        """Create the form widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="User Registration Form", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Name
        ttk.Label(main_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Email
        ttk.Label(main_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.email_var, width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Phone
        ttk.Label(main_frame, text="Phone Number:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.phone_var, width=30).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Age
        ttk.Label(main_frame, text="Age:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.age_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.age_var, width=30).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Date of Birth
        ttk.Label(main_frame, text="Date of Birth:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.dob_frame = ttk.Frame(main_frame)
        self.dob_frame.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # If tkcalendar is available, use DateEntry
        try:
            self.dob_var = tk.StringVar()
            self.dob_entry = DateEntry(self.dob_frame, width=15, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            self.dob_entry.pack(side=tk.LEFT)
        except:
            # Fallback to regular entry if tkcalendar is not installed
            self.dob_var = tk.StringVar()
            ttk.Label(self.dob_frame, text="(YYYY-MM-DD)").pack(side=tk.RIGHT)
            ttk.Entry(self.dob_frame, textvariable=self.dob_var, width=15).pack(side=tk.LEFT)
        
        # Submit Button
        submit_btn = ttk.Button(main_frame, text="Register", command=self.submit_form)
        submit_btn.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Status Label
        self.status_var = tk.StringVar()
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="green")
        status_label.grid(row=7, column=0, columnspan=2)
        
        # Configure grid
        for i in range(8):
            main_frame.grid_rowconfigure(i, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
    
    def validate_inputs(self):
        """Validate form inputs"""
        name = self.name_var.get().strip()
        if not name or len(name) < 2:
            messagebox.showerror("Validation Error", "Name must be at least 2 characters long.")
            return False
        
        email = self.email_var.get().strip()
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            messagebox.showerror("Validation Error", "Please enter a valid email address.")
            return False
        
        phone = self.phone_var.get().strip()
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Validation Error", "Please enter a valid phone number (at least 10 digits).")
            return False
        
        age = self.age_var.get().strip()
        try:
            age_num = int(age)
            if not (0 < age_num < 120):
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid age between 1 and 119.")
            return False
        
        # Handle date from DateEntry or regular Entry
        try:
            if hasattr(self, 'dob_entry'):
                # Using DateEntry
                dob = self.dob_entry.get_date().strftime('%Y-%m-%d')
            else:
                # Using regular Entry
                dob = self.dob_var.get().strip()
                datetime.strptime(dob, '%Y-%m-%d')  # Validate format
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid date in YYYY-MM-DD format.")
            return False
        
        return True
    
    def submit_form(self):
        """Submit form data to the database"""
        if not self.validate_inputs():
            return
        
        try:
            # Get cleaned data
            name = self.name_var.get().strip()
            email = self.email_var.get().strip()
            phone = self.phone_var.get().strip()
            age = int(self.age_var.get().strip())
            
            # Get date from DateEntry or regular Entry
            if hasattr(self, 'dob_entry'):
                dob = self.dob_entry.get_date().strftime('%Y-%m-%d')
            else:
                dob = self.dob_var.get().strip()
            
            # Insert data into database
            self.cursor.execute('''
            INSERT INTO users (name, email, phone, age, dob)
            VALUES (?, ?, ?, ?, ?)
            ''', (name, email, phone, age, dob))
            
            self.conn.commit()
            
            # Show success message
            self.status_var.set(f"User '{name}' registered successfully!")
            
            # Clear form
            self.name_var.set("")
            self.email_var.set("")
            self.phone_var.set("")
            self.age_var.set("")
            if not hasattr(self, 'dob_entry'):
                self.dob_var.set("")
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save data: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def __del__(self):
        """Clean up database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = UserRegistrationApp(root)
    root.mainloop()