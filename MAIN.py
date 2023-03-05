import requests
import json
from datetime import datetime, timedelta
from tkinter import Tk, Label, PhotoImage, messagebox

class WeatherApp:
    def __init__(self,api_key):
        self.api_key = api_key
        self.city_name = None
        self.temperature = None
        self.weather_description = None
        self.forecast_data = None
    def get_current_weather_data(self):
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={self.api_key}"
        response = requests.get(weather_url)    
        if response.status_code != 200:
            raise ValueError("Failed to get weather data")
        weather_data = json.loads(response.content)
        self.temperature = round(weather_data["main"]["temp"] - 273.15, 2)
        self.weather_description = weather_data["weather"][0]["description"].capitalize()
        self.weather_icon = weather_data["weather"][0]["icon"]
    def get_forecast_data(self):
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={self.city_name}&appid={self.api_key}"
        response = requests.get(forecast_url)
        if response.status_code != 200:
            raise ValueError("Failed to get forecast data")
        forecast_data = json.loads(response.content)["list"]
        self.forecast_data = []  
        for forecast in forecast_data:
            date_str = forecast["dt_txt"]
            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            if date.hour == 12:
                temperature = round(forecast["main"]["temp"] - 273.15, 2)
                weather_description = forecast["weather"][0]["description"].capitalize()
                weather_icon = forecast["weather"][0]["icon"]
                self.forecast_data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "time": date.strftime("%H:%M"),
                    "temperature": temperature,
                    "weather_description": weather_description,
                    "weather_icon": weather_icon
                })
    def get_weather_data(self, city_name):
        self.city_name = city_name
        self.get_current_weather_data()
        self.get_forecast_data()  

    def display_weather_data(self):
        root = Tk()  
        root.title(f"Weather in {self.city_name}")
        root.geometry("400*400")
        root.configure(bg="white")

        icon_url = f"http://openweathermap.org/img/wn/{self.weather_icon}.png"
        icon_data = requests.get(icon_url).content
        icon_image = PhotoImage(data=icon_data) 

        icon_label = Label(root, image=icon_image, bg="white")
        icon_label.pack()
        temperature_label = Label(root, text=f"{self.temperature}°C", font=("Arial", 40), bg="white")
        temperature_label.pack()
        weather_label = Label(root, text=self.weather_description, font=("Arial", 20), bg="white")
        weather_label.pack()     
        forecast_label = Label(root, text="Forecast:", font=("Arial", 20), bg="white")
        forecast_label.pack() 
        for forecast in self.forecast_data:
            date_label = Label(root, text=forecast["date"], font=("Arial", 16), bg="white")
            date_label.pack()
            time_label = Label(root, text=forecast["time"], font=("Arial", 16), bg="white")
                