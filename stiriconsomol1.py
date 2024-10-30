import scrapy
from datetime import datetime

class StiriconsomolSpider(scrapy.Spider):
    name = "stiriconsomol1"
    start_urls = ['https://www.md.kp.media/']

    def parse(self, response):
        # Găsește titlurile articolelor
        titles = response.css('span.sc-17oegr5-0::text').getall()

        # Găsește rezumatele articolelor
        summaries = response.css('a.sc-1tputnk-3::text').getall()

        # Găsește datele publicării
        publish_dates = response.css('time.sc-k5zf9p-10::attr(datetime)').getall()

        # Convertește datele într-un format lizibil
        publish_dates_lizibile = [datetime.fromisoformat(date).strftime('%d-%m-%Y %H:%M:%S') for date in publish_dates]

        # Găsește URL-urile articolelor
        urls = response.css('a.sc-1tputnk-2::attr(href)').getall()

        # Creează un dict pentru fiecare articol
        for title, summary, publish_date, url in zip(titles, summaries, publish_dates_lizibile, urls):
            yield {
                'Titlu': title,
                'Rezumat': summary,
                'Data Publicării': publish_date,
                'URL': url
            }
