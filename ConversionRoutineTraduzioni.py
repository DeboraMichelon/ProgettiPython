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
    return render_template("gui_ConversionRoutines.html")

def apri_browser():
    #time.sleep(3)  # Attendi che il server sia avviato
    webbrowser.get('windows-default').open_new("http://127.0.0.1:5000/")

@app.route('/GenCR', methods=["POST"])
def GenCR():
    # Acquisizione dati dalla gui
    NumJira = request.form.get('NumJira')
    DescJira = request.form.get('DescJira')
    Files = request.files.getlist('files')
    TipoCR = request.form.get('routine')
    numFiles = len(Files) if Files and Files[0].filename else 0

     # Controllo dati mancanti
    errorMSG = None
    if (not NumJira or not DescJira or not TipoCR or numFiles == 0):
        errorMSG = "Attenzione: compilare tutti i campi e caricare almeno un file XML."
        return render_template("gui_ConversionRoutines.html", errorMSG=errorMSG)
    
    # Creazione della conversion routine
    Conversion = ''
    Classe = ''
    if (NumJira and DescJira and TipoCR and numFiles):
        Conversion = 'Include Region.ITXX.Main'
        if (TipoCR == 'Automatica'):
            Classe = 'Region.ITXX.Convert.'
        elif (TipoCR == 'Manuale'):
            Classe = 'Region.ITXX.Conversions.'
        Classe += NumJira.replace('-','') 
        Conversion += '\nClass ' + Classe + ' Extends websys.DataConversion.Abstract'
        Conversion += '\n{'
        Conversion += '\nParameter DESCRIPTION = "' + (NumJira + ': ' + DescJira) +'";'
        Conversion += '\nParameter MULTIPROCESS = 0;'
        Conversion += '\nClassMethod Main() As %Status'
        Conversion += '\n{'
        Conversion += '\n   /// This conversion routine will XML load a translation type forcibly due to once only nature of the code table'
        Conversion += '\n   set sc=$$$OK'
        
        fileContent= []
        for file_storage in Files:
            # Leggi il contenuto dell'XML come stringa
            xml_content = file_storage.read().decode('utf-8')
            guid = None
            # Estrai il contenuto di un tag specifico
            try:
                root = ET.fromstring(xml_content)
                # Cerca TranslationType
                elem = root.find('.//websys.TranslationType')
                if elem is not None and 'GUID' in elem.attrib:
                    guid = elem.attrib['GUID']
                 # Cerca DictionaryTranslated solo se non già trovato
                if guid is None:
                    elem = root.find('.//websys.DictionaryTranslated')
                    if elem is not None and 'GUID' in elem.attrib:
                        guid = elem.attrib['GUID']
                # Cerca TranslationEPR solo se non già trovato
                if guid is None:
                    elem = root.find('.//websys.TranslationEPR')
                    if elem is not None and 'GUID' in elem.attrib:
                        guid = elem.attrib['GUID']
            except Exception as e:
                guid = None
            fileContent.append({'GUID': guid, 'contenuto':xml_content})
        
        for guidNum, file_info in enumerate(fileContent, start=1):
            guid = file_info['GUID']
            Conversion += '\n   set sc=$$$ADDSC(sc,$$$LoadStreamXData($CLASSNAME(), "Translation' + str(guidNum) + '", "' + guid + '"))'

        Conversion += '\n   quit sc'
        Conversion += '\n}'
    
        for guidNum, file_info in enumerate(fileContent, start=1):
            Conversion += '\n\n XData Translation' + str(guidNum)
            Conversion += '\n{'
            Conversion += '\n   ' + file_info['contenuto']
            Conversion += '\n}'

        Conversion += '\n}'
    
    #print(Conversion)
    nomeFile = Classe + '.txt'
    file_path = os.path.join(tmp_folder, nomeFile)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(Conversion)

#Output della funzione da mostrare nella gui
    return render_template("gui_ConversionRoutines.html", 
        nomeFile=nomeFile,
        download_ready=True,
        download_url=f"/download/{nomeFile}",
        NumJira=NumJira,
        DescJira=DescJira,
        numFiles=numFiles,
        TipoCR=TipoCR)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(tmp_folder, filename, as_attachment=True)

'''
#Outpput della funzione da salvare in un txt
    filename = f"{nomeFile}"
    buffer = io.BytesIO()
    buffer.write(Conversion.encode('utf-8'))
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='text/plain'
    )
'''

if __name__ == '__main__':
    threading.Thread(target=apri_browser).start()
    app.run()

# d $System.OBJ.Load(dir,'c')