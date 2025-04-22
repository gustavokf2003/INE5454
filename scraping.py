import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# Função para remover colchetes e números de referência
def limpar_referencias(texto):
    if isinstance(texto, str):
        return re.sub(r'\[\d+\]', '', texto).strip()
    return texto

# Função para remover palavras específicas de uma string
def remover_palavras(texto, palavras):
    for palavra in palavras:
        texto = texto.replace(palavra, '')
    return texto.strip()


url = "https://pt.wikipedia.org/wiki/Lista_de_desastres_naturais_por_n%C3%BAmero_de_%C3%B3bitos"
res = requests.get(url)
soup = BeautifulSoup(res.content, "html.parser")

# Encontra todas as tabelas no HTML
tabelas = pd.read_html(str(soup))
# Lista para armazenar todas as tabelas processadas
tabelas_processadas = []

# Filtrar tabelas desejadas
for tabela in tabelas:
    # Verifica se a tabela possui as colunas desejadas
    colunas_desejadas = ['Número de mortos', 'Evento', 'Localização', 'Data']
    colunas_desejadas2 = ['Número de mortos (estimativa)', 'Evento', 'Localização', 'Data']
    if all(coluna in tabela.columns for coluna in colunas_desejadas):
        tabelas_processadas.append(tabela)
    if all(coluna in tabela.columns for coluna in colunas_desejadas2):
        tabela = tabela.rename(columns={'Número de mortos (estimativa)': 'Número de mortos'})
        tabelas_processadas.append(tabela)


tabelas_modificadas = []
for i, tabela in enumerate(tabelas_processadas):
    # Aplica a função em todas as células do DataFrame
    tabela = tabela.applymap(limpar_referencias)

    # Tenta encontrar o título da tabela
    titulo = soup.find_all("table")[i+2].find_previous("h3")
    if titulo != None:
        titulo = titulo.text

        titulo = remover_palavras(titulo, ["Dez", "mais", "mortíferas", "mortíferos"])

        tabela['Tipo'] = titulo
        tabelas_modificadas.append(tabela)


df = pd.concat(tabelas_modificadas, ignore_index=True)
df = df.drop(columns=['Classificação'], errors='ignore')
df.to_csv("desastres_naturais.csv", index=False, encoding='utf-8')