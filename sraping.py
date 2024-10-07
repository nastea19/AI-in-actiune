import requests
from bs4 import BeautifulSoup
import csv

# # URL-ul paginii
url = 'https://stiri.md/'
response = requests.get(url)
response.raise_for_status()  # Verifică dacă cererea a avut succes
soup = BeautifulSoup(response.text, 'html.parser')  # Parsează conținutul paginii folosind BeautifulSoup

# # Găsește toate titlurile articolelor de știri (h2 cu clasele respective)
titles = soup.find_all('h2', class_='mocked-styled-158 t181517i')
 # Creez o listă cu titlurile
title_list = [title.get_text(strip=True) for title in titles]

# # Găsește toate elementele care conțin numărul de vizualizări
views = soup.find_all('span', class_='mocked-styled-160')
# # Creez o listă cu vizualizările
view_list = [view.get_text(strip=True) for view in views]

# # Verific dacă numărul de titluri corespunde cu numărul de vizualizări
if len(title_list) == len(view_list):
#     # Scrie titlurile și vizualizările într-un fișier CSV
    with open('stiri_vizualizari.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Titlu', 'Vizualizari'])  # Scrie antetul
        for title, view in zip(title_list, view_list):
           writer.writerow([title, view])  # Scrie titlu și vizualizare pe fiecare rând

    print(f'S-au salvat {len(title_list)} articole și vizualizările lor în fișierul CSV.')
else:
     print('Numărul de titluri nu corespunde cu numărul de vizualizări. Verifică structura paginii.')

