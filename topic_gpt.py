import pandas as pd
import os
import tiktoken 
import json




def readCsv(modelName):

	topicInfo = pd.read_csv(os.path.join(r'..\Topic Modeling', f'{modelName.upper()}', f'{modelName}_topic_info.csv'), index_col=0) # usecols=['Representation', 'Representative_Docs']
	topicInfo = topicInfo[topicInfo['Topic'] >= 0].drop(['Count', 'Name'], axis=1)


	data = pd.read_csv(r'..\Dataset\7_Data_final\final_dataset.csv', usecols=['id', 'channel_title'])
	data = data[~data['channel_title'].isin(['CNN en Español', 'Noticias Telemundo'])]

	print(f'FINAL dataset: {data.shape[0]:,d}')

	commentsData = pd.read_csv(os.path.join(r'..\Dataset\9_Data_topics', 'comments_topicNEW.csv'), usecols=['id', 'texto', 'texto_lemma'])
	
	commentsData = commentsData[commentsData['id'].isin(data['id'])]
	
	print(f'CommentsData: {commentsData.shape[0]:,d}')


	finalComments = []
	finalIds = []

	for nTopic, docs in zip(topicInfo['Topic'].values, topicInfo['Representative_Docs'].values):

		print(f'*** Topic {nTopic} ***')

		lstComments = []
		lstIds = []

		for comment in docs.split(','):
			comment = comment.replace("[", "").replace("]", "").replace("'", "").strip()
			
			filterComment = commentsData[commentsData['texto_lemma'] == comment]

			if filterComment.shape[0] != 0:
				
				originalText = filterComment['texto'].values.tolist()[0]
				originalId = filterComment['id'].values.tolist()[0]

				lstComments.append(originalText)
				lstIds.append(originalId)

		finalComments.append(lstComments)
		finalIds.append(lstIds)
	

	finalData = topicInfo[['Topic', 'Representation']]
	finalData['Representative_Docs'] = finalComments
	finalData['Ids_Docs'] = finalIds

	print(finalData.columns)
	print(finalData.shape)

	orderCols = ['Topic', 'Representation', 'Ids_Docs', 'Representative_Docs']
	finalData[orderCols].to_csv(os.path.join(r'..\Topic Modeling', f'{modelName.upper()}', f'{modelName}_info_EDITED.csv'), index=False)



def createMessage(keywords, repr_docs):

	repr_docs = [x.replace("[", "").replace("]", "").replace("'", "").strip() for x in repr_docs.split(',')]

	delimiter = '####'

	system_message = 'You are a helpful assistant. Your task is to analyse comments from YouTube, related to news in Mexico in 2024.'

	user_message = f'''I have a topic that contains the following documents delimited with {delimiter}. The topic is described by the following keywords: {keywords}.
Based on the information above, extract a short topic label and description in a JSON format:
{{"topic_name": "<topic>", "topic_description": "<topic_description>"}}

Comments:
{delimiter}
{delimiter.join(repr_docs)}
{delimiter}'''

	messages = '[{\"role\": \"system", "content": system_message}, {"role": "user", "content": f"{user_message}"}]'

	return messages

def madePropts(destinyDirectory, modelName, gptVersion='gpt-4o-mini'):

	df = pd.read_csv(os.path.join(r'..\Topic Modeling', f'{modelName.upper()}', f'{modelName}_info_EDITED.csv'))

	requestsLst = []
	for nTopic, keywords, docs in zip(df['Topic'], df['Representation'], df['Representative_Docs']):

		message = createMessage(keywords, docs)

		custom_id = f'topic_{nTopic}'

		prompt = f"{{\"custom_id\": \"{custom_id}\", \"method\": \"POST\", \"url\": \"/v1/chat/completions\", \"body\": {{\"model\": \"{gptVersion}\", \"messages\": {message}, \"max_tokens\": 50}}}}"
		requestsLst.append(prompt)
	

	# finalFilename = os.path.join(destinyDirectory, f'gpt_topic_{modelName}.jsonl')
	# with open(finalFilename, 'w') as file:
	# 	for line in requestsLst:
	# 		file.write(line)  # Adding the line to the text.txt  
	# 		file.write('\n')  # Adding a new line character  



def procesarTopicGpt(modelName):

	filename = open(os.path.join(r'..\Topic Modeling', f'{modelName.upper()}', f'gpt_topic_{modelName}_100tokens_output.jsonl'), 'r')
	lines = filename.readlines()

	topicos = []
	for line in lines:
			
		json_object = json.loads(line)

		userID = json_object['custom_id']
		response = json_object['response']['body']['choices'][0]['message']['content'].replace("```json", "").replace("```", "").replace('\n', '').strip()

		if not response.endswith('"') and not response.endswith('}'):
			response = response + '"}'
		elif response.endswith('"'):
			response = response + '}'
		else:
			pass
		
		
		jsonResponse = json.loads(response)
		topicName = jsonResponse['topic_name']
		topicDecr = jsonResponse['topic_description']
		
		topicos.append((userID, topicName, topicDecr))
	

	# finalTopicos = pd.DataFrame(data=topicos, columns=['topic', 'topic_name', 'topic_description'])
	# finalTopicos.to_csv(os.path.join(r'..\Topic Modeling', f'{modelName.upper()}', f'topic_{modelName}_description-gpt_100tokens.csv'), index=False)



# gpt4_enc = tiktoken.encoding_for_model("gpt-4")

# def get_tokens(enc, text):
# 	return list(map(lambda x: enc.decode_single_token_bytes(x).decode('utf-8'), 
# 				  enc.encode(text)))

# x = get_tokens(gpt4_enc, 'topic_name: "room cleanliness", topic_description: "The size of the room is mentioned, with some reviews describing them as spacious and others as small."')
# print(len(x))




### ===================================================
# modelName = 'modelo6'
# readCsv(modelName)


# destinyDirectory = r'D:\Elizabeth\Posdoc - News\Topic Modeling\Modelo6'
# modelName = 'modelo6'
# madePropts(destinyDirectory, modelName)


# modelName = 'modelo6'
# procesarTopicGpt(modelName)

