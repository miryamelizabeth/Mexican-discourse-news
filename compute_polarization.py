import pandas as pd
import os
import matplotlib.pyplot as plt


# 1. Cargar los datos
data = pd.read_csv(r'..\Dataset\7_Data_final\final_dataset.csv', parse_dates=['video_published_at_day'])

topic = pd.read_csv(r'..\Topic Modeling\Modelo6\topic_modelo6_distribution.csv')

sentiment = pd.read_csv(r'..\Dataset\8_Data_attributes\sentiment_comments.csv').drop(['video_id'], axis=1)
emotion = pd.read_csv(r'..\Dataset\8_Data_attributes\emotions_comments.csv').drop(['video_id'], axis=1)
hate = pd.read_csv(r'..\Dataset\8_Data_attributes\hate_speech_comments.csv').drop(['video_id'], axis=1)

data['Topic'] = topic['Topic']
data['Topic Name'] = topic['Topic Name']

other1 = pd.merge(left=sentiment, right=emotion, on='id', how='left').merge(right=hate, on='id', how='left')

df = pd.merge(left=data, right=other1, on='id', how='left')
print(f'\n*** TOTAL DATASET: {df.shape[0]:,d}\n')

df = df[~df['Topic'].isin([-1, 17, 46, 47])]
print(f'\n*** TOTAL DATASET: {df.shape[0]:,d}\n')



sentCols = ['Positive', 'Negative', 'Neutral'] + ['sentiment_tag']
emoCols = ['Joy', 'Anger', 'Sadness', 'Disgust', 'Surprise', 'Fear'] + ['emotion_tag']
hateCols = ['Hateful'] + ['hateful_tag']
aggrCols = ['Aggressive'] + ['aggressive_tag']




"""
1. SENTIMIENTO
Sentimientos mas polarizantes
"""
print(f'\n*** SENTIMIENTO ***')

# Primero, calculamos la distribución de sentimientos por tópico
sentiment_counts = df.groupby(['Topic', 'Topic Name', 'sentiment_tag']).size().unstack(fill_value=0)

# Asegurar que todas las columnas estén presentes
for col in ['Positive', 'Negative', 'Neutral']:
	if col not in sentiment_counts.columns:
		sentiment_counts[col] = 0

# Calculamos proporciones
sentiment_props = sentiment_counts.div(sentiment_counts.sum(axis=1), axis=0)

# Definir el índice de polarización
sentiment_props['polarization_index'] = 1 - (sentiment_props['Positive'] - sentiment_props['Negative']).abs() - sentiment_props['Neutral']

topSenti = sentiment_props.sort_values('polarization_index', ascending=False).reset_index()

## Guardando...
order = ['Topic', 'Topic Name'] + ['polarization_index'] + ['Positive', 'Negative', 'Neutral']
topSenti[order].to_csv(r'..\Plots\7_Topicos_polarizantes\sentiment_polarization_index.csv', index=False)



"""
HATE
"""
print(f'\n*** HATE ***')

# Primero, calculamos la distribución de hate por tópico
hate_counts = df.groupby(['Topic', 'Topic Name', 'hateful_tag']).size().unstack(fill_value=0)

# Asegurar que todas las columnas estén presentes
for col in ['Hateful', 'Non-hateful']:
	if col not in hate_counts.columns:
		hate_counts[col] = 0

# Calculamos proporciones
hate_props = hate_counts.div(hate_counts.sum(axis=1), axis=0)

# Definir el índice de polarización
hate_props['polarization_index'] = 1 - (hate_props['Hateful'] - hate_props['Non-hateful']).abs()

topHate = hate_props.sort_values('polarization_index', ascending=False).reset_index()

## Guardando...
order = ['Topic', 'Topic Name'] + ['polarization_index'] + ['Hateful', 'Non-hateful']
topHate[order].to_csv(r'..\Plots\7_Topicos_polarizantes\hate_polarization_index.csv', index=False)



"""
AGGRESSION
"""
print(f'\n*** AGGRESSION ***')

# Primero, calculamos la distribución de agresion por tópico
aggression_counts = df.groupby(['Topic', 'Topic Name', 'aggressive_tag']).size().unstack(fill_value=0)

# Asegurar que todas las columnas estén presentes
for col in ['Aggressive', 'Non-aggressive']:
	if col not in aggression_counts.columns:
		aggression_counts[col] = 0

# Calculamos proporciones
aggression_props = aggression_counts.div(aggression_counts.sum(axis=1), axis=0)

# Definir el índice de polarización
aggression_props['polarization_index'] = 1 - (aggression_props['Aggressive'] - aggression_props['Non-aggressive']).abs()

topAggression = aggression_props.sort_values('polarization_index', ascending=False).reset_index()

## Guardando...
order = ['Topic', 'Topic Name'] + ['polarization_index'] + ['Aggressive', 'Non-aggressive']
topAggression[order].to_csv(r'..\Plots\7_Topicos_polarizantes\aggression_polarization_index.csv', index=False)
