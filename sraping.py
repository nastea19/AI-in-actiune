import requests
from bs4 import BeautifulSoup
import csv
url = 'https://stiri.md/'
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful
soup = BeautifulSoup(response.text, 'html.parser')  # Parse the page content using BeautifulSoup

# Find all article links
article_tags = soup.find_all('a', href=lambda href: href and '/article/' in href)
articles_data = []

for article in article_tags:
    # Get the title
    title_tag = article.find('h2')
    if not title_tag:
        title_tag = article.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else ''
    
    # Get the link
    link = article['href']
    full_link = 'https://stiri.md' + link
    
    # Get the summary
    summary_tag = article.find('p')
    summary = summary_tag.get_text(strip=True) if summary_tag else ''
    
    # Get the date
    time_tag = article.find('time')
    date = time_tag.get_text(strip=True) if time_tag else ''
    
    # Get the views
    views = ''
    # Views are typically within a span tag next to an SVG icon
    views_tag = article.find('span', class_=lambda x: x and ('clfmhif' in x or 'chx12dn' in x))
    if views_tag:
        views = views_tag.get_text(strip=True)
    
    # Append the data if the title is not empty to avoid duplicates or empty entries
    if title:
        articles_data.append({
            'Titlu': title,
            'Vizualizari': views,
            'Data publicarii': date,
            'Sursa': full_link,
            'Rezumat': summary
        })

# Remove duplicates by converting the list to a dictionary and back to a list
unique_articles = {article['Sursa']: article for article in articles_data}.values()

# Now write to CSV
with open('stiri_vizualizari.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['Titlu', 'Vizualizari', 'Data publicarii', 'Sursa', 'Rezumat']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for data in unique_articles:
        writer.writerow(data)

print(f'S-au salvat {len(unique_articles)} articole, vizualizările și datele lor în fișierul CSV.')


# if len(articles_data) > 0:
#     articles_data = articles_data[1:]  # Exclude primul articol

# # Eliminăm duplicatele convertind lista într-un dicționar și înapoi într-o listă
# unique_articles = {article['Sursa']: article for article in articles_data}.values()

# # Acum scriem în CSV
# with open('stiri_vizualizari.csv', mode='w', newline='', encoding='utf-8') as file:
#     fieldnames = ['Titlu', 'Vizualizari', 'Data publicarii', 'Sursa', 'Rezumat', 'Referinte']
#     writer = csv.DictWriter(file, fieldnames=fieldnames)
#     writer.writeheader()
#     for data in unique_articles:
#         writer.writerow(data)

# print(f'S-au salvat {len(unique_articles)} articole, vizualizările și datele lor în fișierul CSV.')
#Prima versiune de cod!!!!!!!





