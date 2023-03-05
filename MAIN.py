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