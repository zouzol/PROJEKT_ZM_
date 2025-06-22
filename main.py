import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup


def get_coordinates(location):
    try:
        url = f'https://pl.wikipedia.org/wiki/{location}'
        response = requests.get(url).text
        soup = BeautifulSoup(response, 'html.parser')
        longitude = float(soup.select('.longitude')[1].text.replace(',', '.'))
        latitude = float(soup.select('.latitude')[1].text.replace(',', '.'))
        return [latitude, longitude]
    except Exception:
        return [52.23, 21.0]  # fallback: Warszawa