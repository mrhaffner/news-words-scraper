from project import db
from datetime import datetime
import pandas as pd
import texthero as hero

#get by date, date range
#by political affiliation
class TopWords:
    BASE_SQL = 'SELECT website_id, clean_title, clean_text FROM articles'

    def display_all_top_words():
        base_df = TopWords.get_all_articles()
        TopWords.output_word_dataframe_with_type(base_df, 'all articles')


    def get_all_articles():
        query = TopWords.BASE_SQL
        return pd.read_sql_query(query, db)


    def display_todays_top_words():
        base_df = TopWords.get_todays_articles()
        TopWords.output_word_dataframe_with_type(base_df, "today's articles")


    def get_todays_articles():
        todays_date = datetime.today().strftime('%Y-%m-%d')
        query = f"{TopWords.BASE_SQL} WHERE date = '{todays_date}'"
        return pd.read_sql_query(query, db)


    def output_word_dataframe_with_type(base_df, query_type):
        print(f'Analyzing {base_df.shape[0]} News Articles...')
        print('... \n')
        
        df = TopWords.create_title_text_sum_df(base_df)
        pd.options.display.float_format = '{:,.0f}'.format
        print(f'Here are the Top Words for {query_type}:')
        print(df.head(40) + '\n')
        #print words counted?


    def create_title_text_sum_df(base_df):
        top_title_words = hero.top_words(base_df['clean_title'])
        top_text_words = hero.top_words(base_df['clean_text'])
        sum_all_words = top_text_words.add(top_title_words, fill_value=0).sort_values(ascending=False)
        title_df = pd.DataFrame({'title_word': top_title_words.index, 'title_count': top_title_words.values})
        text_df = pd.DataFrame({'text_word': top_text_words.index, 'text_count': top_text_words.values})
        sum_df = pd.DataFrame({'sum_word': sum_all_words.index, 'sum_count': sum_all_words.values})
        return pd.concat([title_df, text_df, sum_df], axis=1)




    # query = '''SELECT website_id, clean_title, clean_text, date, tag_left_wing, tag_right_wing, tag_state_funded
    #             FROM articles AS a 
    #             INNER JOIN websites AS w ON w.id = a.website_id;'''
    # base_df = pd.read_sql_query(query, db)