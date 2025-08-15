# Idea: Random Password Generator
# Description:
# For Beginners: Create a command-line password generator in Python that generates random
# passwords based on user-defined criteria, such as length and character types (letters, numbers,
# symbols). Allow users to specify password length and character set preferences.
# For Advanced: Develop an advanced password generator with a graphical user interface (GUI)
# using Tkinter or PyQt. Enhance it by including options for password complexity, adherence to
# security rules, and clipboard integration for easy copying.
# Key Concepts and Challenges:
# 1.Randomization: Learn how to generate random characters and strings.
# 2.User Input Validation: Validate user input for password length and character types.
# 3.Character Set Handling: Manage different character sets (letters, numbers, symbols).
# 4.GUI Design (for Advanced): Create an intuitive and user-friendly interface for password
# generation.
# 5.Security Rules (for Advanced): Implement rules for generating strong, secure passwords.
# 6.Clipboard Integration (for Advanced): Allow users to copy generated passwords to the
# clipboard for convenience.
# 7.Customization (for Advanced): Enable users to customize password generation further, e.g.,
# excluding specific characters.

import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip


def generate_password():
    length = length_var.get()

    if length < 4:
        messagebox.showerror("Error", "Password length must be at least 4.")
        return

    characters = ""
    if letters_var.get():
        characters += string.ascii_letters
    if numbers_var.get():
        characters += string.digits
    if symbols_var.get():
        characters += string.punctuation

    if not characters:
        messagebox.showerror("Error", "Please select at least one character type.")
        return

    password = ''.join(random.choice(characters) for _ in range(length))
    password_var.set(password)


def copy_to_clipboard():
    password = password_var.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password to copy!")


# GUI Setup
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("400x300")
root.config(bg="#f0f0f0")

# Variables
length_var = tk.IntVar(value=12)
letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
password_var = tk.StringVar()

# Widgets
tk.Label(root, text="Password Length:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=5)
tk.Spinbox(root, from_=4, to=50, textvariable=length_var, width=5).pack()

tk.Checkbutton(root, text="Include Letters (A-Z, a-z)", variable=letters_var, bg="#f0f0f0").pack(anchor="w", padx=50)
tk.Checkbutton(root, text="Include Numbers (0-9)", variable=numbers_var, bg="#f0f0f0").pack(anchor="w", padx=50)
tk.Checkbutton(root, text="Include Symbols (!@#$)", variable=symbols_var, bg="#f0f0f0").pack(anchor="w", padx=50)

tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

tk.Entry(root, textvariable=password_var, font=("Arial", 12), width=30, justify="center").pack(pady=5)

tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=5)

root.mainloop()
