# Idea: BMI Calculator
# Project Description:
# For Beginners: Create a command-line BMI calculator in Python. Prompt users for their
# weight (in kilograms) and height (in meters). Calculate the BMI and classify it into categories
# (e.g., underweight, normal, overweight) based on predefined ranges. Display the BMI result and
# category to the user.
# For Advanced: Develop a graphical BMI calculator with a user-friendly interface (GUI) using
# libraries like Tkinter or PyQt. Allow users to input weight and height, calculate BMI, and
# visualize the result. Enable data storage for multiple users, historical data viewing, and BMI
# trend analysis through statistics and graphs.
# Key Concepts and Challenges:
# 1. User Input Validation: Ensure valid user inputs within reasonable ranges and handle errors
# gracefully.
# 2. BMI Calculation: Accurately implement the BMI formula.
# 3. Categorization: Classify BMI values into health categories based on predefined ranges.
# 4. GUI Design (for Advanced): Create an intuitive interface with labels, input fields, and result
# displays.
# 5. Data Storage (for Advanced): Implement user data storage, possibly using file storage or a
# small database.
# 6. Data Visualization (for Advanced): Visualize historical BMI data with graphs or charts.
# 7. Error Handling (for Advanced): Address potential issues with data storage or retrieval.
# 8. User Experience (for Advanced): Ensure a responsive and user-friendly GUI with clear
# instructions and feedback.

import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# Database setup
DB_FILE = "BMI Calculator\Bmi_data.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')
    # BMI records table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            weight REAL,
            height REAL,
            bmi REAL,
            category TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# Load users from DB
def load_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name FROM users ORDER BY name ASC")
    users = [row[0] for row in c.fetchall()]
    conn.close()
    return users

# Add new user
def add_user():
    new_user = simpledialog.askstring("Add User", "Enter new user's name:")
    if new_user:
        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO users (name) VALUES (?)", (new_user,))
            conn.commit()
            conn.close()
            refresh_user_list()
            messagebox.showinfo("User Added", f"User '{new_user}' added successfully.")
        except sqlite3.IntegrityError:
            messagebox.showinfo("Duplicate User", f"User '{new_user}' already exists.")

# Save BMI record to DB
def save_record(user, weight, height, bmi, category):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE name=?", (user,))
    user_id = c.fetchone()[0]
    c.execute('''
        INSERT INTO bmi_records (user_id, date, weight, height, bmi, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, bmi, category))
    conn.commit()
    conn.close()

# BMI Calculation
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Show historical BMI graph
def show_graph():
    user = selected_user.get()
    if not user or user == "Select User":
        messagebox.showerror("Missing Name", "Please select a user to view graph.")
        return

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE name=?", (user,))
    user_id = c.fetchone()[0]
    c.execute("SELECT date, bmi FROM bmi_records WHERE user_id=? ORDER BY date", (user_id,))
    records = c.fetchall()
    conn.close()

    if not records:
        messagebox.showinfo("No Data", f"No BMI records found for {user}.")
        return

    dates = [r[0] for r in records]
    bmis = [r[1] for r in records]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, marker="o")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"BMI Trend for {user}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Refresh dropdown menu
def refresh_user_list():
    menu = user_dropdown["menu"]
    menu.delete(0, "end")
    users = ["Select User"] + load_users()
    for u in users:
        menu.add_command(label=u, command=lambda value=u: selected_user.set(value))
    selected_user.set("Select User")

# Handle BMI calculation
def on_calculate():
    try:
        user = selected_user.get()
        if not user or user == "Select User":
            raise ValueError("Please select a user.")

        weight = float(weight_entry.get())
        height = float(height_entry.get())

        # Validation
        if not (20 <= weight <= 300):
            raise ValueError("Weight must be between 20–300 kg.")
        if not (0.5 <= height <= 2.5):
            raise ValueError("Height must be between 0.5–2.5 m.")

        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)

        result_label.config(text=f"BMI: {bmi:.2f} ({category})")
        save_record(user, weight, height, bmi, category)
        messagebox.showinfo("BMI Result", f"User: {user}\nYour BMI is {bmi:.2f} ({category})\nRecord saved!")

    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

# --- Tkinter UI ---
init_db()  # Create tables if not exist
root = tk.Tk()
root.title("Advanced BMI Calculator - SQLite Version")
root.geometry("420x320")
root.resizable(False, False)

tk.Label(root, text="Select User:").pack(pady=5)

# Frame for dropdown + Add button side-by-side
user_frame = tk.Frame(root)
user_frame.pack(pady=5)

selected_user = tk.StringVar()
users = ["Select User"] + load_users()
selected_user.set("Select User")

user_dropdown = tk.OptionMenu(user_frame, selected_user, *users)
user_dropdown.pack(side="left", padx=5)

tk.Button(user_frame, text="Add User", command=add_user, bg="lightyellow").pack(side="left", padx=5)

tk.Label(root, text="Weight (kg):").pack(pady=5)
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (m):").pack(pady=5)
height_entry = tk.Entry(root)
height_entry.pack()

tk.Button(root, text="Calculate BMI", command=on_calculate, bg="lightblue").pack(pady=10)
tk.Button(root, text="Show BMI Graph", command=show_graph, bg="lightgreen").pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

root.mainloop()
