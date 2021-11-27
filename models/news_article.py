from project import cursor, db
from datetime import datetime
from models import get_soup
import pandas as pd
import texthero as hero


class NewsArticle:
    CREATE_SQL = '''
        INSERT INTO articles (website_id, url, title, date, text) 
        VALUES(?,?,?,?,?)
    '''

    WEBSITES_TO_CLEAN_QUERY = '''
        SELECT id, title, text
        FROM ARTICLES
        WHERE clean_title IS NULL
            OR clean_text IS NULL
    '''

    def __init__(self, rss_article, entry_element, entry_class, entry_id, website_id):
        self.website_id = website_id
        self.title = rss_article.title.get_text(strip=True)
        self.url = self.find_url(rss_article)
        self.text = self.scrape_article_text(entry_element, entry_class, entry_id)
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.clean_title = None
        self.clean_text = None


    def find_url(self, rss_article):
        if self.website_id == 'cbc':
            found_url = rss_article.link.next_sibling
        else: 
            found_url = rss_article.guid
        return found_url.get_text(strip=True)


    def scrape_article_text(self, entry_element, entry_class, entry_id):
        soup = get_soup(self.url)
        if entry_id != '':
            article_body = soup.find(entry_element, id=entry_id)
        else:
            article_body = soup.find(entry_element, class_=entry_class)

        text_raw = article_body.get_text() if article_body else ''

        return text_raw


    def create_one(self):
        if self.text == '':
            return
        values = (self.website_id, self.url, self.title, self.date, self.text)
        cursor.execute(NewsArticle.CREATE_SQL, values)
        db.commit()


    @staticmethod
    def get_unclean_articles():
        return pd.read_sql_query(NewsArticle.WEBSITES_TO_CLEAN_QUERY, db)


    @staticmethod
    def clean_articles(df):
        df['clean_title'] = (
            df['title']
                .pipe(hero.clean)
                .apply(NewsArticle.remove_non_letters) 
        )
        df['clean_text'] = (
            df['text']
                .pipe(hero.clean)
                .apply(NewsArticle.remove_non_letters) 
        )
        return df


    @staticmethod
    def remove_non_letters(text):
        return ' '.join(
            text.replace("'", '')
                .replace('"', '')
                .replace('-', '')
                .replace('.', '')
                .split()
            )
    
    
    @staticmethod
    def save_cleaned_articles(cleaned_df):
        for _, row in cleaned_df.iterrows():
            update_sql = 'UPDATE articles SET clean_title = ?, clean_text = ? WHERE id = ?'
            cursor.execute(update_sql, (row['clean_title'], row['clean_text'], row['id']))
        db.commit()