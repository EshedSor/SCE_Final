import os
import requests
import json
from django.conf import settings
from datetime import datetime
import urllib
def generate_cities():
    endpoint = settings.CITIES_API_ENDPOINT
    res = requests.post(endpoint)
    if res.status_code == 200:
        try:
            return res.json()
        except requests.exceptions.JSONDecodeError:
            print("JSON Decode Error")
def load_cities():
    try:
        with open('cities.json', 'r', encoding='utf-8') as openfile:  # Specify encoding
            json_object = json.load(openfile)
        cities_list = []
        for i in json_object['result']['records']:  # Assuming json_object is a list of dictionaries
            cities_list.append((i['שם_ישוב'], i['שם_ישוב']))
        cities_list.sort()
        return cities_list
    except Exception as e:  # Catch and print the exception
        print(f"Error reading from cities file: {e}")
        return None

def save_cities():
    try:
        to_write = generate_cities()

        with open("cities.json", "w", encoding='utf-8') as outfile:
            json.dump(to_write, outfile, ensure_ascii=False, indent=4)
        print("Successfully written cities to file")
    except Exception as e:
        print("Error writing cities to file:", e)

def refresh_cities():
    if is_cities_expired():
        save_cities()
    return load_cities()

def is_cities_expired():
    return False if os.path.isfile("./cities.json") else True