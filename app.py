from project import db
from models.news_website import NewsWebsite

websites = NewsWebsite.get_all()

for website in websites:
    website.scrape_rss_feed()
    
db.commit()

db.close()