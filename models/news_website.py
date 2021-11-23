from models.news_article import NewsArticle
from models.news_word import NewsWord
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
        return [NewsWebsite(*website_info) for website_info in websites_results]


    def scrape_rss_feed(self):
        soup = get_soup(self.rss_url)
        rss_articles = soup.find_all('item')
        for rss_article in rss_articles:
            new_article = NewsArticle(rss_article, self.article_entry_element, self.article_entry_class, self.article_entry_id, self.id)
            new_article.create_one()
            #is this the best place for this?
            NewsWord.parse_news_article(new_article)
            time.sleep(1)


    @staticmethod
    def scrape_all():
        websites = NewsWebsite.get_all()

        for website in websites:
            website.scrape_rss_feed()