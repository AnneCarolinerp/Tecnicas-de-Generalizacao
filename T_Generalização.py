from pandas.core.frame import DataFrame
from google.colab.patches import cv2_imshow
import pandas as pd
import math
import cv2

corona = pd.read_csv("Covid.csv", low_memory=False)
regioes = pd.read_csv("Regioes.csv")

corona = corona[['municipioCaso', 'sexoCaso', 'dataNascimento', 'resultadoFinalExame']]
corona = corona.dropna()

#@title Técnicas de Anonimização – Generalização {run:'auto'}

#@markdown Informe o nível desejado para visualização da data de nascimento:
nivelDN = 'Nivel 1' #@param ["Nivel 1", "Nivel 2", "Nivel 3"]

#@markdown Informe o nível desejado para visualização do municipio:
nivelEst = 'Nivel 1' #@param ["Nivel 1", "Nivel 2"]

#@markdown Representação da árvore:
img = cv2.imread("RepresentacaoDeArvore.png")
cv2_imshow(img)

lines = []

for index, row in corona[:10].iterrows():
  if(type(row['dataNascimento'])==str):
    dataNasc = row['dataNascimento'].split('-')
    if nivelDN == "Nivel 3" :
      row['dataNascimento'] = dataNasc[2]+'/'+dataNasc[1]+'/'+dataNasc[0]
    elif nivelDN == "Nivel 2" :
      row['dataNascimento'] = dataNasc[1]+'/'+dataNasc[0]
    elif nivelDN == "Nivel 1" :
      row['dataNascimento'] = dataNasc[0]
  if(type(row['municipioCaso']) == str):
    if nivelEst == "Nivel 2" :
      row['municipioCaso'] = row['municipioCaso']
      dataframe = pd.DataFrame(lines, columns=['Data', 'Municipio', 'Resultado Exame'])

    elif nivelEst == "Nivel 1" :
      row['municipioCaso'] = regioes.query('municipios == "'+ row['municipioCaso'] + '"')['regioes'].values[0]
      dataframe = pd.DataFrame(lines, columns=['Data', 'Região', 'Resultado Exame'])

  result = (row['dataNascimento'], row['municipioCaso'], row['resultadoFinalExame'])
  lines.append(result)

dataframe.to_csv('covid_publico')
for coluna in dataframe.columns:
  display(dataframe.sort_values(coluna))
  break