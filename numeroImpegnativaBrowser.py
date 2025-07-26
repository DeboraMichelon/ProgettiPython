import random
from datetime import datetime
import math
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("gui.html")

@app.route('/', methods=["POST"])
def NumImpegnativa():
    codRegione = ""
    subregion = ""
    if request.method == "POST":
        if request.form.get("VEN") == "Veneto":
            codRegione = '050'
            subregion = 'Veneto'
        elif request.form.get("LAZ") == "Lazio":
            codRegione = '120'
            subregion = 'Lazio'
        elif request.form.get("PIE") == "Piemonte":
            codRegione = "010"
            subregion = "Piemonte"
        elif request.form.get("VDA") == "Valle d'Aosta":
            codRegione = "020"
            subregion = "Valle d'Aosta"
    year = str(datetime.now().year)
    cifre = ""
    somma = 0
    for i in range(9):
        a = random.randint(0, 9)
        cifre += str(a)
        somma += a
    modulo = str(somma % 9)
    numeroImpegnativa = codRegione + year[-2:] + cifre + modulo
    return render_template("gui.html", numero=numeroImpegnativa, subregion=subregion)

if __name__ == '__main__':
    app.run()