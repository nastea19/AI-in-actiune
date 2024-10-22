import requests
from bs4 import BeautifulSoup
import csv
import time
url = 'https://stiri.md/'
response = requests.get(url)
response.raise_for_status() 
soup = BeautifulSoup(response.text, 'html.parser') 

# gaseste toate articole
article_tags = soup.find_all('a', href=lambda href: href and '/article/' in href)
articles_data = []

# Citeste articolele deja salvate în fisierul CSV
def citeste_articole_csv():
    try:
        with open('stiri_vizualizari1.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return {row['Titlu'] for row in reader}  # Set cu titluri pentru a verifica unicitatea
    except FileNotFoundError:
        return set()  # Daca fisierul nu exista, returneaza un set gol

# Obtine articole noi care nu exista deja in fisier
for article in article_tags:
    title_tag = article.find('h2')
    if not title_tag:
        title_tag = article.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else ''
    link = article['href']
    full_link = 'https://stiri.md' + link if link.startswith('/') else link
    
    # partea cu data publicarii
    time_tag = article.find('time')
    date = time_tag.get_text(strip=True) if time_tag else ''
    
    # pentru vizualizari ca sa le extrag
    views = ''
    views_tag = article.find('span', class_=lambda x: x and ('clfmhif' in x or 'chx12dn' in x))
    if views_tag:
        views = views_tag.get_text(strip=True)
    if title and link:
        try:
            article_response = requests.get(full_link)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.text, 'html.parser')
            
            #partea cu rezumat
            content_div=article_soup.find('p')
            summary = ''
            if content_div:
             summary = content_div.get_text(strip=True)

            print(f"Summary: {summary}")
            # extrag referintele
            references = []
            content_div = article_soup.find('div', class_=lambda x: x and ('article-content' in x or x.startswith('mocked-styled')))
            if content_div:
                a_tags = content_div.find_all('a', href=True)
                for a in a_tags:
                    href = a['href']
                    if 'stiri.md' not in href and href.startswith('http'):
                        references.append(href)
                references = ', '.join(references)
            
            articles_data.append({
                'Titlu': title,
                'Vizualizari': views,
                'Data publicarii': date,
                'Sursa': full_link,
                'Rezumat':summary,
                'Referinte': references
                
            })
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching article {full_link}: {e}")
            continue

# Elimin duplicatele prin conversia listei intr-un dictionar si inapoi la o lista
unique_articles = {article['Sursa']: article for article in articles_data}.values()
articole_existent = citeste_articole_csv()
# Filtreaza articolele noi care nu sunt deja in fisier
articole_noi = [data for data in unique_articles if data['Titlu'] not in articole_existent]

# Daca exista articole noi le aduga in fisier
if articole_noi:
    with open('stiri_vizualizari1.csv', mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['Titlu', 'Vizualizari', 'Data publicarii', 'Sursa', 'Referinte','Rezumat']  
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Dacă fisierul este gol, scrie header-ul
        if file.tell() == 0:
            writer.writeheader()
        
        # Scrie articolele noi in fisier
        for data in articole_noi:
            writer.writerow(data)
    
    print(f'S-au adaugat {len(articole_noi)} articole noi in fisierul CSV.')
else:
    print('Nu sunt articole noi de adaugat.')
