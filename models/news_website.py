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
    def scrape_all():
        start_time = time.time()
        print('Engaging News Scraper')
        print('...')

        websites = NewsWebsite.get_all()
        for website in websites:
            NewsWebsite.scrape_website(website)
            if website.name == 'CNN':
                break

        print('Finished scraping')
        print(f'Scraping took {time.time() - start_time} seconds')


    @staticmethod
    def get_all():
        websites_query = '''   
            SELECT id, name, rss_url, article_entry_element, article_entry_class, article_entry_id 
            FROM websites
        '''
        websites_results = cursor.execute(websites_query)
        return [NewsWebsite(*website_info) for website_info in websites_results]


    @staticmethod
    def scrape_website(website):
        print(f'Scraping {website.name}')

        start_time = time.time()
        website.scrape_rss_feed()
        
        print(f'Scraping {website.name} took {time.time() - start_time} seconds')


    def scrape_rss_feed(self):
        soup = get_soup(self.rss_url)
        rss_articles = soup.find_all('item')

        for rss_article in rss_articles:
            new_article = NewsArticle(rss_article, self.article_entry_element, self.article_entry_class, self.article_entry_id, self.id)
            if new_article.text != '':
                new_article.create_one()
            time.sleep(1)


    @staticmethod
    def clean_all():
        df = NewsArticle.get_unclean_articles()
        cleaned_df = NewsArticle.clean_articles(df)
        NewsArticle.save_cleaned_articles(cleaned_df)
