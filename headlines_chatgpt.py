import pandas as pd
import os
import json



def tagHeadlines(model):

	print(f'* Reading files...')

	dataset = pd.read_csv('headlines.csv')

	requestsLst = []
	idLst = dataset['video_id'].values
	textLst = dataset['texto'].values

	for iD, headline in zip(idLst, textLst):

		prompt = f"Classify the news headline as Politics, Economy, Society, Sports, Entertainment, Science-Technology, Culture, National or International. Only select one option. \\\"\\\"{headline}\\\"\\\""

		message = f"{{\"custom_id\": \"{iD}\", \"method\": \"POST\", \"url\": \"/v1/chat/completions\", \"body\": {{\"model\": \"{model}\", \"messages\": [{{\"role\": \"user\", \"content\": \"{prompt}\"}}], \"max_tokens\": 10}}}}"

		requestsLst.append(message)

	
	finalFilename = f'label_headlines.jsonl'
	with open(finalFilename, 'w') as file:  
		for line in requestsLst:
			file.write(line)  # Adding the line to the text.txt  
			file.write('\n')  # Adding a new line character  

	print('FIN!!! :)')


def procesarTagHeadlines():
	
	todo = []

	filename = open(r'..\batch_output.jsonl', 'r')
	lines = filename.readlines()

	for line in lines:
			
		json_object = json.loads(line)
		videoID = json_object['custom_id']
		response = json_object['response']['body']['choices'][0]['message']['content']
		
		todo.append((videoID, response))

	df = pd.DataFrame(todo, columns=['video_id', 'type_headline'])
	print(df['type_headline'].value_counts())

	df.to_csv('headlines_result.csv', index=False)





### ==============================================
model = 'MODEL'
tagHeadlines(model)

procesarTagHeadlines()
