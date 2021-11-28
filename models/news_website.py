from models.news_article import NewsArticle
from project import cursor
from models import get_soup
import time


class NewsWebsite:
    def __init__(self, id, name, rss_url, article_entry_element, article_entry_class, article_entry_id):
        self.id = id
        self.name = name
        self.rss_url = rss_url
        self.article_entry_element = article_entry_element
        self.article_entry_class = article_entry_class
        self.article_entry_id = article_entry_id


    @staticmethod
    def get_all():
        websites_query = '''   
            SELECT id, name, rss_url, article_entry_element, article_entry_class, article_entry_id 
            FROM websites
        '''
        websites_results = cursor.execute(websites_query)
        return [NewsWebsite(*website_info) for website_info in websites_results]


    def scrape_rss_feed(self):
        soup = get_soup(self.rss_url)
        rss_articles = soup.find_all('item')
        for rss_article in rss_articles:
            #check if exists?
            new_article = NewsArticle(rss_article, self.article_entry_element, self.article_entry_class, self.article_entry_id, self.id)
            new_article.create_one()
            time.sleep(1)


    @staticmethod
    def scrape_all():
        websites = NewsWebsite.get_all()
        for website in websites:
            website.scrape_rss_feed()


    @staticmethod
    def clean_all():
        df = NewsArticle.get_unclean_articles()
        cleaned_df = NewsArticle.clean_articles(df)
        NewsArticle.save_cleaned_articles(cleaned_df)
