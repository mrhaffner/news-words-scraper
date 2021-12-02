import scattertext as st    
import pandas as pd
from project import db
    

def get_title_df():
    query = '''
        SELECT a.clean_title,
        CASE WHEN w.tag_right_wing = 1 THEN 'Right Wing'
            WHEN w.tag_left_wing = 1 THEN 'Left Wing'
        END AS political_leaning
        FROM articles AS a
        INNER JOIN websites AS w
        ON w.id = a.website_id
        WHERE w.tag_right_wing = 1
            OR w.tag_left_wing = 1
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
    open("right_wing_vs_left_wing_news_words.html", "w").write(html)


df = get_title_df()
graph_text(df, 'clean_title')


db.close()