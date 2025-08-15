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
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt

# File to store data
DATA_FILE = "BMI Calculator\Bmi_records.csv"

# Ensure CSV exists with header
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["User", "Date", "Weight (kg)", "Height (m)", "BMI", "Category"])

# Load users from CSV
def load_users():
    users = set()
    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.add(row["User"])
    return sorted(users)

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

# Save record to CSV
def save_record(user, weight, height, bmi, category):
    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([user, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), weight, height, round(bmi, 2), category])

# Show historical BMI graph for a specific user
def show_graph():
    user = selected_user.get()
    if not user or user == "Select User":
        messagebox.showerror("Missing Name", "Please select a user to view graph.")
        return

    dates, bmis = [], []
    with open(DATA_FILE, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["User"].lower() == user.lower():
                dates.append(row["Date"])
                bmis.append(float(row["BMI"]))

    if not dates:
        messagebox.showinfo("No Data", f"No BMI records found for {user}.")
        return

    plt.figure(figsize=(8, 4))
    plt.plot(dates, bmis, marker="o")
    plt.xticks(rotation=45, ha="right")
    plt.title(f"BMI Trend for {user}")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Add new user
def add_user():
    new_user = simpledialog.askstring("Add User", "Enter new user's name:")
    if new_user:
        current_users = load_users()
        if new_user in current_users:
            messagebox.showinfo("Duplicate User", f"User '{new_user}' already exists.")
        else:
            # Just add an empty record with today's date for recognition
            save_record(new_user, 0, 0, 0, "N/A")
            refresh_user_list()
            messagebox.showinfo("User Added", f"User '{new_user}' added successfully.")

# Refresh dropdown menu
def refresh_user_list():
    menu = user_dropdown["menu"]
    menu.delete(0, "end")
    users = ["Select User"] + load_users()
    for user in users:
        menu.add_command(label=user, command=lambda value=user: selected_user.set(value))
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

# Tkinter UI
root = tk.Tk()
root.title("Advanced BMI Calculator - Multiple Users")
root.geometry("400x320")
root.resizable(False, False)

# User Selection
selected_user = tk.StringVar()
users = ["Select User"] + load_users()
selected_user.set("Select User")

tk.Label(root, text="Select User:").pack(pady=5)

user_frame = tk.Frame(root)  # Frame to hold both widgets
user_frame.pack(pady=5)

user_dropdown = tk.OptionMenu(user_frame, selected_user, *users)
user_dropdown.pack(side="left", padx=5)

tk.Button(user_frame, text="Add User", command=add_user, bg="lightyellow").pack(side="left", padx=5)

# Weight & Height Input
tk.Label(root, text="Weight (kg):").pack(pady=5)
weight_entry = tk.Entry(root)
weight_entry.pack()

tk.Label(root, text="Height (m):").pack(pady=5)
height_entry = tk.Entry(root)
height_entry.pack()

# Buttons
tk.Button(root, text="Calculate BMI", command=on_calculate, bg="lightblue").pack(pady=10)
tk.Button(root, text="Show BMI Graph", command=show_graph, bg="lightgreen").pack(pady=5)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

root.mainloop()
# End of the BMI Calculator code