from models.news_article import NewsArticle
from project import cursor
from models import get_soup
import time


class NewsWebsite:
    WEBSITES_QUERY = '''
        SELECT id, name, rss_url, article_entry_element, article_entry_class, article_entry_id 
        FROM websites
        '''

    def __init__(self, id, name, rss_url, article_entry_element, article_entry_class, article_entry_id):
        self.id = id
        self.name = name
        self.rss_url = rss_url
        self.article_entry_element = article_entry_element
        self.article_entry_class = article_entry_class
        self.article_entry_id = article_entry_id


    @staticmethod
    def get_all():
        websites_results = cursor.execute(NewsWebsite.WEBSITES_QUERY)
        return  [NewsWebsite(*website_info) for website_info in websites_results]

    def scrape_rss_feed(self):
        soup = get_soup(self.rss_url)
        rss_articles = soup.find_all('item')
        for rss_article in rss_articles:
            parsed_article = NewsArticle(rss_article, self.article_entry_element, self.article_entry_class, self.article_entry_id, self.id)
            parsed_article.save()
            time.sleep(1)
