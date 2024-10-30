import csv
import requests
from bs4 import BeautifulSoup

# Numele fișierelor CSV
input_file = "Coloana_SURSA.csv"  # Fișierul CSV cu URL-uri
output_file = "data_extrase2.csv"  # Fișierul CSV pentru salvarea datelor extrase

# Funcția de extragere a datelor dintr-un URL
def extract_data_from_url(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url  # Adăugăm schema dacă lipsește

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Exemplu de extragere a datelor - poți personaliza în funcție de structura paginilor web
        date_info = soup.find('time').get_text()  # De exemplu, datele pot fi într-un tag 'data'

        return date_info
    except Exception as e:
        print(f"Eroare la accesarea {url}: {e}")
        return "N/A"

# Citirea URL-urilor din fișierul CSV și scrierea datelor extrase într-un nou fișier CSV
with open(input_file, newline='', encoding="utf-8") as csvfile:
    url_reader = csv.reader(csvfile)
    with open(output_file, 'w', newline='', encoding="utf-8") as csvfile_output:
        fieldnames = ["URL", "Data Extrase"]
        writer = csv.DictWriter(csvfile_output, fieldnames=fieldnames)
        writer.writeheader()

        for row in url_reader:
            url = row[0].strip()  # Eliminăm spațiile suplimentare
            data_extracted = extract_data_from_url(url)
            writer.writerow({"URL": url, "Data Extrase": data_extracted})

print("Extragerea datelor este finalizată și salvată în data_extrase.csv.")
