import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random
import os

from nltk import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud


random.seed(42)
np.random.seed(42)


sns.set_theme(context='paper', style='darkgrid', palette='Dark2', font_scale=1.5, font='Arial')



# 1. Cargar los datos
data = pd.read_csv(r'..\Dataset\7_Data_final\final_dataset.csv', parse_dates=['video_published_at_day'])

heads = pd.read_csv(r'..\Dataset\8_Data_attributes\headline_videos.csv')
sentiment = pd.read_csv(r'..\Dataset\8_Data_attributes\sentiment_comments.csv').drop(['video_id'], axis=1)
emotion = pd.read_csv(r'..\Dataset\8_Data_attributes\emotions_comments.csv').drop(['video_id'], axis=1)
hate = pd.read_csv(r'..\Dataset\8_Data_attributes\hate_speech_comments.csv').drop(['video_id'], axis=1)


other1 = pd.merge(left=data, right=heads, on='video_id', how='left')
other2 = pd.merge(left=sentiment, right=emotion, on='id', how='left').merge(right=hate, on='id', how='left')

df = pd.merge(left=other1, right=other2, on='id', how='left')

print(f'\n*** TOTAL DATASET: {df.shape[0]:,d}\n')




""""
>> Tipo de noticia <<
- Likes/comments/views por tipo de noticias
"""
print(f'\n\n*** Likes/comments/views por tipo de noticias ***\n')

temp1 = df[['video_id', 'video_headline', 'video_total_views', 'video_total_likes', 'video_total_comments']].drop_duplicates(subset='video_id')
orderHeadlines = sorted(df['video_headline'].unique())

stats1 = temp1['video_headline'].value_counts()
stats2 = temp1['video_headline'].value_counts(normalize=True)
stats3 = temp1.groupby(['video_headline'])[['video_total_views', 'video_total_likes', 'video_total_comments']].agg(['mean', 'std']).reset_index()
print(stats1)
print(stats2)
print(stats3)

# Total views
plt.figure(figsize=(10,6)) # figsize=(6,4)
sns.barplot(x='video_headline', y='video_total_views', data=temp1, errorbar='se', order=orderHeadlines, palette='Dark2')
# plt.title('Relation between news classification and # views')
plt.xlabel('News classification')
plt.ylabel('Mean number of views (± SEM)')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
# plt.show()
plt.savefig(r'..\Plots\8_headline_views.pdf', bbox_inches='tight', dpi=300)


# Total likes
plt.figure(figsize=(10,6)) # figsize=(6,4)
sns.barplot(x='video_headline', y='video_total_likes', data=temp1, errorbar='se', order=orderHeadlines, palette='Dark2')
# plt.title('Relation between news classification and # likes')
plt.xlabel('News classification')
plt.ylabel('Mean number of likes (± SEM)')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
# plt.show()
plt.savefig(r'..\Plots\8_headline_likes.pdf', bbox_inches='tight', dpi=300)


# Comments
commentsReal = df.groupby(['video_id', 'video_headline'])['id'].count().reset_index(name='totalCommentsReal')

plt.figure(figsize=(10,6)) # figsize=(6,4)
sns.barplot(x='video_headline', y='totalCommentsReal', data=commentsReal, errorbar='se', order=orderHeadlines, palette='Dark2')
# plt.title('Relation between news classification and # comments')
plt.xlabel('News classification')
plt.ylabel('Mean number of comments (± SEM)')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
# plt.show()
plt.savefig(r'..\Plots\8_headline_commentsReal.pdf', bbox_inches='tight', dpi=300)


# Sentiment
print(f'\n*** Sentiment distribution por tipo de noticias ***')
print(pd.crosstab(df['video_headline'], df['sentiment_tag'], normalize='index').reset_index())

ax = pd.crosstab(df['video_headline'], df['sentiment_tag'], normalize='index').plot(kind='bar', stacked=True, width=0.81, figsize=(10,6))
# plt.title('Relation between news classification and sentiment')
plt.xlabel('News classification')
plt.ylabel('Frequency of comments (%)')
plt.xticks(rotation=0)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=1, symbol=' %'))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()
plt.savefig(r'..\Plots\8_headline_sentiment.pdf', bbox_inches='tight', dpi=300)


# Emotion
print(f'\n*** Emotion distribution por tipo de noticias ***')
print(pd.crosstab(df['video_headline'], df['emotion_tag'], normalize='index').reset_index())

ax = pd.crosstab(df['video_headline'], df['emotion_tag'], normalize='index').plot(kind='bar', stacked=True, width=0.81, figsize=(10,6))
# plt.title('Relation between news classification and emotion')
plt.xlabel('News classification')
plt.ylabel('Frequency of comments (%)')
plt.xticks(rotation=0)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=1, symbol=' %'))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()
plt.savefig(r'..\Plots\8_headline_emotion.pdf', bbox_inches='tight', dpi=300)


# Hate
print(f'\n*** Hate distribution por tipo de noticias ***')
print(pd.crosstab(df['video_headline'], df['hateful_tag'], normalize='index').reset_index())

ax = pd.crosstab(df['video_headline'], df['hateful_tag'], normalize='index').plot(kind='bar', stacked=True, width=0.81, figsize=(10,6))
# plt.title('Relation between news classification and hate speech')
plt.xlabel('News classification')
plt.ylabel('Frequency of comments (%)')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=1, symbol=' %'))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()
plt.savefig(r'..\Plots\8_headline_hate.pdf', bbox_inches='tight', dpi=300)


# Aggression
print(f'\n*** Aggression distribution por tipo de noticias ***')
print(pd.crosstab(df['video_headline'], df['aggressive_tag'], normalize='index').reset_index())

ax = pd.crosstab(df['video_headline'], df['aggressive_tag'], normalize='index').plot(kind='bar', stacked=True, width=0.81, figsize=(10,6))
# plt.title('Relation between news classification and aggressiveness')
plt.xlabel('News classification')
plt.ylabel('Frequency of comments (%)')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=1, symbol=' %'))
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()
plt.savefig(r'..\Plots\8_headline_aggression.pdf', bbox_inches='tight', dpi=300)





"""
Palabras más comunes (Nube de palabras)
- Palabras mas comunes en titulos / comentarios
"""
### Wordcloud Titles news
titlesDf = pd.read_csv(r'..\Dataset\9_Data_topics\videos_title_topic.csv').merge(right=heads, on='video_id', how='left')
titlesDf = titlesDf[titlesDf['video_id'].isin(data['video_id'])]

print(f'\n*** TOTAL VIDEO: {titlesDf.shape[0]:,d}\n')


def graficarNube(datitos, filename, max_words=100):

	stop_words = stopwords.words('spanish') + ['tras', 'asi', 'ser', 'si', 'deja', 'va', 'paso', 'año', 'años', 'paso', 'noticias', 'dice', 'mexico']

	sentences = ' '.join(datitos['texto_nostop_lemma'].values)
	tokens = word_tokenize(sentences)

	wordcloud = WordCloud(background_color='white',
				max_words=max_words,
				stopwords=stop_words,
				# width=1200, height=800,
				width=600, height=400,
				random_state=42).generate_from_text(' '.join(tokens)) #.generate_from_frequencies(fdist)

	plt.figure(figsize=(30, 20))
	plt.imshow(wordcloud)
	plt.axis('off')
	# plt.show()
	plt.savefig(os.path.join(r'..\Plots', f'FigB_wordcloud_{filename}.pdf'), bbox_inches='tight', dpi=300)

## All
graficarNube(titlesDf, 'all')

### Por tipo de noticia
for x in titlesDf['video_headline'].unique():
	temporal = titlesDf[titlesDf['video_headline'] == x]
	graficarNube(temporal, f'{x}')
