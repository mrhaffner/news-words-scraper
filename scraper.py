from project import db
from models.news_website import NewsWebsite


NewsWebsite.scrape_all()
NewsWebsite.clean_all()

db.close()