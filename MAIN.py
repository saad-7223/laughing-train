import requests
import json
from datetime import datetime, timedelta
from tkinter import Tk, Label, PhotoImage, messagebox

class WeatherApp: 
    def __init__(self, api_key):