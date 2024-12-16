#Import required modules
import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

#Function to get weather information from WeatherAPI
def get_weather(city):
    API_key = "6e3d7ca7988c9ece01bcfbc8f6d7680d"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    #Parse the response JSON to get weather information
    weather = res.json()
    icon_id = weather['weather'] [0] ['icon']
    temperature = weather['main'] ['temp'] - 273.15
    description = weather['weather'] [0] ['description']
    city = weather['name']
    country = weather['sys']['country']

    #Get the icon URL and return all weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}2x.png"
    return (icon_url, temperature, description, city, country)

#Function to search the weather for a city
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    #If the city is found unpack the weather information
    icon_url, temperature, description, city, country = result
    location_Label.configure(text=f"{city}, {country}")

    # Save the image data locally first
    response = requests.get(icon_url, stream=True)
    if response.status_code == 200:
        with open("weather_icon.png", "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print("Failed to download icon image")  # Inform the user if download fails
        return

    # Now open the saved image
    image = Image.open("weather_icon.png")
    icon = ImageTk.PhotoImage(image)
    icon_Label.configure(image=icon)
    icon_Label.image = icon

    #Update temperature and description labels
    temperature_Label.configure(text=f"Temperature: {temperature:.2f}°F")
    description_Label.configure(text=f"Description: {description}")

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x400")

# Entry widget -> to enter city name
city_entry = ttkbootstrap.Entry(root, font="Helvetica, 18")
city_entry.pack(pady=10)

#Button widget -> to search for the weather information
search_Button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning")
search_Button.pack(pady=10)

#Label widget -> to show the city/country name
location_Label = tk.Label(root, font="Helvetica, 25")
location_Label.pack(pady=20)

#Label widget -> to show weather icon
icon_Label = tk.Label(root, font="Helvetica, 20")
icon_Label.pack()

#Label widget -> to show temperature
temperature_Label = tk.Label(root, font="Helvetica, 20")
temperature_Label.pack()

#Label widget -> to show weather description
description_Label = tk.Label(root, font="Helvetica, 20")
description_Label.pack()

root.mainloop()