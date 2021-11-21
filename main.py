import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import sqlite3
import pandas as pd


def get_soup(url):
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, 'html.parser')


def parse_article(url, tag, entry_class, entry_id):
    soup = get_soup(url)

    if entry_id is not None:
        article = soup.find(tag, id=entry_id)
    else:
        article = soup.find(tag, class_=entry_class)
    return article.get_text() if article else ''


def parse_rss_feed(url, tag, entry_class, entry_id):
    soup = get_soup(url)
    articles = soup.find_all('item')
    articles_data = []

    for article in articles:
        article_data = {}
        article_data['title'] = article.title.get_text(strip=True)
        article_url = article.guid.get_text(strip=True)
        article_data['url'] = article_url
        article_data['body'] = parse_article(article_url, tag, entry_class, entry_id)
        article_data['date_collected'] = datetime.today().strftime('%Y-%m-%d')

        articles_data.append(article_data)
        # break
        time.sleep(1)
    
    return articles_data


con = sqlite3.connect('website_data.sqlite3')
cur = con.cursor()

# for row in cur.execute('SELECT id FROM websites'):
#     print(row[0])
query = 'SELECT id, rss_url, article_entry_element, article_entry_class, article_entry_id FROM websites'
SQL_Query = pd.read_sql_query(query, con, index_col=['id'])

df_columns = ['rss_url', 'article_entry_element', 'article_entry_class', 'article_entry_id']
df = pd.DataFrame(SQL_Query, columns=df_columns)

#iterate over websites
for website, row in df.iterrows():
    rss_url = row['rss_url']
    tag = row['article_entry_element']
    entry_class = row['article_entry_class']
    entry_id = row['article_entry_id']
    articles_data = parse_rss_feed(rss_url, tag, entry_class, entry_id)
    print(articles_data)
#do something with article_data

con.close()
