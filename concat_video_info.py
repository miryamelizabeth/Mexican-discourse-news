import pandas as pd
import os
import uuid



def concatenar_info_comments(sourceDirectoryVideo, sourceDirectoryComments, destinyDirectory):
    
	## Leer videos info
	videosDf = pd.read_csv(os.path.join(sourceDirectoryVideo, f'info_videos.csv'))
	videosDf['video_descriptionClean'].fillna('No disponible', inplace=True)

	## Leer comentarios
	commentsDf = pd.read_csv(os.path.join(sourceDirectoryComments, f'comments_videos_final.csv')).drop(['index', 'comment_lang', 'comment_words', 'comment_chars'], axis=1)

	## Concatenar
	mergeDf = pd.merge(left=commentsDf, right=videosDf, on='video_id', how='left')

	## Eliminar vacios
	tempDf = mergeDf.dropna()

	## Quedarse solo con comentarios arriba de 10
	countDf = tempDf.groupby(['video_id'])['video_id'].count().reset_index(name='count')

	idsList = countDf[countDf['count'] >= 10]['video_id'].values.tolist()

	finalDf = tempDf[tempDf['video_id'].isin(idsList)]

	print(f'\nVIDEOO')
	print(f'{videosDf.shape[0]:,d}')
	print(videosDf.isnull().sum().sum())

	print(f'\nCOMENARIO')
	print(f'{commentsDf.shape[0]:,d}')
	print(commentsDf.isnull().sum().sum())

	print(f'\nMERGE')
	print(f'{mergeDf.shape[0]:,d}')
	print(mergeDf.isnull().sum().sum())
	
	print(f'\nTEMP')
	print(f'{tempDf.shape[0]:,d}')
	print(tempDf.isnull().sum().sum())

	print(f'\nfinalDf')
	print(f'{finalDf.shape[0]:,d}')
	print(finalDf.isnull().sum().sum())


	## Generar IDs por instancia
	lst = [str(uuid.uuid4()) for _ in range(finalDf.shape[0])]
	instanceIDlst = [f'{x.split("-")[0].lower()}{x.split("-")[1].lower()}' for x in lst]

	finalDf['id'] = instanceIDlst


	## Guardar
	print(f'\nGuardando...')

	columns = ['id', 'video_id', 'channel_title', 'video_published_at_day', 'video_published_at_hour',
       'video_duration_format', 'video_duration_hour', 'video_duration_minutes', 'video_duration_seconds',
	   'video_total_views', 'video_total_likes', 'video_total_comments',
	   'video_titleClean', 'video_descriptionClean',
	   'comment_authorChannelId', 'comment_textClean',
       'comment_likeCount', 'comment_publishedAt', 'comment_updatedAt']
	
	finalDf[columns].to_csv(os.path.join(destinyDirectory, f'final_dataset.csv'), index=False)





### ==============================================
sourceDirectoryVideo = r'..\Dataset\6_Data_seed_videos_info_preprocessed_final'
sourceDirectoryComments = r'..\Dataset\5_Data_video_comments_preprocessed_final'
destinyDirectory = r'..\Dataset\7_Data_final'

concatenar_info_comments(sourceDirectoryVideo, sourceDirectoryComments, destinyDirectory)
