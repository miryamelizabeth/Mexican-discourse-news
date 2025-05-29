"""
Información:
https://developers.google.com/youtube/v3/docs/playlistItems#contentDetails.videoPublishedAt
"""

import pandas as pd
import os
import time
import datetime

from googleapiclient.discovery import build



# Function to get playlist videos
def get_playlist_videos(api_key, playlist_id, directory, filename):

	print(f'\n\n**********************************************')
	print(f'OBTENIENDO VIDEOS DE PLAYLIST: {playlist_id}')
	print(f'Filename: {filename}')
	print(f'**********************************************')

	youtube = build('youtube', 'v3', developerKey=api_key)
	videos = []
	next_page_token = None
	
	contar = 1
	while True:
		request = youtube.playlistItems().list(
			part='snippet,contentDetails',
			playlistId=playlist_id,
			maxResults=50,  # Maximum allowed per request
			pageToken=next_page_token
		)
		response = request.execute()

		total_results = response['pageInfo']['totalResults']
		print(f'{contar}/{total_results//50} Total Results: {total_results}')
		print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
		
		for item in response['items']:
			
			playlist_item_id = item['id']
			playlist_item_etag = item['etag']

			video_id = item['contentDetails']['videoId']
			try:
				video_published_at = item['contentDetails']['videoPublishedAt']
			except Exception as e:
				video_published_at = ''

			channel_id = item['snippet']['channelId']
			channel_title = item['snippet']['channelTitle']

			video_title = item['snippet']['title']
			video_description = item['snippet']['description']
			
			
			videos.append([channel_id, channel_title, playlist_item_id, playlist_item_etag, video_id, video_published_at, video_title, video_description])


		next_page_token = response.get('nextPageToken')
		if not next_page_token:
			break

		contar += 1
		time.sleep(5)
	

	## Guardando videos...
	print(f'Guardando...')
	df = pd.DataFrame(data=videos, columns=['channel_id', 'channel_title', 'playlist_item_id', 'playlist_item_etag', 'video_id', 'video_published_at', 'video_title', 'video_description'])
	
	print(df.head())

	df.to_csv(os.path.join(directory, filename), index=False)

	print(f'\n\n---> END! :) <---\n\n')



def filtrar_videos_año(sourceDirectory, destinyDirectory, year):

	finalDf = pd.DataFrame()
	
	lstFiles = os.listdir(sourceDirectory)

	total = len(lstFiles)
	print(f'Total: {total}')

	for i, filename in enumerate(lstFiles, start=1):

		print(f'\n*** {i} - {filename} ***')

		df = pd.read_csv(os.path.join(sourceDirectory, filename))

		filterDf = df[(df['video_published_at'].str.startswith(year)) & (df['video_title'] != 'Private video') & (df['video_title'] != 'Deleted video')]
		
		finalDf = pd.concat([finalDf, filterDf])

		print(f'Antes: {df.shape[0]}\tDespues: {filterDf.shape[0]}')


	print(f'\nGuardando...')
	print(finalDf.shape)
	finalDf.to_csv(os.path.join(destinyDirectory, f'videos_{year}.csv'), index=False)

	print(f'\n\n---> END! :) <---\n\n')



def get_video_details(api_key, video_ids):
	
	youtube = build('youtube', 'v3', developerKey=api_key)

	request = youtube.videos().list(
		part='snippet,contentDetails,statistics',
		id=video_ids
	)

	response = request.execute()
	
	video_details = []
	
	for item in response.get('items', []):
		try:
			video_info = {
				'video_id': item['id'],
				'video_title': item['snippet']['title'],
				'channel_title': item['snippet']['channelTitle'],
				'video_published_at': item['snippet']['publishedAt'],
				'video_duration': item['contentDetails']['duration'],
				'video_total_views': item['statistics'].get('viewCount', 'N/A'),
				'video_total_likes': item['statistics'].get('likeCount', 'N/A'),
				'video_total_comments': item['statistics'].get('commentCount', 'N/A')
			}
		except Exception as e:
			video_info = {
				'video_id': item['id'],
				'video_title': '',
				'channel_title': '',
				'video_published_at': '',
				'video_duration': '',
				'video_total_views': '',
				'video_total_likes': '',
				'video_total_comments': ''
			}
		
		video_details.append(video_info)
	
	return video_details



def get_all_info_videos(api_key, sourceDirectory, destinyDirectory, year, start_index, end_index):

	print(f'\n\n**********************************************')
	print(f'OBTENIENDO INFO VIDEOS: [{start_index} - {end_index}]')
	print(f'API_KEY: {api_key}')
	print(f'**********************************************')


	df = pd.read_csv(os.path.join(sourceDirectory, f'videos_{year}.csv'))

	video_ids = df['video_id'].values.tolist()[start_index:end_index]
	total_videos = len(video_ids)

	print(f'\nTotal Videos: {total_videos}')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')


	finalDf = pd.DataFrame()

	for i in range(0, total_videos, 5):

		print(f'{i}')

		lst_ids = video_ids[i:i+5]

		videos_info = get_video_details(api_key, lst_ids)

		videoDf = pd.DataFrame(videos_info)
		finalDf = pd.concat([finalDf, videoDf])

		time.sleep(5)


	## Guardando videos...
	print(f'\n\nGuardando...')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
	
	print(finalDf.head())

	horaFinal = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
	finalDf.to_csv(os.path.join(destinyDirectory, f'videos-info_{start_index}-{end_index}_{horaFinal}.csv'), index=False)

	print(f'\n\n---> END! :) <---\n\n')





# ===============================================================
# Obtener lista de videos de las playlists

api_key = 'API_KEY'
directory = r'..\Dataset\1_Data_playlist'


playlist_id = 'PLmZsiRvDGLteHyT2dtOlEtuwfeZwYw5H0'
filename = 'nmas_mexico.csv'

# playlist_id = 'PLRzDietc_2Kh2AdNYy66kxUZxfaDLHwjH'
# filename = 'milenio_mexico.csv'

# playlist_id = 'PLRzDietc_2KhFD0TIjfxlnAIQOn6Mu6Pd'
# filename = 'milenio_cdmx.csv'

# playlist_id = 'PL8sO_uk4FP01SVQweKbAPy8S8NztNFiaG'
# filename = 'adn40_noticias2024.csv'

get_playlist_videos(api_key, playlist_id, directory, filename)





# ===============================================================
# Filtrar videos por año y que no sean privados/eliminados
sourceDirectory = r'..\Dataset\1_Data_playlist'
destinyDirectory = r'..\Dataset\2_Data_seed_videos'
year = '2024'

filtrar_videos_año(sourceDirectory, destinyDirectory, year)





# ===============================================================
# Obtener stats de los videos
api_key = 'API_KEY'
sourceDirectory = r'..\Dataset\2_Data_seed_videos'
destinyDirectory = r'..\Dataset\3_Data_seed_videos_info'
year = 2024
get_all_info_videos(api_key, sourceDirectory, destinyDirectory, year, 0, -1)
