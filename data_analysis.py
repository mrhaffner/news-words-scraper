from project import db
import pandas as pd
import texthero as hero
import matplotlib.pyplot as plt

# df = pd.read_sql_query('SELECT * FROM words', db)
# df['total_count'] = df.loc[:, df.columns != 'word'].sum(axis=1)
# # print(df.head())
# top_words = df.sort_values('total_count', ascending=False)
# print(top_words[360:400])
# # plt.hist()

df = pd.read_sql_query('SELECT * FROM articles', db)
# title_df = df[['website_id', 'title']]
# title_df['title_word_count'] = title_df['title'].str.len()
# # print(title_df.head(10))

print(df.loc[3, 'text'])


text_df = df[['website_id', 'text']]
# text_df['text_word_count'] = text_df['text'].str.len()

# print(text_df.head(10))
# df['title'] = hero.clean(df['title'])
# print(df.loc[0, 'text'])
df['text'] = hero.clean(df['text'])
# print(df.loc[0, 'text'])
# print(hero.top_words(df['text'])[:100])
print('~~~~~~~~~~~~~~~~~~~~~~~')
print('~~~~~~~~~~~~~~~~~~~~~~~')

print(df.loc[3, 'text'])


# text = "(CNN)Whether it's your first time cooking a turkey or you are a poultry aficionado, mishaps can happen in the kitchen"
# df = pd.DataFrame(data={'text':[text]})
# df['clean_text'] = hero.clean(df['text'])
# print(df.loc[0, 'clean_text'])