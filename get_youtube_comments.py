"""
Informacion:
https://developers.google.com/youtube/v3/docs/commentThreads
"""

import pandas as pd
import os
import time
import datetime

from googleapiclient.discovery import build


# ===============================
API_KEY = 'API_KEY'

# YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)



def read_video_ids(csv_filename):
	'''
	Reads video IDs from a CSV file.
	Assumes the CSV file has a column named 'video_id'.
	'''
	df = pd.read_csv(csv_filename)
	return df['video_id'].tolist()


def get_video_comments(video_id, max_comments=500):
	'''
	Retrieve the first `max_comments` comments from a YouTube video.
	'''
	comments = []
	next_page_token = None

	while len(comments) < max_comments:

		request = youtube.commentThreads().list(
			part='snippet',
			videoId=video_id,
			maxResults=min(100, max_comments - len(comments)),  # Fetch remaining comments (100 per default maximum)
			pageToken=next_page_token
		)
		response = request.execute()

		for item in response.get('items', []):
			comment_snippet = item['snippet']['topLevelComment']['snippet']

			# Extract comment data
			comment = {
					'video_id': video_id,
					'comment_authorDisplayName': comment_snippet.get('authorDisplayName'),
					'comment_authorChannelId': comment_snippet.get('authorChannelId', {}).get('value', ''),
					'comment_textDisplay': comment_snippet.get('textDisplay'),
					'comment_textOriginal': comment_snippet.get('textOriginal'),
					'comment_likeCount': comment_snippet.get('likeCount', 0),
					'comment_publishedAt': comment_snippet.get('publishedAt'),
					'comment_updatedAt': comment_snippet.get('updatedAt')
				}
			comments.append(comment)

		next_page_token = response.get('nextPageToken')
		if not next_page_token:
			break  # Stop if no more pages available

		time.sleep(3)  # Sleep to avoid hitting rate limits

	return comments



def obtener_comentarios(sourceDirectory, filenameInfo, destinyDirectory):

	print(f'\n\n============================')
	print(f'Starting...')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
	print(f'============================\n')


	input_csv = os.path.join(sourceDirectory, f'{filenameInfo}.csv')  # CSV file containing video IDs
	video_ids = read_video_ids(input_csv)
	total_videos = len(video_ids)

	print(f'Total Results: {total_videos}')


	finalDf = pd.DataFrame()
	for i, video_id in enumerate(video_ids):
		
		print(f'{i+1}) Fetching comments for video: {video_id}')
		video_comments = get_video_comments(video_id)

		df = pd.DataFrame(video_comments)

		finalDf = pd.concat([finalDf, df])

		if (i + 1) % 10 == 0:
			print(f'** Procesando {i+1}/{total_videos}...')


	print('\nGuardando...')
	finalDf.to_csv(os.path.join(destinyDirectory, f'comments_{filenameInfo}.csv'), index=False)
	print('\nComments saved successfully!')





## ===============================================================
## Obtener comentarios de los videos
api_key = 'API_KEY'
sourceDirectory = r'..\Dataset\3_Data_seed_videos_info'
destinyDirectory = r'..\Dataset\4_Data_video_comments'
filenameInfo = 'videos_elegidos.csv'

obtener_comentarios(sourceDirectory, filenameInfo, destinyDirectory)
