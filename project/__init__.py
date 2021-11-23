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
    )
;'''

cursor.execute(create_articles_table)

create_words_table = '''
    CREATE TABLE IF NOT EXISTS words (
        word TEXT PRIMARY KEY,
        cnn_count INTEGER DEFAULT 0 NOT NULL,
        guardian_count INTEGER DEFAULT 0 NOT NULL,
        huffpo_count INTEGER DEFAULT 0 NOT NULL,
        breitbart_count INTEGER DEFAULT 0 NOT NULL,
        fox_count INTEGER DEFAULT 0 NOT NULL,
        federalist_count INTEGER DEFAULT 0 NOT NULL,
        npr_count INTEGER DEFAULT 0 NOT NULL,
        rt_count INTEGER DEFAULT 0 NOT NULL,
        cbc_count INTEGER DEFAULT 0 NOT NULL,
    );
'''

cursor.execute(create_words_table)