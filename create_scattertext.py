import scattertext as st    
import pandas as pd
from project import db
import datetime
    

def get_title_df(today=False):
    today_sql = f" AND date = '{datetime.today().strftime('%Y-%m-%d')}'" if today else ''
    query = f'''
        SELECT a.clean_title,
        CASE WHEN w.tag_right_wing = 1 THEN 'Right Wing'
            WHEN w.tag_left_wing = 1 THEN 'Left Wing'
        END AS political_leaning
        FROM articles AS a
        INNER JOIN websites AS w
        ON w.id = a.website_id
        WHERE (w.tag_right_wing = 1
            OR w.tag_left_wing = 1){today_sql};
    '''
    return pd.read_sql(query, db)


def get_text_df(today=False):
    today_sql = f" AND date = '{datetime.today().strftime('%Y-%m-%d')}'" if today else ''
    query = f'''
        SELECT a.clean_text,
        CASE WHEN w.tag_right_wing = 1 THEN 'Right Wing'
            WHEN w.tag_left_wing = 1 THEN 'Left Wing'
        END AS political_leaning
        FROM articles AS a
        INNER JOIN websites AS w
        ON w.id = a.website_id
        WHERE (w.tag_right_wing = 1
            OR w.tag_left_wing = 1){today_sql};
    '''
    return pd.read_sql(query, db)


def graph_text(df, analyze_col):
    df["parse"] = df[analyze_col].apply(st.whitespace_nlp_with_sentences)
    #political_leaning maybe change to input variable for state sponsored or compare newsite to newsite
    #could even let users generate their own comparison?
    corpus = (
        st.CorpusFromParsedDocuments(df, category_col="political_leaning", parsed_col="parse")
        # st.CorpusFromParsedDocuments(df, category_col="political_leaning", text_col=analyze_col, nlp=nlp)
        .build()
        .get_unigram_corpus()
        .compact(st.AssociationCompactor(2000))
    )

    # print(list(corpus.get_scaled_f_scores_vs_background().index[:10]))

    html = st.produce_scattertext_explorer(
        corpus,
        category="Right Wing",
        category_name="Right Wing",
        not_category_name="Left Wing",
        minimum_term_frequency=5,
        pmi_threshold_coefficient=0,
        width_in_pixels=1000,
        transform=st.Scalers.dense_rank,
    )
    #variable name to write different input options to different files? today vs all etc
    return html

def save_graph_by_date_text_field(text_field='title', today=False):
    if text_field == 'title':
        df = get_title_df(today)
        html = graph_text(df, 'clean_title')
        today_text = '_today' if today else ''
        open(f"right_wing_vs_left_wing_title_words{today_text}.html", "w").write(html)
    elif text_field == 'text':
        df = get_text_df(today)
        html = graph_text(df, 'clean_text')
        today_text = '_today' if today else ''
        open(f"right_wing_vs_left_wing_text_words{today_text}.html", "w").write(html)
    else:
        print('Invalid Input')


db.close()