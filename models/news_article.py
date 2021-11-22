from project import cursor
from datetime import datetime
from models import get_soup


class NewsArticle:
    SAVE_SQL = '''
        INSERT INTO articles (website_id, url, title, date, text) 
        VALUES(?,?,?,?,?) '''
    #get id from database set to highest? increment from there? or use uuid?
    #sqlite have an option?
    def __init__(self, rss_article, entry_element, entry_class, entry_id, website_id):
        self.website_id = website_id
        self.title = rss_article.title.get_text(strip=True)
        self.url = self.find_url(rss_article)
        self.text = self.scrape_article(entry_element, entry_class, entry_id)
        self.date = datetime.today().strftime('%Y-%m-%d')

    def find_url(self, rss_article):
        if self.website_id == 'cbc':
            found_url = rss_article.link.next_sibling
        else: 
            found_url = rss_article.guid
        return found_url.get_text(strip=True)

    def scrape_article(self, entry_element, entry_class, entry_id):
        soup = get_soup(self.url)

        if entry_id is not None:
            article_body = soup.find(entry_element, id=entry_id)
        else:
            article_body = soup.find(entry_element, class_=entry_class)

        text_raw = article_body.get_text() if article_body else ''

        return ' '.join(text_raw.split())


    def save(self):
        print(self.title)
        print(self.url)
        print(self.text)
        print(self.date)
        print(self.website_id)
        values = (self.website_id, self.url, self.title, self.date, self.text)
        cursor.execute(NewsArticle.SAVE_SQL, values)
        #probably save to db here