# Idea: Basic Weather App
# Description:
# For Beginners: Create a command-line weather app in Python that fetches and displays current
# weather data for a user-specified location (e.g., city or ZIP code) using a weather API. Show
# basic information such as temperature, humidity, and weather conditions.
# For Advanced: Develop a graphical weather app with a user-friendly interface (GUI) using
# libraries like Tkinter or PyQt. Enable users to input their location or use GPS for automatic
# detection. Provide detailed weather data, including current conditions, hourly and daily
# forecasts, wind speed, and visual elements like weather icons.
# Key Concepts and Challenges:
# 1. API Integration: Connect to a weather API and parse JSON data.
# 2. User Input Handling: Validate and process user input for location.
# 3. GUI Design (for Advanced): Create a user-friendly interface with input fields, weather data
# displays, and visual elements.
# 4. GPS Integration (for Advanced): Implement location detection if developing a mobile app.
# 5. Error Handling: Address potential errors during data retrieval or user input.
# 6. Data Visualization (for Advanced): Display weather data in an appealing manner, possibly
# using icons or animations.
# 7. Unit Conversion (for Advanced): Offer unit options for temperature (e.g., Celsius and
# Fahrenheit).

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import io

API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
ICON_URL = "https://openweathermap.org/img/wn/{}@2x.png"

def get_weather(location, units='metric'):
    params = {"q": location, "appid": API_KEY, "units": units}
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("API Request Error:", e)
        return None

def update_weather():
    location = location_entry.get().strip()
    if not location:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return
    units = 'metric' if units_var.get() == "Celsius" else 'imperial'
    data = get_weather(location, units)

    if not data or data.get("cod") != 200:
        messagebox.showerror("Error", f"Could not find weather for '{location}'.")
        return

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"].title()
    wind = data["wind"]["speed"]
    icon_code = data["weather"][0]["icon"]

    temp_label.config(text=f"{temp}°{'C' if units == 'metric' else 'F'}")
    desc_label.config(text=desc)
    wind_label.config(text=f"Wind {wind} {'m/s' if units == 'metric' else 'mph'}")

    icon_response = requests.get(ICON_URL.format(icon_code))
    img_data = icon_response.content
    img = Image.open(io.BytesIO(img_data))
    img = img.resize((70, 70), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(img)
    icon_label.config(image=photo)
    icon_label.image = photo

root = tk.Tk()
root.title("Mini Weather")
root.geometry("200x350")
root.configure(bg='#202530')
root.resizable(False, False)

# Card frame with padding
card = tk.Frame(root, bg="#282e3a")
card.place(relwidth=0.92, relheight=0.92, relx=0.04, rely=0.04)

# Padding sizes
padx = 10
pady = 7

# City input
location_entry = tk.Entry(card, font=("Segoe UI", 12), justify="center", bd=2, relief="groove")
location_entry.pack(padx=padx, pady=(18, 6), fill="x")

# Unit selection
units_var = tk.StringVar(value="Celsius")
unit_menu = tk.OptionMenu(card, units_var, "Celsius", "Fahrenheit")
unit_menu.config(font=("Segoe UI", 9), bg="#364052", fg="white", relief="flat", bd=1,
                 highlightthickness=1, highlightbackground="#404855")
unit_menu.pack(padx=padx, pady=(0, 10), fill="x")

# Search button
search_btn = tk.Button(card, text="Get Weather", font=("Segoe UI", 10, 'bold'),
                       bg="#388bfd", fg="white", activebackground="#2994ff",
                       relief="flat", command=update_weather, height=1)
search_btn.pack(padx=padx, pady=(0, 15), fill="x")

# Weather icon
icon_label = tk.Label(card, bg="#282e3a")
icon_label.pack(pady=(0, 8))

# Weather info
temp_label = tk.Label(card, text="--°C", font=("Segoe UI", 18, "bold"), fg="#fafafa", bg="#282e3a")
temp_label.pack(pady=(0, 3))

desc_label = tk.Label(card, text="Weather", font=("Segoe UI", 11), fg="#c1c1c1", bg="#282e3a")
desc_label.pack(pady=(0, 1))

wind_label = tk.Label(card, text="Wind --", font=("Segoe UI", 9), fg="#85aaff", bg="#282e3a")
wind_label.pack()

root.mainloop()
