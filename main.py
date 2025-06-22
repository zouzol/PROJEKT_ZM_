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



class TerenZalewowy:
    def __init__(self, nazwa, lokalizacja, opis):
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.opis = opis
        self.coords = get_coordinates(lokalizacja)
        self.marker = None

class PunktMonitoringu:
    def __init__(self, nazwa, teren, lokalizacja):
        self.nazwa = nazwa
        self.teren = teren
        self.lokalizacja = lokalizacja
        self.coords = get_coordinates(lokalizacja)
        self.marker = None


class Pracownik:
    def __init__(self, imie, nazwisko, punkt, lokalizacja):
        self.imie = imie
        self.nazwisko = nazwisko
        self.punkt = punkt
        self.lokalizacja = lokalizacja
        self.coords = get_coordinates(lokalizacja)
        self.marker = None