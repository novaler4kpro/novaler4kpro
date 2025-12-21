import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import os

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
        if href.startswith('http'):
            full_url = href
        else:
            full_url = "https://www.novaler.com" + href if href.startswith('/') else "https://www.novaler.com/uploads/" + href
        filename = os.path.basename(full_url.split('?')[0])  # Nettoie au cas où
        zip_links.append((filename, full_url))

# Fonction pour extraire la date du filename (cherche 8 chiffres consécutifs YYYYMMDD)
def extract_date_sort_key(filename):
    match = re.search(r'(\d{8})', filename)
    if match:
        date_str = match.group(1)
        try:
            # Retourne un objet datetime pour un tri précis (plus récent d'abord)
            return datetime.strptime(date_str, '%Y%m%d')
        except ValueError:
            pass
    # Si pas de date trouvée, on met très ancien pour qu'il aille à la fin
    return datetime(2000, 1, 1)

# Trie par date descendante (plus récent en haut)
zip_links.sort(key=lambda x: extract_date_sort_key(x[0]), reverse=True)

# Génère le nom humain comme dans ton exemple
def generate_name(filename):
    # Extrait la date pour l'ajouter à la fin au format DDMMYYYY
    date_match = re.search(r'(\d{8})', filename)
    formatted_date = ""
    if date_match:
        date_str = date_match.group(1)
        formatted_date = f"_{date_str[6:]}{date_str[4:6]}{date_str[:4]}"

    # Nettoyage de base du nom
    base = filename.lower().replace('-novaler4kpro-backup-', '').replace('-usb.zip', '').replace('-mmc.zip', '').replace('.zip', '')

    # Mapping précis basé sur les backups actuels du site (au 21/12/2025)
    mapping = {
        'openpli-gcc-15.2': 'Openpli_GCC_15.2',
        'openpli-gcc': 'Openpli_GCC_15.1',  # fallback si version pas précisée
        'openpli-10.1': 'OpenPli_Py3.12',
        'openpli-10': 'OpenPli_Py3.12',
        'openpli-9.1': 'OpenPLi_9.1',
        'openpli-9': 'OpenPLi_9',
        'openpli-develop': 'OpenPLi_py3',
        'openatv-7.6.0': 'OpenATV_7.6.0',
        'openatv-7.6': 'OpenATV_7.6.0',
        'openatv-7.5.1': 'OpenATV_7.5.1',
        'openatv-7.5': 'OpenATV_7.5.1',
        'openatv-7.4': 'OpenATV_7.4',
        'openbh-5.6': 'OpenBH_5.6.001',
        'openbh-5.5.1': 'OpenBlackHole_5.5.1',
        'teamblue-7.6': 'Teamblue_7.6',
        'teamblue': 'Teamblue',
        'openvix-6.8': 'Open_VIX_6.8',
        'openvix-6.7': 'Open_VIX_6.7',
        'gazal_mix': 'GAZAL_MAX',
        'gazal-01': 'Gazal_Linux',
        'define-7.0': 'Define-7.0',
        'densy-os': 'Densy-OS',
        'spider-plus-pro': 'Spider-Plus',
        'sungate-titan': 'Sungate-Titan',
        'egami-11.0.r5': 'Egami_11.0r5',
        'egami-11': 'Egami_11.0r5',
        'egami-10.6.r13': 'Egami_10.6r13',
        'pure2-7.4': 'Pure2_7.4',
        'pure2-7.3': 'Pure2_7.3',
        'openspa-8.5': 'Open_SPA_8.5.001',
        'corvoboys': 'Corvoboys',
        'openhdf-7.5': 'OpenHDF_7.5',
        'satdreamgr-10': 'SatDreamGR_10',
        'nonsolosat-33': 'NonSoloSat_33-py3',
    }

    name = base
    for key, val in mapping.items():
        if key in base:
            name = val
            break

    # Si pas de correspondance, on garde une version propre du nom original
    if name == base:
        name = base.replace('-', '_').replace('.', '_').title()

    return (name + formatted_date).replace('-', '_').upper()

# Écrit le fichier backups.txt
with open('backups.txt', 'w', encoding='utf-8') as f:
    f.write("Novaler4K_UHD_MultiboxPro\n")
    for filename, url in zip_links:
        name = generate_name(filename)
        f.write(f"{name} {url}\n")

print(f"backups.txt mis à jour avec {len(zip_links)} backups, triés par date (plus récent en premier).")
