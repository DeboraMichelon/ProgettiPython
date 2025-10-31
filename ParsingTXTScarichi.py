from flask import Flask, request, render_template, send_from_directory
import os
import threading
import webbrowser
import time
import xml.etree.ElementTree as ET

app = Flask(__name__)

base_dir = os.path.dirname(os.path.abspath(__file__))
tmp_folder = os.path.join(base_dir, "tmp")
os.makedirs(tmp_folder, exist_ok=True)

@app.route('/')
def my_form():
    return render_template("gui_ParsingTXTScarichi.html")

def apri_browser():
    #time.sleep(3)  # Attendi che il server sia avviato
    webbrowser.get('windows-default').open_new("http://127.0.0.1:5000/")

def assegnaEtichetta(filename: str, scarico: str) -> str:
    nome_maiuscolo = filename.upper()  # normalizza per sicurezza
    if scarico == "APS_Veneto":
        if "ACC" in nome_maiuscolo:
            return "ACC"
        elif "ANA" in nome_maiuscolo:
            return "ANA"
        elif "PRE" in nome_maiuscolo:
            return "PRE"
        else:
            return "Sconosciuto"
    else:
        return "Sconosciuto"

@app.route('/Parse', methods=["POST"])
def Parse():
    # Acquisizione dati dalla gui
    Scarico = request.form.get('scarico')
    Files = request.files.getlist('files')
    file_info = []
    numFiles = len(Files) if Files and Files[0].filename else 0

     # Controllo dati mancanti
    errorMSG = None
    if (not Scarico or numFiles == 0):
        errorMSG = "Attenzione: compilare tutti i campi e caricare almeno un file TXT."
        return render_template("gui_ParsingTXTScarichi.html", errorMSG=errorMSG)
    
    # Leggo il nome di ciascun file e gli attribuisco un'etichetta
    for file in Files:
        filename = file.filename
        label = assegnaEtichetta(filename, Scarico)
        file_info.append({"nome": filename, "etichetta": label})

    #Output della funzione da mostrare nella gui
    return render_template("gui_ParsingTXTScarichi.html", 
        Scarico=Scarico,
        numFiles=numFiles,
        #download_ready=True,
        #download_url=f"/download/{nomeFile}",
        file_info=file_info)
        
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(tmp_folder, filename, as_attachment=True)

if __name__ == '__main__':
    threading.Thread(target=apri_browser).start()
    app.run()