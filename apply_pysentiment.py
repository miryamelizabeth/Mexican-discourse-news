### Ejecutar en google colab usando GPU

import pandas as pd
import os
import datetime

from pysentimiento import create_analyzer



def obtenerTagFromModel(sourceDirectory, destinyDirectory, task, mode='comments', lang='es'):
	"""
	task = 'sentiment', 'emotion', 'irony'
	"""

	print(f'\n\n*** Iniciando {task.upper()} ***')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')


	analyzer = create_analyzer(task=task, lang=lang)


	print(f'\nLeer dataset...')
	df = pd.read_csv(os.path.join(sourceDirectory, f'final_dataset.csv'))
	total = df.shape[0]

	print(f'* Total de comentarios: {total:,d}')

	columnInterest = 'id' if mode == 'comments' else 'video_id'

	data = []

	contar = 0
	for iD, text in zip(df[columnInterest].values, df['texto'].values):

		resultAnalyzer = analyzer.predict(text)
		# returns AnalyzerOutput(output=POS, probas={POS: 0.998, NEG: 0.002, NEU: 0.000})

		resultados = resultAnalyzer.probas
		resultados['tag'] = resultAnalyzer.output
		resultados[columnInterest] = iD

		data.append(resultados)

		if contar % 1000 == 0:
			print(f'> Procesados {contar:,d}/{total:,d} - {datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}...')

		if contar % 5000 == 0:
			tempDf = pd.DataFrame(data=data)
			tempDf.to_csv(os.path.join(destinyDirectory, f'temp{contar}_{task}_{mode}.csv'), index=False)

		contar += 1


	print(f'\n\n Guardando...')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')

	finalDf = pd.DataFrame(data=data)
	finalDf.to_csv(os.path.join(destinyDirectory, f'FINAL_{task}_{mode}.csv'), index=False)

	print(f'\n\nEnd! :D')
	print(f'{datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}')





## ===============================================
sourceDirectory = r'..\Dataset\7_Data_final'
destinyDirectory = r'..\Dataset\8_Data_attributes'

TASK = 'sentiment'
# TASK = 'emotion'

# MODE = 'comments'
MODE = 'videos'

obtenerTagFromModel(sourceDirectory, destinyDirectory, task=TASK, mode=MODE)
