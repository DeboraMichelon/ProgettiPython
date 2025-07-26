import random
from datetime import datetime
import math
import webbrowser
import os

# Percorso della GUI in HTML e apertura nel browser predefinito
gui_path = os.path.abspath("gui.html")
webbrowser.open(f"file://{gui_path}")

def NumImpegnativa():
    subregion = input("Per quale subregion vuoi generare un numero impegnativa? ")
    year = str(datetime.now().year)
    codRegione = {
        "VEN" : "050",
        "LAZ" : "120",
        "PIE" : "010",
        "VDA" : "020"
    }.get(subregion)
    cifre = ""
    somma = 0
    for i in range(9):
        a = random.randint(0, 9)
        cifre += str(a)
        somma += a
    modulo = str(somma % 9)
    numeroImpegnativa = codRegione + year[-2:] + cifre + modulo
    print("Ecco qui una ricetta rossa per la subregion " + subregion + ": " + numeroImpegnativa)

NumImpegnativa()