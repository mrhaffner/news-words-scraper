import sqlite3

db = sqlite3.connect('website_data.sqlite3')
cursor = db.cursor()

create_articles_table = '''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        website_id TEXT NOT NULL,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        text TEXT NOT NULL,
        FOREIGN KEY (website_id) REFERENCES websites (id)
);'''

cursor.execute(create_articles_table)