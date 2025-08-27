import qrcode
import os

# URL da aprire
urls = [
    "https://maps.app.goo.gl/cLMQRg3vQPeFsbZ46", #Day1, ItinerarioA
    "https://maps.app.goo.gl/ZX2mEnfbT1VDUNg18"  #Day1, ItinerarioB
]

# Definizione del path dove salvare i qrcodes generati
folder = r"C:\Users\dmichelo\OneDrive - InterSystems Corporation\Desktop\ProgettiPython\ProgettiPython\QRCodes"

# Generazione QR e Salvataggio come immagine
for i, url in enumerate(urls, start=1):
    filename = f"qrcode_{i}.png"
    path = os.path.join(folder, filename)
    
    qr = qrcode.make(url)
    qr.save(path)