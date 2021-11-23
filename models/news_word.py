from project import cursor, db

class NewsWord:
    WORD_QUERY = '''
        SELECT word, cnn_count, guardian_count, huffpo_count, breitbart_count, fox_count, federalist_count, npr_count, rt_count, cbc_count
        FROM words
        WHERE word = ?
    '''

    CREATE_SQL = '''
        INSERT INTO words (word)
        VALUES(?)
    '''

    def __init__(self, word, cnn_count=0, guardian_count=0, huffpo_count=0, breitbart_count=0, fox_count=0, federalist_count=0, npr_count=0, rt_count=0, cbc_count=0):
        self.word = word
        self.cnn_count = cnn_count
        self.guardian_count = guardian_count
        self.huffpo_count = huffpo_count
        self.breitbart_count = breitbart_count
        self.fox_count = fox_count
        self.federalist_count = federalist_count
        self.npr_count = npr_count
        self.rt_count = rt_count
        self.cbc_count = cbc_count

    @staticmethod
    def parse_news_article(news_article):
        words_counter = news_article.count_words()
        for word, count in words_counter.items():
            word_query_result = NewsWord.get_word(word)
            populated_word = NewsWord(word)

            if len(word_query_result.fetchall()) == 0:
                populated_word.create_one()

            column = f'{news_article.website_id}_count'
            #should be increment count method?
            current_count = getattr(populated_word, column)
            setattr(populated_word, column, current_count + count)
            
            populated_word.update_word_count(column, populated_word)

    # def increase_word_count(self, column, count_to_add):


    @staticmethod
    def get_word(word):
        found_word = cursor.execute(NewsWord.WORD_QUERY, (word,))
        return found_word if found_word else None


    def update_word_count(self, column, news_word):
        update_sql = f'UPDATE words SET {column} = ? WHERE word = ?'
        cursor.execute(update_sql, (getattr(news_word, column), news_word.word))
        db.commit()


    def create_one(self):
        cursor.execute(NewsWord.CREATE_SQL, (self.word,))
        db.commit()

#when do I emplement saving the words? after article creation?

#create list of bad words not to save