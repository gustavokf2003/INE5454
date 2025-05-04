import pandas as pd
import re
import numpy as np

df = pd.read_csv('desastres_naturais.csv')

def limpar_mortos(valor):
    if pd.isna(valor):
        return np.nan

    # Remove espaços, traços não numéricos e substitui vírgula por ponto se necessário
    texto = str(valor).replace('\xa0', '').replace(' ', '').replace('+', '')
    texto = texto.replace(',', '').replace('–', '-').replace('−', '-').replace('.', '')
    
    # Casos com intervalo: pegar a média
    if '-' in texto:
        try:
            partes = re.split(r'[-–]', texto)
            numeros = [float(p.strip()) for p in partes if p.strip()]
            if numeros:
                return int(sum(numeros) / len(numeros))
        except:
            return np.nan
    try:
        return int(float(texto))
    except:
        return np.nan
    
def normalizar_data(data):
    if pd.isna(data):
        return None

    data = str(data).strip().lower()

    # Mapeamento de meses em português
    meses = {
        'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
        'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
        'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
    }

    # Expressão para capturar dia, mês (por extenso) e ano
    match = re.match(r'(\d{1,2}) de (\w+) de (\d{3})', data)
    if match:
        dia, mes_ext, ano = match.groups()
        mes = meses.get(mes_ext)
        if mes:
            return f"{int(dia):02d}-{mes}-{ano}"
        
    # Expressão ano ou ano
    match = re.match(r'(\d{4}) ou (\d{4})', data)
    if match:
        ano1, ano2 = match.groups()
        return f"00-00-{ano1}"
    
    # Formato: mês por extenso e ano (sem dia)
    match = re.match(r'(\w+) de (\d{3})', data)
    if match:
        mes_ext, ano = match.groups()
        mes = meses.get(mes_ext)
        if mes:
            return f"00-{mes}-{ano}"
    
    # Apenas ano (formato genérico)
    match = re.match(r'^\d{4}$', data)
    if match:
        ano = match.group(0)
        return f"00-00-{ano}"
    
    # Tenta converter diretamente se estiver em formato dd/mm/yyyy ou similar
    try:
        dt = pd.to_datetime(data, dayfirst=True, errors='coerce')
        if pd.notna(dt):
            return dt.strftime('%d-%m-%y')
    except:
        pass

    return None  # Caso não consiga tratar

def limpar_localizacao(localizacao):
    if pd.isna(localizacao):
        return localizacao

    # Se a localização atual estiver entre parênteses, extrai o conteúdo (ex: " (agora Turquia)")
    match = re.search(r'\((.*?)\)', localizacao)
    if match:
        conteudo = match.group(1)
        if 'agora' in conteudo:
            localizacao = conteudo.replace('agora', '').strip()
        else:
            localizacao = re.sub(r'\(.*?\)', '', localizacao).strip()
    else:
        localizacao = re.sub(r'\(.*?\)', '', localizacao).strip()

    # Substitui " e " por ", " para padronizar múltiplos países
    localizacao = localizacao.replace(' e ', ', ')

    # Substitui pontos duplos, vírgulas duplas, espaços extras
    localizacao = re.sub(r'\s*,\s*', ', ', localizacao)  # espaço após vírgula
    localizacao = re.sub(r'\s+', ' ', localizacao).strip()  # remove espaços duplicados
    localizacao = re.sub(r',$', '', localizacao)  # remove vírgula no final

    return localizacao

df['Data'] = df['Data'].apply(normalizar_data)
df['Número de mortos'] = df['Número de mortos'].apply(limpar_mortos)
df['Tipo'] = df['Tipo'].astype(str).str.strip().str.capitalize()
df['Localização'] = df['Localização'].apply(limpar_localizacao)

df.to_csv('desastres_naturais_corrigido.csv', index=False)

