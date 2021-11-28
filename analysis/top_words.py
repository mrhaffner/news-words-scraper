from project import db
import pandas as pd
import texthero as hero

class TopWords:
    def display_all_top_words():
        base_df = TopWords.get_words()

        print(f'Analyzing {base_df.shape[0] - 1} News Articles...')
        print('... \n')
        
        df = TopWords.create_all_words_df(base_df)
        pd.options.display.float_format = '{:,.0f}'.format
        print(df.head(40))


    def get_words():
        query = 'SELECT website_id, clean_title, clean_text FROM articles'
        return pd.read_sql_query(query, db)


    def create_all_words_df(base_df):
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