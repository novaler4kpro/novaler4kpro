import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

URL = "https://www.novaler.com/downloads/enigma2-backups2/multibox-4k-pro-ultra-hd"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

# Trouve tous les liens .zip
zip_links = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if href.endswith('.zip'):
        full_url = "https://www.novaler.com" + href if href.startswith('/uploads/') else href
        filename = href.split('/')[-1]
        zip_links.append((filename, full_url))

# Trie par date dans le nom de fichier (du plus récent au plus ancien)
def extract_date(filename):
    match = re.search(r'(\d{8})', filename)
    return match.group(1) if match else '00000000'

zip_links.sort(key=lambda x: extract_date(x[0]), reverse=True)

# Génère les noms comme dans l'exemple
def generate_name(filename):
    base = filename.replace('-novaler4kpro-backup-', '').replace('-usb.zip', '').replace('-mmc.zip', '')
    base = base.replace('.zip', '')

    # Mapping simple pour les images connues
    mapping = {
        'openpli-GCC': 'Openpli_GCC',
        'openpli-10': 'OpenPli_Py3.12',  # ou ajuste selon la version
        'openpli-9': 'OpenPLi_9',
        'openpli-develop': 'OpenPLi_py3',
        'openatv-7.6': 'OpenATV_7.6.0',
        'openatv-7.5': 'OpenATV_7.5.1',
        'openatv-7.4': 'OpenATV_7.4',
        'openbh-5.6': 'OpenBH_5.6.001',
        'openbh-5.5': 'OpenBlackHole_5.5.1',
        'teamblue': 'Teamblue',
        'openvix-6.8': 'Open_VIX_6.8',
        'openvix-6.7': 'Open_VIX_6.7',
        'define-7.0': 'Define-7.0',
        'egami-11': 'Egami_11.0r5',
        'egami-10': 'Egami_10.6r13',
        'pure2-7.4': 'Pure2_7.4',
        'pure2-7.3': 'Pure2_7.3',
        'openspa': 'Open_SPA',
        'corvoboys': 'Corvoboys',
        'openhdf': 'OpenHDF',
        'satdreamgr': 'SatDreamGR',
        'nonsolosat': 'NonSoloSat',
        'GAZAL_Mix': 'GAZAL_MAX',
        'Densy-OS': 'Densy-OS',
        'Gazal-01': 'Gazal_Linux',
        'Spider-Plus-Pro': 'Spider-Plus',
        'Sungate-titan': 'Sungate-Titan',
    }

    name = base
    for key, val in mapping.items():
        if key in base:
            name = val
            break

    # Extrait la date et la formate DDMMYYYY
    date_match = re.search(r'(\d{8})', filename)
    if date_match:
        date_str = date_match.group(1)
        formatted_date = f"{date_str[6:]}{date_str[4:6]}{date_str[:4]}"
        name += f"_{formatted_date}"

    return name.replace('.', '_').replace('-', '_').upper()

# Écrit le fichier
with open('backups.txt', 'w', encoding='utf-8') as f:
    f.write("Novaler4K_UHD_MultiboxPro\n")
    for filename, url in zip_links:
        name = generate_name(filename)
        f.write(f"{name} {url}\n")

print("backups.txt mis à jour avec", len(zip_links), "liens.")
