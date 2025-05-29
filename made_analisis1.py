import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from datetime import datetime


# sns.set_style('darkgrid')
sns.set_theme(context='paper', style='darkgrid', palette='Dark2', font_scale=1.5, font='Arial')




# Cargar el archivo CSV
df = pd.read_csv(r'..\Dataset\7_Data_final\final_dataset.csv', parse_dates=['video_published_at_day'])

print(f'\n*** TOTAL DATASET: {df.shape[0]:,d}\n')



"""
Distribución de publicaciones a lo largo del tiempo
"""
def getPartDay(hour):
	if hour >= 5 and hour < 12: return 'Morning'
	elif hour >= 12 and hour < 17: return 'Afternoon'
	elif hour >= 17 and hour < 21: return 'Evening'
	else: return 'Night'


# Eliminar duplicados videos
columns = ['video_id', 'video_published_at_day', 'video_published_at_hour', 'video_duration_hour', 'video_duration_minutes', 'video_duration_seconds', 'video_total_views', 'video_total_likes', 'video_total_comments']
temp1 = df[columns].drop_duplicates(subset='video_id')

# Obtener dia de la semana
temp1['week_day'] = temp1['video_published_at_day'].apply(lambda x: x.strftime('%A'))

# Convertir la hora a formato datetime
temp1['video_published_at_hour'] = pd.to_datetime(temp1['video_published_at_hour'], format='%H:%M:%S').dt.hour

temp1['published_part_day'] = temp1['video_published_at_hour'].apply(getPartDay)


plt.figure(figsize=(10, 5))
sns.histplot(x='video_published_at_day', data=temp1, bins=12, kde=True, palette='Dark2')
# plt.title('Distribution of publications over time')
plt.xlabel('Date of publication')
plt.ylabel('Number of posts')
plt.xticks(rotation=45)
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
# plt.show()
plt.savefig(r'..\Plots\1_distribucion_mensual.pdf', bbox_inches='tight', dpi=300)


## Cifras de la grafica
print('\n*** Porcentaje de videos publicados por día de la semana **')
print(temp1['week_day'].value_counts(normalize=True))

plt.figure(figsize=(10, 5))
sns.countplot(x='week_day', data=temp1, stat='percent', order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],  palette='Dark2')
# plt.title('Rate of videos published per day of the week')
plt.xlabel('Day of the week')
plt.ylabel('Frequency of posts (%)')
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\1_distribucion_semana.pdf', bbox_inches='tight', dpi=300)



"""
Análisis de la interacción (comentarios)
"""
def getDays(videoDate, commentDate):
	lst = []
	for video, comment in zip(videoDate, commentDate):
		d1 = video
		d2 = comment.split('T')[0]
		delta = datetime.strptime(d2, '%Y-%m-%d') - datetime.strptime(d1, '%Y-%m-%d')
		lst.append(delta.days)
	return lst

def getDaysRange(deltaDays):

	if deltaDays == 0:
		return 'Same day'
	elif deltaDays == 1:
		return 'Next day'
	elif deltaDays >= 2 and deltaDays <= 7:
		return '2-7 days'
	elif deltaDays > 7 and deltaDays <= 30:
		return '1-4 weeks'
	elif deltaDays > 30 and deltaDays <= 365:
		return '1 month - 1 year'
	else:
		return '+1 year'


df['days_since_published'] = getDays(df['video_published_at_day'].astype(str).values, df['comment_publishedAt'].astype(str).values)

df['days_since_published_range'] = df['days_since_published'].apply(getDaysRange)

# Tiempo promedio para comentarios
mean_comment_time = df[df['days_since_published'] >= 0].groupby(['video_id'])['days_since_published'].mean()
# ¿Cuánto tiempo después de publicado un video sigue recibiendo comentarios?
max_comment_time = df[df['days_since_published'] >= 0].groupby(['video_id'])['days_since_published'].max()

print('\n*** Mean comment time ***')
print(mean_comment_time.describe().round(2))
print('\n*** Max comment time ***')
print(max_comment_time.describe().round(2))

## Cifras de la grafica
print('\n*** Tiempo entre la publicación del video y los comentarios ***')
print(df['days_since_published_range'].value_counts(normalize=True))


plt.figure(figsize=(10, 5))
sns.countplot(x='days_since_published_range', data=df, stat='percent', order=['Same day', 'Next day', '2-7 days', '1-4 weeks', '1 month - 1 year', '+1 year'],  palette='Dark2')
# plt.title('Time between video posting and comments')
plt.xlabel('Days after publication')
plt.ylabel('Frequency of comments (%)')
plt.gca().yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100.0, decimals=1, symbol=' %'))
# plt.show()
plt.savefig(r'..\Plots\3_comments_interaction_days.pdf', bbox_inches='tight', dpi=300)


# ¿Los videos virales generan conversación durante más tiempo?
columns = ['video_id', 'video_total_views', 'video_total_likes', 'video_total_comments']
temp3 = df[columns].drop_duplicates(subset='video_id')

# obtener maximo de dias por video
maxDf = df.groupby(['video_id'])['days_since_published'].max().reset_index(name='max_comment_days')

temp3 = pd.merge(left=temp3, right=maxDf, on='video_id', how='left')

viral_threshold = temp3['video_total_views'].quantile(0.75)  # Cuartil superior = videos virales

viral_vs_non_viral = temp3.groupby(temp3['video_total_views'] > viral_threshold)['max_comment_days']

print(f'\n*** Viral_threshold: {viral_threshold:,.2f}')
print(f'** Tiempo (dias) de conversación en videos virales vs. no virales:\n{viral_vs_non_viral.describe().round(2)}')




"""
Distribución de Likes en Comentarios
"""

# ¿Qué porcentaje de comentarios recibe likes?
percent_comments_with_likes = (df['comment_likeCount'] > 0).mean() * 100

# ¿Cuál es la cantidad promedio de likes por comentario?
average_likes_per_comment = df['comment_likeCount'].mean()
std_likes_per_comment = df['comment_likeCount'].std()

print(f'\n*** Porcentaje de comentarios que reciben likes: {percent_comments_with_likes:.2f}%')
print(f'** Promedio de likes por comentario: {average_likes_per_comment:.2f}')
print(f'** Std de likes por comentario: {std_likes_per_comment:.2f}')

maxi = df['comment_likeCount'].max()
print(f'\n*** Comentario con más likes: {maxi:,d}')
print([f'{x}: {y}\n' for x, y in zip(df.columns, df[df['comment_likeCount'] == maxi].values)])
