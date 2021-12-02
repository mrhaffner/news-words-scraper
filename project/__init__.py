import sqlite3

db = sqlite3.connect('website_data.sqlite3')
cursor = db.cursor()

create_articles_table = '''
    CREATE TABLE IF NOT EXISTS articles (
        website_id TEXT NOT NULL,
        url TEXT NOT NULL PRIMARY KEY,
        date TEXT NOT NULL,
        title TEXT NOT NULL,
        text TEXT NOT NULL,
        clean_title TEXT,
        clean_text TEXT,
        FOREIGN KEY (website_id) REFERENCES websites (id)
    );
'''

cursor.execute(create_articles_table)
