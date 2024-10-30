import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime#pentru a converti data si ora fara fus orar
import os  # Import corect pentru a verifica existența fișierului

url = 'https://www.md.kp.media/'
response = requests.get(url)
response.raise_for_status() 
soup = BeautifulSoup(response.text, 'html.parser') 

# # Găsește toate titlurile articolelor
article_tags = soup.find_all('span', class_='sc-17oegr5-0')
titles = [tag.get_text().strip() for tag in article_tags]

# # Găsește toate rezumatele articolelor
summary_tags = soup.find_all('a', class_='sc-1tputnk-3')
summaries = [tag.get_text().strip() for tag in summary_tags]

# Găsește toate titlurile articolelor
#article_tags = soup.find_all('div', class_='sc-j7em19-3')
#titles = [tag.get_text().strip() for tag in article_tags]

# Găsește toate rezumatele articolelor
#summary_tags = soup.find_all('div', class_='sc-j7em19-4')
#summaries = [tag.get_text().strip() for tag in summary_tags]

# Găsește toate datele publicării articolelor
time_tags = soup.find_all('time', class_='sc-k5zf9p-10')
publish_dates = [tag['datetime'] for tag in time_tags]

# Convertește datele într-un format mai lizibil
publish_dates_lizibile = [datetime.fromisoformat(date).strftime('%d-%m-%Y %H:%M:%S') for date in publish_dates]

# Găsește toate URL-urile articolelor (elementele <a> cu clasa 'sc-1tputnk-2')
url_tags = soup.find_all('a', class_='sc-1tputnk-2')
urls = [tag['href'] for tag in url_tags]  # Extrage atributul href care conține URL-ul

# Numele fișierului CSV
csv_file = 'stiri_consomol.csv'

# Verifică dacă fișierul CSV există deja
existing_urls = set()

if os.path.exists(csv_file):
#     # Deschide fișierul CSV și citește URL-urile existente
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Sari peste antet
        for row in reader:
            if row:  # Dacă rândul nu e gol
                existing_urls.add(row[3])  # Adaugă URL-ul existent (a patra coloană)

# Deschide fișierul CSV în modul append (adaugă)
with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if file.tell() == 0:  # Verifică dacă fișierul este gol
        writer.writerow(['Titlu', 'Rezumat', 'Data Publicării', 'URL'])
    # Scrie doar articolele noi (care nu au URL-ul deja în fișier)
    for title, summary, publish_date, url in zip(titles, summaries, publish_dates_lizibile, urls):
        if url not in existing_urls:
            writer.writerow([title, summary, publish_date, url])

print(f"Știrile noi au fost adăugate în {csv_file}.")