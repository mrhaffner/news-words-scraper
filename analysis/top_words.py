from project import db
from datetime import datetime
import pandas as pd
import texthero as hero
# import matplotlib.pyplot as plt
#get by date, date range
#by political affiliation
#past 7 days?
#calculate total numbers of words analyzed per column
#calculate % occurence 
class TopWords:
    def display_all(today=False):
        base_df = TopWords.get_all_articles(today)
        today_qualifier = ' from today' if today else ''
        output_qualifier = 'all articles' + today_qualifier
        TopWords.output_word_dataframe_with_type(base_df,  output_qualifier)


    def get_all_articles(today):
        query = TopWords.get_sql_query(today)
        return pd.read_sql_query(query, db)

#condense right wring and left wing into one method with political leaning arguement
    def display_right_wing(today=False):
        base_df = TopWords.get_all_right_wing_articles(today)
        today_qualifier = ' from today' if today else ''
        output_qualifier = 'right wing articles' + today_qualifier
        TopWords.output_word_dataframe_with_type(base_df, output_qualifier)


    def get_all_right_wing_articles(today):
        query = TopWords.get_sql_query(today=today, right_wing=True)
        return pd.read_sql_query(query, db)


    def display_left_wing(today=False):
        base_df = TopWords.get_all_left_wing_articles(today)
        today_qualifier = ' from today' if today else ''
        output_qualifier = 'left wing articles' + today_qualifier
        TopWords.output_word_dataframe_with_type(base_df, output_qualifier)


    def get_all_left_wing_articles(today):
        query = TopWords.get_sql_query(today=today, left_wing=True)
        return pd.read_sql_query(query, db)


    def output_word_dataframe_with_type(base_df, query_type):
        print(f'Analyzing {base_df.shape[0]} News Articles...')
        print('... \n')
        
        df = TopWords.create_title_text_sum_df(base_df)
        pd.options.display.float_format = '{:,.0f}'.format

        print(f'Here are the Top Words for {query_type}:')
        print(df.head(40))
        print('\n')
        #print words counted?


    def create_title_text_sum_df(base_df):
        top_title_words = hero.top_words(base_df['clean_title'])
        top_text_words = hero.top_words(base_df['clean_text'])
        sum_all_words = top_text_words.add(top_title_words, fill_value=0).sort_values(ascending=False)
        title_df = pd.DataFrame({'title_word': top_title_words.index, 'title_count': top_title_words.values})
        text_df = pd.DataFrame({'text_word': top_text_words.index, 'text_count': top_text_words.values})
        sum_df = pd.DataFrame({'sum_word': sum_all_words.index, 'sum_count': sum_all_words.values})
        return pd.concat([title_df, text_df, sum_df], axis=1)


    def get_sql_query(today = False, right_wing = False, left_wing = False):
        base_sql = 'SELECT website_id, clean_title, clean_text FROM articles'
        today_qualifier = f" date = '{datetime.today().strftime('%Y-%m-%d')}'" if today else ''

        if right_wing or left_wing:
            political_leaning = 'right_wing' if right_wing else 'left_wing'
            political_sql = f'{base_sql} AS a INNER JOIN websites AS w ON w.id = a.website_id WHERE tag_{political_leaning} = 1'
            today_qualifier_plus = f" AND{today_qualifier}" if today else ''
            return political_sql + today_qualifier_plus
        
        today_qualifier_plus = f" WHERE{today_qualifier}" if today else ''
        return base_sql + today_qualifier_plus

    #need column that says right wing or left wing
    #axis clean title/text vs right_wing/left_wing as political_leaning

    #need to create input df
    #where do I call this method?
    
    # def graph_text(df, analyze_col):
    #     df["parse"] = df[analyze_col].apply(st.whitespace_nlp_with_sentences)
    #     #political_leaning maybe change to input variable for state sponsored or compare newsite to newsite
    #     #could even let users generate their own comparison?
    #     corpus = (
    #         st.CorpusFromParsedDocuments(df, category_col="political_leaning", parsed_col="parse")
    #         .build()
    #         .get_unigram_corpus()
    #         .compact(st.AssociationCompactor(2000))
    #     )

    #     ##missing code? scaled-f?

    #     html = st.produce_scattertext_explorer(
    #         corpus,
    #         category="political_leaning",
    #         category_name="Right Wing",
    #         not_category_name="Left Wing",
    #         minimum_term_frequency=5,
    #         pmi_threshold_coefficient=0,
    #         width_in_pixels=1000,
    #         # metadata=corpus.get_df()["page_host"],
    #         transform=st.Scalers.dense_rank,
    #     )
    #     #variable name to write different input options to different files? today vs all etc
    #     open("right_wing_vs_left_wing_news_words.html", "w").write(html)