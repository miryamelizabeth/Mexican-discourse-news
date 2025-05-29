import pandas as pd
import os
import re
import emoji
import unicodedata
import datetime

from langdetect import detect

from nltk.tokenize import TweetTokenizer, word_tokenize

from sklearn.feature_extraction.text import CountVectorizer
  
# Create a reference variable for Class TweetTokenizer 
tk = TweetTokenizer() 



def iso8601_to_excel_duration(iso_duration):
	"""
	Example usage:
	iso_duration = 'PT2H30M15S'
	excel_duration = iso8601_to_excel_duration(iso_duration)
	print(excel_duration)  # Output: '02:30:15'
	"""
	
	# Regular expression to extract hours, minutes, and seconds
	match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)

	if match:
		hours = int(match.group(1) or 0)
		minutes = int(match.group(2) or 0)
		seconds = int(match.group(3) or 0)

		# Format the Excel duration as HH:MM:SS
		return f'{hours:02}:{minutes:02}:{seconds:02}'

	else:
		raise ValueError('Invalid ISO 8601 duration format')


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


def remove_otros(texto):

	texto = re.sub(r'adsdsas$', ' ', texto)
	texto = re.sub(r'asad$', ' ', texto)
	texto = re.sub(r'comenta este video y compartelo con tus amigos para mas informacion entra no olvides dejarnos tus comentarios y visitarnos en facebook twitter sitio suscribete a nuestro canal w youtube com channel uclqo4zaaz hqdctlovcgka$', ' ', texto)
	texto = re.sub(r'diciembre de$', ' ', texto)
	texto = re.sub(r'esquivel corte completo$', ' ', texto)
	texto = re.sub(r'mantente siempre informado con las noticias sobre los acontecimientos mas importantes a nivel nacional e internacional excelsior web w excelsior com mx facebook x instagram tiktok$', ' ', texto)
	texto = re.sub(r'mas informacion en h siguenos en nuestras redes sociales para estar enterado de todo fb tw ig$', ' ', texto)
	texto = re.sub(r'mas informacion en siguenos en nuestras redes sociales para estar enterado de todo fb tw ig$', ' ', texto)
	texto = re.sub(r'mas informacion en no olvides seguirnos en nuestras redes sociales para estar enterado de todo fb tw ig$', ' ', texto)
	texto = re.sub(r'mas informacion en no olvides seguirnos en nuestras redes sociales para estar enterado de todo fb tw$', ' ', texto)
	texto = re.sub(r'mas informacion en s heraldodemexico com mx siguenos en nuestras redes sociales para estar enterado de todo fb tw ig$', ' ', texto)
	texto = re.sub(r'mas noticias de el universal suscribete a el universal plus con tu suscripcion a el universal plus tienes acceso a contenidos exclusivos siguenos en facebook twitter google news spotify tiktok instagram$', ' ', texto)
	texto = re.sub(r'nd$', ' ', texto)
	texto = re.sub(r'no quieres perderte de nada suscribete escuchanos en w adn mx adn radio siguenos en todas nuestras redes facebook x instagram tiktok spotify toda la informacion no te pierdas la transmision de noticias adn en vivo mientras otros quieren que los veas nosotros ponemos la mirada en ti las noticias que van$', ' ', texto)
	texto = re.sub(r'noticias telemundo noticias telemundo de hoy telemundo noticias noticias telemundo telemundo noticias de hoy noticias telemundo de hoy en vivo ultima hora noticias de hoy noticias de ultima hora$', ' ', texto)
	texto = re.sub(r'noticias telemundo noticias telemundo noticias telemundo de hoy telemundo noticias noticias telemundo telemundo noticias de hoy noticias telemundo de hoy en vivo ultima hora noticias de hoy noticias de ultima hora$', ' ', texto)
	texto = re.sub(r'sigue aqui la conferencia de la presidenta claudia sheinbaum pardo desde palacio nacional$', ' ', texto)
	texto = re.sub(r'siguenos en x danos me gusta en facebook vea la primera mananera de la presidenta de mexico$', ' ', texto)
	texto = re.sub(r'suscribete a nuestro canal sigue nuestro en vivo las horas sitio s w milenio com facebook x instagram tiktok$', ' ', texto)
	texto = re.sub(r'suscribete aqui siguenos en whatsapp siguenos tambien en facebook twitter instagram tiktok$', ' ', texto)
	texto = re.sub(r'suscribete shorts youtube com cnnee shorts nuestro sitio unete a whatsapp channel dale a me gusta en facebook siguenos en twitter miranos en instagram$', ' ', texto)
	texto = re.sub(r'suscribete shorts youtube com cnnee shorts nuestro sitio unete a whatsapp channel dale me gusta en facebook siguenos en twitter miranos en instagram$', ' ', texto)
	texto = re.sub(r'ultima hora suscribete aqui siguenos en whatsapp siguenos tambien en facebook twitter instagram tiktok$', ' ', texto)
	texto = re.sub(r'lee la nota completa visita s w aristeguinoticias com$', ' ', texto)
	texto = re.sub(r'para mas informacion visita s w aristeguinoticias com$', ' ', texto)
	texto = re.sub(r'visita s w aristeguinoticias com para toda la informacion sobre la reforma judicial$', ' ', texto)
	texto = re.sub(r'visita w aristeguinoticias com para mas informacion sobre la reforma judicial$', ' ', texto)
	texto = re.sub(r'visita s w aristeguinoticias com para mas informacion$', ' ', texto)
	texto = re.sub(r'visita w aristeguinoticias com para mas informacion$', ' ', texto)
	texto = re.sub(r'visita w aristeguinoticias com para mas detalles$', ' ', texto)
	texto = re.sub(r'visita s w aristeguinoticias com$', ' ', texto)
	texto = re.sub(r'visita w aristeguinoticias com$', ' ', texto)
	texto = re.sub(r'w aristeguinoticias com$', ' ', texto)
	texto = re.sub(r'descarga nuestra app suscribete noticias noticias telemundo es un proveedor lider de noticias para los hispanos de ee uu sus galardonados espacios de noticias transmitidos desde telemundo center incluyen los noticieros diarios noticias telemundo con julio vaqueiro noticias telemundo fin de semana noticias telemundo mediodia y noticias telemundo en la noche el equipo digital de noticias telemundo ofrece contenido ininterrumpido para los hispanos de ee uu a traves de sus crecientes plataformas moviles y en linea noticias telemundo investiga produce reportes investigativos y documentales en profundidad noticias telemundo planeta tierra ofrece informacion relacionada con el medio ambiente y el cambio climatico adicionalmente noticias telemundo produce galardonados especiales de noticias documentales y eventos noticiosos como debates politicos asambleas ciudadanas y foros telemundo es una empresa de medios de primera categoria lider en la industria en la produccion y distribucion de contenido en espanol de alta calidad a traves de multiples plataformas para hispanos en los estados unidos y alrededor del mundo la cadena ofrece producciones dramaticas originales de telemundo studios el productor de contenido en espanol de horario estelar asi como contenido alternativo peliculas de cine especiales noticias y eventos deportivos de primer nivel alcanzando el de los televidentes hispanos en los estados unidos en mercados a traves de estaciones propias y afiliadas de tv abierta telemundo tambien es propietaria de wkaq una estacion de television local que sirve puerto rico telemundo es parte de nbcuniversal telemundo enterprises una division de nbcuniversal una de las companias lideres en el mundo de los medios y entretenimiento nbcuniversal es una subsidiaria de comcast corporation siguenos en x danos me gusta en facebook$', ' ', texto)
	texto = re.sub(r'siguenos en x danos me gusta en facebook$', ' ', texto)
	texto = re.sub(r'youtu be \w+ \w $', ' ', texto)
	texto = re.sub(r'youtu be \w+ $', ' ', texto)
	texto = re.sub(r'^ultima hora', ' ', texto)
	texto = re.sub(r'^video oficial de noticias telemundo', ' ', texto)

	return texto



# -------------------------------------
def processText(allText, mode='title', traducir_emojis=False):
	""" Cleans all the garbage in the text and returns the cleaned text """

	## Quitar la ultima parte de los títulos
	if mode == 'title':
		allText = [t if len(t.split('-')) == 1 else ' '.join(t.split('-')[:-1]) for t in allText]


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


	## Quitar URLs
	print(f'\n> Remove URLs and hashtags')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [removeUrls(t) for t in allText]
	allText = [re.sub(r'#\w+', '', t) for t in allText]


	## Quitar otras cosas
	print(f'\n> Remove other things')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	allText = [helper_preprocess(t) for t in allText]


	print(f'\n> Puntuation y lo que falta')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')
	
	allText = [removePunctuation(t) for t in allText]

	allText = [remove_emojis_symbos_unicode(t, traducir_emojis) for t in allText]

	allText = [t.lower() for t in allText]


	if mode == 'title':
		allText = [t.replace('ultima hora', '').strip() for t in allText]
	elif mode == 'description':
		allText = [remove_otros(t).strip() for t in allText]
	else:
		pass


	return allText



def procesamiento_videos(sourceDirectory1, sourceDirectory2, destinyDirectory):
	"""
	* convertir duracion
	* concatenar comentarios procesados con video info procesada
	"""

	print(f'\n\nProcesando...')

	## Leer videos elegidos (video_id,video_title,channel_title,video_published_at,video_duration,video_total_views,video_total_likes,video_total_comments)
	metaVideos = pd.read_csv(os.path.join(sourceDirectory1, 'videos_elegidos_all_sinrepetir.csv'))
	metaVideos['video_total_likes'].fillna(0, inplace=True)

	## Leer la semilla que tiene la descripción de la noticia
	descrVideos = pd.read_csv(os.path.join(sourceDirectory2, 'videos_2024.csv'), usecols=['video_id', 'video_description']).drop_duplicates()
	descrVideos['video_description'].fillna('ND', inplace=True)
	
	## Concatenar la información y eliminar duplicados
	infoVideos = pd.merge(left=metaVideos, right=descrVideos, on='video_id', how='left')
	infoVideos.drop_duplicates(subset=['video_id'], inplace=True)

	## Convertir fecha
	print(f'* Fecha...')
	infoVideos['video_published_at_day'] = infoVideos['video_published_at'].apply(lambda x: x.split('T')[0])
	infoVideos['video_published_at_hour'] = infoVideos['video_published_at'].apply(lambda x: x.split('T')[1].replace('Z', ''))

	## Convertir la duración a formato legible y separarla en horas, minutos, segundos
	print(f'* Duracion...')
	infoVideos['video_duration_format'] = infoVideos['video_duration'].apply(lambda x: iso8601_to_excel_duration(x))

	infoVideos['video_duration_hour'] = infoVideos['video_duration_format'].apply(lambda x: int(x.split(':')[0]))
	infoVideos['video_duration_minutes'] = infoVideos['video_duration_format'].apply(lambda x: int(x.split(':')[1]))
	infoVideos['video_duration_seconds'] = infoVideos['video_duration_format'].apply(lambda x: int(x.split(':')[2]))

	## Filtrar videos de menos de una hora
	infoVideos = infoVideos[infoVideos['video_duration_hour'] == 0]

	## Limpiar titulo
	print(f'* Titulo...')
	infoVideos['video_titleClean'] = processText(infoVideos['video_title'].values, mode='title')

	## Limpiar descripcion
	print(f'* Descripcion...')
	infoVideos['video_descriptionClean'] = processText(infoVideos['video_description'].values, mode='description')


	## Guardar
	print(f'* Guardando...')
	print(infoVideos.shape)

	colsElegir = ['video_id', 'channel_title', 'video_published_at_day', 'video_published_at_hour',
			   'video_duration_format', 'video_duration_hour', 'video_duration_minutes', 'video_duration_seconds',
			   'video_total_views', 'video_total_likes', 'video_total_comments',
			   'video_titleClean', 'video_descriptionClean']
	
	infoVideos[colsElegir].to_csv(os.path.join(destinyDirectory, f'info_videos.csv'), index=False)





### ===============================================================================
sourceDirectory1 = r'..\Dataset\3_Data_seed_videos_info'
sourceDirectory2 = r'..\Dataset\2_Data_seed_videos'
destinyDirectory = r'..\Dataset\6_Data_seed_videos_info_preprocessed'

procesamiento_videos(sourceDirectory1, sourceDirectory2, destinyDirectory)
