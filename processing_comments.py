import pandas as pd
import os
import re
import emoji
import unicodedata
import datetime

from langdetect import detect

from nltk.tokenize import TweetTokenizer

  
# Create a reference variable for Class TweetTokenizer 
tk = TweetTokenizer() 



# -------------------------------------
def removePunctuation(text):
	""" Removes all puntuctuation symbols including ¿! (used in spanish) """

	punctuationStr = r'[:\.,\?!/\\_━🇧▪"\[!"\$%&\(\)\*\+;<=>\^`{\|}~¿¡¬‘’¶£¥€¢₩°«»“”—´¨™©º¸•¤‹›×–…·ا\]]'

	text = re.sub(punctuationStr, ' ', text)

	return re.sub(' +', ' ', text).strip()


def removeUrls(text):

	urlStr = r'https?:\/\/(www\.)?[\w.-]+(\/[\w\-?=&$@%.#]*)+'
	text = re.sub(urlStr, ' ', text)

	urlStr = r':\/\/(www\.)?[\w.-]+(\/[\w\-?=&$@%.#]*)+'
	text = re.sub(urlStr, ' ', text)

	urlStr = r'\w+\=\w+'
	text = re.sub(urlStr, ' ', text)

	return re.sub(' +', ' ', text).strip()


def helper_preprocess(text):

	user_regex = re.compile(r"@[a-zA-Z0-9_]{0,15}")
	text = user_regex.sub('@USER', text)


	shorten = 3
	repeated_regex = re.compile(r"(.)" + r"\1" * (shorten-1) + "+")
	text = repeated_regex.sub(r"\1"*shorten, text)


	letter_regex = re.compile(r'[Aa]{3,}')
	text = letter_regex.sub('a', text)

	letter_regex = re.compile(r'[Bb]{3,}')
	text = letter_regex.sub('b', text)

	letter_regex = re.compile(r'[Cc]{3,}')
	text = letter_regex.sub('c', text)

	letter_regex = re.compile(r'[Dd]{3,}')
	text = letter_regex.sub('d', text)

	letter_regex = re.compile(r'[Ee]{3,}')
	text = letter_regex.sub('e', text)

	letter_regex = re.compile(r'[Ff]{3,}')
	text = letter_regex.sub('f', text)

	letter_regex = re.compile(r'[Gg]{3,}')
	text = letter_regex.sub('g', text)

	letter_regex = re.compile(r'[Hh]{3,}')
	text = letter_regex.sub('h', text)

	letter_regex = re.compile(r'[Ii]{3,}')
	text = letter_regex.sub('i', text)

	letter_regex = re.compile(r'[Jj]{3,}')
	text = letter_regex.sub('j', text)

	letter_regex = re.compile(r'[Kk]{3,}')
	text = letter_regex.sub('k', text)

	letter_regex = re.compile(r'[Ll]{3,}')
	text = letter_regex.sub('l', text)

	letter_regex = re.compile(r'[Mm]{3,}')
	text = letter_regex.sub('m', text)

	letter_regex = re.compile(r'[Nn]{3,}')
	text = letter_regex.sub('n', text)

	letter_regex = re.compile(r'[Oo]{3,}')
	text = letter_regex.sub('o', text)

	letter_regex = re.compile(r'[Pp]{3,}')
	text = letter_regex.sub('p', text)

	letter_regex = re.compile(r'[Qq]{3,}')
	text = letter_regex.sub('q', text)

	letter_regex = re.compile(r'[Rr]{3,}')
	text = letter_regex.sub('r', text)

	letter_regex = re.compile(r'[Ss]{3,}')
	text = letter_regex.sub('s', text)

	letter_regex = re.compile(r'[Tt]{3,}')
	text = letter_regex.sub('t', text)

	letter_regex = re.compile(r'[Uu]{3,}')
	text = letter_regex.sub('u', text)

	letter_regex = re.compile(r'[Vv]{3,}')
	text = letter_regex.sub('v', text)

	letter_regex = re.compile(r'[Ww]{3,}')
	text = letter_regex.sub('w', text)

	letter_regex = re.compile(r'[Xx]{3,}')
	text = letter_regex.sub('x', text)

	letter_regex = re.compile(r'[Yy]{3,}')
	text = letter_regex.sub('y', text)

	letter_regex = re.compile(r'[Zz]{3,}')
	text = letter_regex.sub('z', text)


	laughter_regex = re.compile('[ja][ja]+aj[ja]+')
	replacement = 'jaja'

	text = laughter_regex.sub(replacement, text)


	laughter_regex = re.compile('[ha][ha]+ah[ha]+')
	replacement = 'haha'

	text = laughter_regex.sub(replacement, text)


	hour_regex = re.compile(r'([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]')
	text = hour_regex.sub(' ', text)

	hour_regex = re.compile(r'([01]?[0-9]|2[0-3]):[0-5][0-9]')
	text = hour_regex.sub(' ', text)


	numbers_regex = re.compile(r'\d+\.?\d+')
	text = numbers_regex.sub(' ', text)

	numbers_regex = re.compile(r'\d+:\d+')
	text = numbers_regex.sub(' ', text)

	numbers_regex = re.compile(r'\d+-\d+-?')
	text = numbers_regex.sub(' ', text)


	text = text.replace(" ' ", " ").replace("' ", " ").replace(" '", " ").replace('hashtag', '').replace('http', '').replace('url', '').replace('nbsp', '').replace('\\', '-')


	return re.sub(' +', ' ', text).strip()


def process_palabras_guiones(text):

	lines = []
	with open('lista_guiones.txt', 'r', encoding='utf-8') as file:
		lines = file.readlines()
	
	lines = [l.replace('\n', '').lower() for l in lines]

	final = ' '.join([w.replace('-', '') if w.lower() in lines else w for w in tk.tokenize(text)])

	return final


def corregir_palabras(text):

	df1 = pd.read_csv('lista_cambios.txt')
	dictionary1 = dict(zip(df1['palabra'].str.lower(), df1['nueva_palabra'].str.lower()))

	listaWords = []
	for w in tk.tokenize(text):
		w = w.replace('GROSERIA', '*')
		if w.lower() in dictionary1:
			w = dictionary1[w.lower()]
		listaWords.append(w)

	final = ' '.join(listaWords)

	return final


def corregir_palabras2(text):
	
	df2 = pd.read_csv('lista_cambios2.txt', encoding='utf-8')
	dictionary2 = dict(zip(df2['palabra'].str.lower(), df2['nueva_palabra'].str.lower()))

	for old, new in dictionary2.items():
		text = text.lower().replace(old, new)

	return text



def remove_emojis_symbos_unicode(texto, traducir_emojis=False):
	"""
	Limpia el texto eliminando caracteres especiales, emojis y texto con estilos inusuales.
	Opcionalmente traduce emojis a palabras.
	
	Args:
		texto (str): Comentario a limpiar.
		traducir_emojis (bool): Si es True, convierte los emojis en palabras.

	Returns:
		str: Texto limpio.
	"""

	# Opcionalmente traducir emojis a palabras
	if traducir_emojis:
		texto = emoji.demojize(texto, language='es')  # Traduce emojis a palabras en español

	# Normalizar caracteres Unicode para eliminar estilos raros (𝙳 → D, 𝚗 → n, etc.)
	texto = ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))

	# Eliminar emojis y banderas Unicode con una expresión regular
	texto = re.sub(r'[\U0001F1E6-\U0001F1FF\U0001F300-\U0001F9FF]', '', texto)

	# Eliminar caracteres especiales y símbolos raros
	texto = re.sub(r'[^\w\s,.¡!¿?]', '', texto, flags=re.UNICODE)

	# Eliminar espacios extra
	texto = re.sub(r'\s+', ' ', texto).strip()
	
	return texto


def cleanFinal(text):
	final = text.replace(" '", " ").replace("' ", " ").replace(" '' ", " ").replace(" ' ", " ").replace("#", "").replace(' x q ', ' por que ').replace(' x eso ', ' por eso ')
	return re.sub(' +', ' ', final).strip()


# -------------------------------------
def processText(allText, traducir_emojis=False):
	""" Cleans all the garbage in the text and returns the cleaned text """

	## Remove extra newlines
	print(f'\n> Remove extra newlines')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')
	
	allText = [re.sub(r'[\r|\n|\r\n]+', ' ', str(t)) for t in allText]


	## Remove extra whitespace
	print(f'\n> Remove extra whitespace')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [re.sub(' +', ' ', t).strip() for t in allText]


	## Remove extra tabs
	print(f'\n> Remove extra tabs')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [t.replace('\t', ' ').replace('&nbsp', ' ').replace('nbsp', ' ') for t in allText]


	## Replace symbols (eg. I’m --> I'm   that´s --> that's)
	print(f'\n> Replace symbols')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [re.sub('’', '\'', t) for t in allText]
	allText = [re.sub('”', '\'', t) for t in allText]
	allText = [re.sub('´', '\'', t) for t in allText]
	allText = [re.sub('"', '\'', t) for t in allText]

	allText = [re.sub('‑', '-', t) for t in allText]
	allText = [re.sub('—', '-', t) for t in allText]


	## Replace accents
	allText = [re.sub('á|Á|ä|Ä', 'a', t) for t in allText]
	allText = [re.sub('é|É|ë|Ë', 'e', t) for t in allText]
	allText = [re.sub('í|Í|ï|Ï', 'i', t) for t in allText]
	allText = [re.sub('ó|Ó|ö|Ö', 'o', t) for t in allText]
	allText = [re.sub('ú|Ú|ü|Ü', 'u', t) for t in allText]
	allText = [t.replace('*', 'GROSERIA') for t in allText]


	## Quitar URLs
	print(f'\n> Remove URLs')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [removeUrls(t) for t in allText]


	## Quitar otras cosas
	print(f'\n> Remove other things')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [helper_preprocess(t) for t in allText]


	## Palabras con guiones
	print(f'\n> Remove scripts')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [process_palabras_guiones(t) for t in allText]


	## Corregir palabras con * (GROSERIA) o guiones
	print(f'\n> Fix some words * - groserias pt1')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [corregir_palabras(t) for t in allText]

	print(f'\n> Fix some words * - groserias pt2')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [corregir_palabras2(t) for t in allText]


	print(f'\n> Puntuation y lo que falta')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')
	
	allText = [removePunctuation(t) for t in allText]

	allText = [remove_emojis_symbos_unicode(t, traducir_emojis) for t in allText]

	allText = [cleanFinal(t) for t in allText]

	allText = [t.lower() for t in allText]

	return allText



def detect_language(text):
	try:
		language = detect(text)
	except:
		language = 'NA'
	
	return language



def procesamiento_comentarios(sourceDirectory, destinyDirectory):
	"""
	* checar comentarios en español
	* num. palabras en el comentario
	"""

	suma = 0
	for file in os.listdir(sourceDirectory):

		print(f'\n\n*** {file} ***')

		df = pd.read_csv(os.path.join(sourceDirectory, file)).drop(['comment_textDisplay'], axis=1).drop_duplicates()
		print(df.shape)

		df['comment_textClean'] = processText(df['comment_textOriginal'].values)
		df['comment_lang'] = [detect_language(comment) for comment in df['comment_textClean']]
		

		finalCols = ['video_id','comment_authorChannelId','comment_textOriginal','comment_textClean','comment_lang','comment_likeCount','comment_publishedAt','comment_updatedAt']

		df[finalCols].to_csv(os.path.join(destinyDirectory, file), index=False)
		
		suma += df.shape[0]
	
	print(f'Total: {suma:,d}')



def obtener_comentarios_final(sourceDirectory, destinyDirectory):
	"""
	* revisar que no haya comentarios duplicados
	* quitar nulos (text original y limpio)
	* quitar nulo en idioma (simbolos raros)
	* revisar los comentarios en español
	"""

	finalDf = pd.DataFrame()

	for file in os.listdir(sourceDirectory):

		print(f'\n\n*** {file} ***')

		df = pd.read_csv(os.path.join(sourceDirectory, file))
		antes = df.shape[0]

		# Eliminar duplicados
		df.drop_duplicates(subset=['comment_authorChannelId', 'comment_textOriginal'], inplace=True)
		
		# Eliminar comentario original nulo
		df.dropna(subset='comment_textOriginal', inplace=True)

		# Eliminar comentario limpio nulo
		df.dropna(subset='comment_textClean', inplace=True)

		# Eliminar idioma nulo
		df.dropna(subset='comment_lang', inplace=True)

		## Solamente en español
		df = df[df['comment_lang'] == 'es']

		finalDf = pd.concat([finalDf, df], axis=0)

			

	print(f'\n\n===============================\n')
	print(f'Guardando...')

	finalDf = finalDf.reset_index(names='index')
	finalDf.to_csv(os.path.join(destinyDirectory, 'comments_videos_final.csv'), index=False)





### ------------------------------------------------------
sourceDirectory = r'..\Dataset\4_Data_video_comments'
finalDirectory = r'..\Dataset\5_Data_video_comments_preprocessed'

procesamiento_comentarios(sourceDirectory, finalDirectory)



sourceDirectory = r'..\Dataset\5_Data_video_comments_preprocessed'
finalDirectory = r'..\Dataset\5_Data_video_comments_preprocessed_final'

obtener_comentarios_final(sourceDirectory, finalDirectory)
