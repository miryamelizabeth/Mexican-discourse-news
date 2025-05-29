import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# sns.set_style('darkgrid')
sns.set_theme(context='paper', style='darkgrid', palette='Dark2', font_scale=1.5, font='Arial')



# 1. Cargar los datos
data = pd.read_csv(r'..\Dataset\7_Data_final\final_dataset.csv', parse_dates=['video_published_at_day'])
data = data[~data['channel_title'].isin(['CNN en Español', 'Noticias Telemundo'])]

sentiment = pd.read_csv(r'..\Dataset\8_Data_attributes\sentiment_comments.csv').drop(['video_id'], axis=1)
emotion = pd.read_csv(r'..\Dataset\8_Data_attributes\emotions_comments.csv').drop(['video_id'], axis=1)
hate = pd.read_csv(r'..\Dataset\8_Data_attributes\hate_speech_comments.csv').drop(['video_id'], axis=1)

otherAttributes = pd.merge(left=sentiment, right=emotion, on='id', how='left').merge(right=hate, on='id', how='left')

df = pd.merge(left=data, right=otherAttributes, on='id', how='left')

print(f'\n*** TOTAL DATASET: {df.shape[0]:,d}\n')


hateOrder = ['Hateful', 'Non-hateful']
aggressiveOrder = ['Aggressive', 'Non-aggressive']




"""
Analisis de Sentimientos / Emociones / Hate / Aggression
"""
### Distribución de los sentimientos
sentiment_counts = df['sentiment_tag'].value_counts(normalize=True)
print(f'\n*** Sentiment distribution ***')
print(sentiment_counts)

plt.figure(figsize=(6,4)) # figsize=(8,6)
sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, order=sentiment_counts.index, palette='Dark2')
# plt.title('Distribution of sentiments in comments')
plt.xlabel('Sentiment label')
plt.ylabel('Frequency of comments (%)')
plt.ylim(0, 0.95)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\4_distribution_sentiment_comments.pdf', bbox_inches='tight', dpi=300)


### Distribución de las emociones
emotion_counts = df['emotion_tag'].value_counts(normalize=True)
print(f'\n*** Emotion distribution ***')
print(emotion_counts)

plt.figure(figsize=(6,4))
sns.barplot(x=emotion_counts.index, y=emotion_counts.values, order=emotion_counts.index, palette='Dark2')
# plt.title('Distribution of emotions in comments')
plt.xlabel('Emotion label')
plt.ylabel('Frequency of comments (%)')
plt.ylim(0, 0.95)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\4_distribution_emotions_comments.pdf', bbox_inches='tight', dpi=300)


### 2. Distribución del hate
hateful_counts = df['hateful_tag'].value_counts(normalize=True)
print(f'\n*** Hate distribution ***')
print(hateful_counts)

plt.figure(figsize=(6,4))
sns.barplot(x=hateful_counts.index, y=hateful_counts.values, order=hateOrder, palette='Dark2')
# plt.title('Distribution of hateful in comments')
plt.xlabel('Hateful label')
plt.ylabel('Frequency of comments (%)')
plt.ylim(0, 0.95)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\4_distribution_hate_comments.pdf', bbox_inches='tight', dpi=300)


### 2. Distribución de la agresión
aggressive_counts = df['aggressive_tag'].value_counts(normalize=True)
print(f'\n*** Aggressiveness distribution ***')
print(aggressive_counts)

plt.figure(figsize=(6,4))
sns.barplot(x=aggressive_counts.index, y=aggressive_counts.values, order=aggressiveOrder, palette='Dark2')
# plt.title('Distribution of aggressiveness in comments')
plt.xlabel('Aggressive label')
plt.ylabel('Frequency of comments (%)')
plt.ylim(0, 0.95)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\4_distribution_aggression_comments.pdf', bbox_inches='tight', dpi=300)




"""
Analisis de los atributos por likes (popularidad)
"""
### ¿Hay una relación entre el sentimiento y los likes del comentario?
zz1 = df.groupby(['sentiment_tag'])['comment_likeCount'].describe().round(1)
zz2 = df.groupby(['emotion_tag'])['comment_likeCount'].describe().round(1)
zz3 = df.groupby(['hateful_tag'])['comment_likeCount'].describe().round(1)
zz4 = df.groupby(['aggressive_tag'])['comment_likeCount'].describe().round(1)

print(zz1)
print(zz2)
print(zz3)
print(zz4)


plt.figure(figsize=(6,4))
sns.barplot(data=df, x='sentiment_tag', y='comment_likeCount', errorbar='se', order=sentiment_counts.index, palette='Dark2')
# plt.title('Relationship between sentiment and likes in comments')
plt.xlabel('Sentiment label')
plt.ylabel('Mean number of likes (± SEM)')
plt.ylim(0, 6.3)
# plt.show()
plt.savefig(r'..\Plots\5_sentiment_likes.pdf', bbox_inches='tight', dpi=300)


# Relacion emociones y likes
plt.figure(figsize=(6,4))
sns.barplot(data=df, x='emotion_tag', y='comment_likeCount', errorbar='se', order=emotion_counts.index, palette='Dark2')
# plt.title('Relationship between emotion and likes in comments')
plt.xlabel('Emotion label')
plt.ylabel('Mean number of likes (± SEM)')
plt.ylim(0, 6.3)
# plt.show()
plt.savefig(r'..\Plots\5_emotion_likes.pdf', bbox_inches='tight', dpi=300)


# Relacion hate y likes
plt.figure(figsize=(6,4))
sns.barplot(data=df, x='hateful_tag', y='comment_likeCount', errorbar='se', order=hateOrder, palette='Dark2')
# plt.title('Relationship between hateful and likes in comments')
plt.xlabel('Hateful label')
plt.ylabel('Mean number of likes (± SEM)')
plt.ylim(0, 6.3)
# plt.show()
plt.savefig(r'..\Plots\5_hate_likes.pdf', bbox_inches='tight', dpi=300)


# Relacion aggression y likes
plt.figure(figsize=(6,4))
sns.barplot(data=df, x='aggressive_tag', y='comment_likeCount', errorbar='se', order=aggressiveOrder, palette='Dark2')
# plt.title('Relationship between aggressiveness and likes in comments')
plt.xlabel('Aggressive label')
plt.ylabel('Mean number of likes (± SEM)')
plt.ylim(0, 6.3)
# plt.show()
plt.savefig(r'..\Plots\5_aggression_likes.pdf', bbox_inches='tight', dpi=300)




### Analizar qué comentarios reciben más likes y si tienen características comunes
print(f'\n*** TOP comments (likes) ***')
top_comments = df.nlargest(100, 'comment_likeCount') # top_comments = df[df['comment_likeCount'] >= 500]
print(top_comments['comment_likeCount'].describe().round(2))

yy1 = top_comments['sentiment_tag'].value_counts(normalize=True)
yy2 = top_comments['emotion_tag'].value_counts(normalize=True)
yy3 = top_comments['hateful_tag'].value_counts(normalize=True)
yy4 = top_comments['aggressive_tag'].value_counts(normalize=True)

print(yy1)
print(yy2)
print(yy3)
print(yy4)


# Distribución de sentimiento en los comentarios más populares
plt.figure(figsize=(6,4))
sns.countplot(data=top_comments, stat='percent', x='sentiment_tag', order=top_comments['sentiment_tag'].value_counts().index, palette='Dark2')
# plt.title('Sentiment in popular comments')
plt.xlabel('Sentiment label')
plt.ylabel('Frequency of comments (%)')
plt.ylim(0, 100)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\6_sentiment_comments_popular.pdf', bbox_inches='tight', dpi=300)


# Distribución de emociones en los comentarios más populares
plt.figure(figsize=(6,4))
sns.countplot(data=top_comments, stat='percent', x='emotion_tag', order=top_comments['emotion_tag'].value_counts().index, palette='Dark2')
# plt.title('Emotion in popular comments')
plt.xlabel('Emotion label')
plt.ylabel('Frequency of comments (%)')
plt.ylim(0, 100)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\6_emotion_comments_popular.pdf', bbox_inches='tight', dpi=300)


# Distribución de hate en los comentarios más populares
plt.figure(figsize=(6,4))
sns.countplot(data=top_comments, stat='percent', x='hateful_tag', order=hateOrder, palette='Dark2')
# plt.title('Hateful in popular comments')
plt.xlabel('Hateful label')
plt.ylabel('Frequency of comments (%)')
plt.ylim(0, 100)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\6_hate_comments_popular.pdf', bbox_inches='tight', dpi=300)


# Distribución de aggression en los comentarios más populares
plt.figure(figsize=(6,4))
sns.countplot(data=top_comments, stat='percent', x='aggressive_tag', order=aggressiveOrder, palette='Dark2')
# plt.title('Aggressiveness in popular comments')
plt.xlabel('Aggressive label')
plt.ylabel('Frequency of comments (%)')
plt.ylim(0, 100)
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\6_aggression_comments_popular.pdf', bbox_inches='tight', dpi=300)
