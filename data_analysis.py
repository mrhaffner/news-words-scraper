from analysis.top_words import TopWords
from project import db
import pandas as pd
import texthero as hero


#plot left wing vs right wing
#plot state sponsored vs not
TopWords.display_all()
TopWords.display_all(today=True)
# TopWords.display_today()
TopWords.display_right_wing()
TopWords.display_left_wing()

# df = pd.read_sql_query('SELECT * FROM words', db)
# df['total_count'] = df.loc[:, df.columns != 'word'].sum(axis=1)
# # print(df.head())
# top_words = df.sort_values('total_count', ascending=False)
# print(top_words[360:400])
# # plt.hist()

# r_df = pd.read_sql_query('SELECT website_id, clean_title, clean_text FROM articles AS a INNER JOIN websites AS w ON w.id = a.website_id WHERE tag_right_wing = 1', db)
# l_df = pd.read_sql_query('SELECT website_id, clean_title, clean_text FROM articles AS a INNER JOIN websites AS w ON w.id = a.website_id WHERE tag_left_wing = 1', db)
# print(hero.top_words(df['clean_text'])[:40])
# r_title_variant = r_df[r_df['clean_title'].str.contains('covid')]
# r_title_variant = r_df['clean_title']
# print(r_title_variant.shape)
# print(hero.top_words(r_title_variant)[:40])

# print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# l_title_variant = l_df[l_df['clean_title'].str.contains('covid')]
# l_title_variant = l_df['clean_title']
# print(l_title_variant.shape)
# print(hero.top_words(l_title_variant)[:40])

# title_df = df[['website_id', 'title']]
# title_df['title_word_count'] = title_df['title'].str.len()
# # print(title_df.head(10))



# text_df = df[['website_id', 'text']]
# text_df['text_word_count'] = text_df['text'].str.len()

# print(text_df.head(10))
# df['title'] = hero.clean(df['title'])
# print(df.loc[0, 'text'])
# df['text'] = hero.clean(df['text'])
# print(df.loc[0, 'text'])
# print(hero.top_words(df['text'])[:100])



# text = "(CNN)Whether it's your first time cooking a turkey or you are a poultry aficionado, mishaps can happen in the kitchen"
# df = pd.DataFrame(data={'text':[text]})
# df['clean_text'] = hero.clean(df['text'])
# print(df.loc[0, 'clean_text'])


#need to get a count of words from text/article for each news websites to get a percentage of total key words for occurance

#maybe get words by day
#set words to ignore
#find what words occur near top words?