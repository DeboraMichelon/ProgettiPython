import qrcode
import os

# URL da aprire
urls = [
    "https://www.amazon.it/gp/r.html?C=1I2QPH0S94DBO&M=urn:rtn:msg:2025122215291876e1baae5289411d9b9fc46d5cd0p0eu&R=2JWQWDSI3W3KQ&T=C&U=https%3A%2F%2Fwww.amazon.it%3Fref_%3Dpe_105482371_1093156431&H=MBVMAYYZFCCTEFSMUMKKB2Q8NBYA&ref_=pe_105482371_1093156431"
]

# Definizione del path dove salvare i qrcodes generati
folder = r"C:\Users\dmichelo\OneDrive - InterSystems Corporation\Desktop\ProgettiPython\ProgettiPython\QRCodes"

# Generazione QR e Salvataggio come immagine
for i, url in enumerate(urls, start=1):
    filename = f"qrcode_{i}.png"
    path = os.path.join(folder, filename)
    
    qr = qrcode.make(url)
    qr.save(path)