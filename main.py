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

# ======= Listy danych ==========
tereny = []
punkty = []
pracownicy = []

root = tk.Tk()
root.title("System zarządzania terenami zalewowymi i punktami monitoringu")
root.geometry('1400x800')

notebook = ttk.Notebook(root)
frame_teren = Frame(notebook)
frame_punkt = Frame(notebook)
frame_pracownik = Frame(notebook)
notebook.add(frame_teren, text="Tereny zalewowe")
notebook.add(frame_punkt, text="Punkty monitoringu")
notebook.add(frame_pracownik, text="Pracownicy")
notebook.pack(expand=1, fill='both')

# --- MAPA ---
frame_mapa = Frame(root)
frame_mapa.pack(fill='both', expand=1)
map_widget = tkintermapview.TkinterMapView(frame_mapa, width=1300, height=400)
map_widget.pack()
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

# ======= FUNKCJE MARKERY =======
def odswiez_markery():
    for t in tereny:
        if t.marker:
            t.marker.delete()
            t.marker = None
    for p in punkty:
        if p.marker:
            p.marker.delete()
            p.marker = None
    for w in pracownicy:
        if w.marker:
            w.marker.delete()
            w.marker = None
    for t in tereny:
        t.marker = map_widget.set_marker(t.coords[0], t.coords[1], text=f"Teren: {t.nazwa}\n{t.opis}")
    for p in punkty:
        p.marker = map_widget.set_marker(p.coords[0], p.coords[1], text=f"Punkt: {p.nazwa}\nTeren: {p.teren}")
    for w in pracownicy:
        w.marker = map_widget.set_marker(w.coords[0], w.coords[1], text=f"Pracownik: {w.imie} {w.nazwisko}\nPunkt: {w.punkt}")

        # =================== TERENY ZALEWOWE ===================
        # Kolumny w zakładce
        frame_teren_form = Frame(frame_teren)
        frame_teren_form.grid(row=0, column=0, padx=30, pady=10, sticky="n")
        frame_teren_lista = Frame(frame_teren)
        frame_teren_lista.grid(row=0, column=1, padx=30, pady=10, sticky="n")

Label(frame_teren_form, text="Nazwa terenu:").grid(row=0, column=0, sticky="w")
entry_nazwa_terenu = Entry(frame_teren_form)
entry_nazwa_terenu.grid(row=1, column=0)
Label(frame_teren_form, text="Lokalizacja (np. Warszawa):").grid(row=2, column=0, sticky="w")
entry_lokalizacja_terenu = Entry(frame_teren_form)
entry_lokalizacja_terenu.grid(row=3, column=0)
Label(frame_teren_form, text="Opis:").grid(row=4, column=0, sticky="w")
entry_opis_terenu = Entry(frame_teren_form)
entry_opis_terenu.grid(row=5, column=0)
button_dodaj_teren = Button(frame_teren_form, text="Dodaj teren", command=lambda: dodaj_teren())
button_dodaj_teren.grid(row=6, column=0, pady=5)

listbox_tereny = Listbox(frame_teren_lista, width=45)
listbox_tereny.grid(row=0, column=0, columnspan=3)
Button(frame_teren_lista, text="Edytuj", command=lambda: edytuj_teren()).grid(row=1, column=0, pady=5)
Button(frame_teren_lista, text="Usuń", command=lambda: usun_teren()).grid(row=1, column=1, pady=5)
Button(frame_teren_lista, text="Pokaż szczegóły", command=lambda: pokaz_szczegoly_terenu()).grid(row=1, column=2, pady=5)
label_szczegoly_teren = Label(frame_teren_lista, text="", justify=LEFT)
label_szczegoly_teren.grid(row=2, column=0, columnspan=3, sticky="w")

def dodaj_teren():
    nazwa = entry_nazwa_terenu.get()
    lokalizacja = entry_lokalizacja_terenu.get()
    opis = entry_opis_terenu.get()
    if not nazwa or not lokalizacja:
        messagebox.showerror("Błąd", "Uzupełnij nazwę i lokalizację!")
        return
    teren = TerenZalewowy(nazwa, lokalizacja, opis)
    tereny.append(teren)
    odswiez_tereny()
    odswiez_markery()
    entry_nazwa_terenu.delete(0, END)
    entry_lokalizacja_terenu.delete(0, END)
    entry_opis_terenu.delete(0, END)

def edytuj_teren():
    idx = listbox_tereny.curselection()
    if not idx: return
    idx = idx[0]
    teren = tereny[idx]
    entry_nazwa_terenu.delete(0, END)
    entry_lokalizacja_terenu.delete(0, END)
    entry_opis_terenu.delete(0, END)
    entry_nazwa_terenu.insert(0, teren.nazwa)
    entry_lokalizacja_terenu.insert(0, teren.lokalizacja)
    entry_opis_terenu.insert(0, teren.opis)
    button_dodaj_teren.config(text="Zapisz", command=lambda: zapisz_teren(idx))

def zapisz_teren(idx):
    nazwa = entry_nazwa_terenu.get()
    lokalizacja = entry_lokalizacja_terenu.get()
    opis = entry_opis_terenu.get()
    tereny[idx] = TerenZalewowy(nazwa, lokalizacja, opis)
    odswiez_tereny()
    odswiez_markery()
    button_dodaj_teren.config(text="Dodaj teren", command=dodaj_teren)
    entry_nazwa_terenu.delete(0, END)
    entry_lokalizacja_terenu.delete(0, END)
    entry_opis_terenu.delete(0, END)

def usun_teren():
    idx = listbox_tereny.curselection()
    if not idx: return
    idx = idx[0]
    teren = tereny.pop(idx)
    if teren.marker:
        teren.marker.delete()
    odswiez_tereny()
    odswiez_markery()

def odswiez_tereny():
    listbox_tereny.delete(0, END)
    for t in tereny:
        listbox_tereny.insert(END, f"{t.nazwa} ({t.lokalizacja})")
    combobox_teren_punkt['values'] = [t.nazwa for t in tereny]

def pokaz_szczegoly_terenu():
    idx = listbox_tereny.curselection()
    if not idx:
        label_szczegoly_teren.config(text="Brak wybranego terenu.")
        return
    teren = tereny[idx[0]]
    label_szczegoly_teren.config(
        text=f"Nazwa: {teren.nazwa}\nLokalizacja: {teren.lokalizacja}\nOpis: {teren.opis}\nWspółrzędne: {teren.coords}"
    )
    map_widget.set_position(teren.coords[0], teren.coords[1])
    map_widget.set_zoom(12)

# =================== PUNKTY MONITORINGU ===================
frame_punkt_form = Frame(frame_punkt)
frame_punkt_form.grid(row=0, column=0, padx=30, pady=10, sticky="n")
frame_punkt_lista = Frame(frame_punkt)
frame_punkt_lista.grid(row=0, column=1, padx=30, pady=10, sticky="n")

Label(frame_punkt_form, text="Nazwa punktu:").grid(row=0, column=0, sticky="w")
entry_nazwa_punktu = Entry(frame_punkt_form)
entry_nazwa_punktu.grid(row=1, column=0)
Label(frame_punkt_form, text="Lokalizacja punktu:").grid(row=2, column=0, sticky="w")
entry_lokalizacja_punktu = Entry(frame_punkt_form)
entry_lokalizacja_punktu.grid(row=3, column=0)
Label(frame_punkt_form, text="Teren zalewowy:").grid(row=4, column=0, sticky="w")
combobox_teren_punkt = ttk.Combobox(frame_punkt_form, state="readonly")
combobox_teren_punkt.grid(row=5, column=0)
button_dodaj_punkt = Button(frame_punkt_form, text="Dodaj punkt", command=lambda: dodaj_punkt())
button_dodaj_punkt.grid(row=6, column=0, pady=5)

listbox_punkty = Listbox(frame_punkt_lista, width=45)
listbox_punkty.grid(row=0, column=0, columnspan=3)
Button(frame_punkt_lista, text="Edytuj", command=lambda: edytuj_punkt()).grid(row=1, column=0, pady=5)
Button(frame_punkt_lista, text="Usuń", command=lambda: usun_punkt()).grid(row=1, column=1, pady=5)
Button(frame_punkt_lista, text="Pokaż szczegóły", command=lambda: pokaz_szczegoly_punktu()).grid(row=1, column=2, pady=5)
label_szczegoly_punkt = Label(frame_punkt_lista, text="", justify=LEFT)
label_szczegoly_punkt.grid(row=2, column=0, columnspan=3, sticky="w")

def dodaj_punkt():
    nazwa = entry_nazwa_punktu.get()
    lokalizacja = entry_lokalizacja_punktu.get()
    teren_idx = combobox_teren_punkt.current()
    if not nazwa or not lokalizacja or teren_idx == -1:
        messagebox.showerror("Błąd", "Uzupełnij nazwę, lokalizację i wybierz teren!")
        return
    teren = tereny[teren_idx]
    punkt = PunktMonitoringu(nazwa, teren.nazwa, lokalizacja)
    punkty.append(punkt)
    odswiez_punkty()
    odswiez_markery()
    entry_nazwa_punktu.delete(0, END)
    entry_lokalizacja_punktu.delete(0, END)

def edytuj_punkt():
    idx = listbox_punkty.curselection()
    if not idx: return
    idx = idx[0]
    punkt = punkty[idx]
    entry_nazwa_punktu.delete(0, END)
    entry_lokalizacja_punktu.delete(0, END)
    entry_nazwa_punktu.insert(0, punkt.nazwa)
    entry_lokalizacja_punktu.insert(0, punkt.lokalizacja)
    combobox_teren_punkt.set(punkt.teren)
    button_dodaj_punkt.config(text="Zapisz", command=lambda: zapisz_punkt(idx))

def zapisz_punkt(idx):
    nazwa = entry_nazwa_punktu.get()
    lokalizacja = entry_lokalizacja_punktu.get()
    teren_idx = combobox_teren_punkt.current()
    if teren_idx == -1: return
    teren = tereny[teren_idx]
    punkty[idx] = PunktMonitoringu(nazwa, teren.nazwa, lokalizacja)
    odswiez_punkty()
    odswiez_markery()
    button_dodaj_punkt.config(text="Dodaj punkt", command=dodaj_punkt)
    entry_nazwa_punktu.delete(0, END)
    entry_lokalizacja_punktu.delete(0, END)

def usun_punkt():
    idx = listbox_punkty.curselection()
    if not idx: return
    idx = idx[0]
    punkt = punkty.pop(idx)
    if punkt.marker:
        punkt.marker.delete()
    odswiez_punkty()
    odswiez_markery()

def odswiez_punkty():
    listbox_punkty.delete(0, END)
    combobox_teren_punkt['values'] = [t.nazwa for t in tereny]
    combobox_punkt_pracownik['values'] = [p.nazwa for p in punkty]
    for p in punkty:
        listbox_punkty.insert(END, f"{p.nazwa} ({p.lokalizacja}) | Teren: {p.teren}")

def pokaz_szczegoly_punktu():
    idx = listbox_punkty.curselection()
    if not idx:
        label_szczegoly_punkt.config(text="Brak wybranego punktu.")
        return
    punkt = punkty[idx[0]]
    label_szczegoly_punkt.config(
        text=f"Nazwa: {punkt.nazwa}\nLokalizacja: {punkt.lokalizacja}\nTeren: {punkt.teren}\nWspółrzędne: {punkt.coords}"
    )
    map_widget.set_position(punkt.coords[0], punkt.coords[1])
    map_widget.set_zoom(12)

# =================== PRACOWNICY ===================
frame_prac_form = Frame(frame_pracownik)
frame_prac_form.grid(row=0, column=0, padx=30, pady=10, sticky="n")
frame_prac_lista = Frame(frame_pracownik)
frame_prac_lista.grid(row=0, column=1, padx=30, pady=10, sticky="n")

Label(frame_prac_form, text="Imię:").grid(row=0, column=0, sticky="w")
entry_imie = Entry(frame_prac_form)
entry_imie.grid(row=1, column=0)
Label(frame_prac_form, text="Nazwisko:").grid(row=2, column=0, sticky="w")
entry_nazwisko = Entry(frame_prac_form)
entry_nazwisko.grid(row=3, column=0)
Label(frame_prac_form, text="Lokalizacja:").grid(row=4, column=0, sticky="w")
entry_lokalizacja_pracownika = Entry(frame_prac_form)
entry_lokalizacja_pracownika.grid(row=5, column=0)
Label(frame_prac_form, text="Punkt monitoringu:").grid(row=6, column=0, sticky="w")
combobox_punkt_pracownik = ttk.Combobox(frame_prac_form, state="readonly")
combobox_punkt_pracownik.grid(row=7, column=0)
button_dodaj_pracownika = Button(frame_prac_form, text="Dodaj pracownika", command=lambda: dodaj_pracownika())
button_dodaj_pracownika.grid(row=8, column=0, pady=5)

listbox_pracownicy = Listbox(frame_prac_lista, width=45)
listbox_pracownicy.grid(row=0, column=0, columnspan=3)
Button(frame_prac_lista, text="Edytuj", command=lambda: edytuj_pracownika()).grid(row=1, column=0, pady=5)
Button(frame_prac_lista, text="Usuń", command=lambda: usun_pracownika()).grid(row=1, column=1, pady=5)
Button(frame_prac_lista, text="Pokaż szczegóły", command=lambda: pokaz_szczegoly_pracownika()).grid(row=1, column=2, pady=5)
label_szczegoly_pracownik = Label(frame_prac_lista, text="", justify=LEFT)
label_szczegoly_pracownik.grid(row=2, column=0, columnspan=3, sticky="w")
