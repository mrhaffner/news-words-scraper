import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sqlite3


def get_soup(url):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, 'html.parser')


def scrape_article(url, tag, entry_class, entry_id):
    soup = get_soup(url)

    if entry_id is not None:
        article = soup.find(tag, id=entry_id)
    else:
        article = soup.find(tag, class_=entry_class)
    return article.get_text() if article else ''


def scrape_rss_feed(url, tag, entry_class, entry_id):
    soup = get_soup(url)
    articles = soup.find_all('item')
    articles_data = []

    for article in articles:
        article_data = {}
        article_data['title'] = article.title.get_text(strip=True)
        article_url = article.guid.get_text(strip=True)
        article_data['url'] = article_url
        article_data['body'] = scrape_article(article_url, tag, entry_class, entry_id)
        article_data['date_collected'] = datetime.today().strftime('%Y-%m-%d')

        articles_data.append(article_data)
        # break
        time.sleep(1)
    
    return articles_data


con = sqlite3.connect('website_data.sqlite3')
cur = con.cursor()

websites_query = 'SELECT id, rss_url, article_entry_element, article_entry_class, article_entry_id FROM websites'
websites_result = cur.execute(websites_query)

for row in websites_result:
    id, rss_url, article_entry_element, article_entry_class, article_entry_id = row
    articles_data = scrape_rss_feed(rss_url, article_entry_element, article_entry_class, article_entry_id)
    print(articles_data)


con.close()
