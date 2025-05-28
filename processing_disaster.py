import pandas as pd
import re
import numpy as np


def processing_disaster(df):
    def limpar_mortos(valor):
        if pd.isna(valor):
            return np.nan

        # Remove espaços, traços não numéricos e substitui vírgula por ponto se necessário
        texto = str(valor).replace('\xa0', '').replace('+', '')
        texto = texto.replace(',', '').replace('–', '-').replace('−', '-').replace('.', '')

        # Divide por espaços e processa cada parte separadamente
        partes = texto.split()
        numeros = []
        for parte in partes:
            # Casos com intervalo: pegar a média
            if '-' in parte or 'a' in parte:
                try:
                    subpartes = re.split(r'[-–]', parte)
                    subnumeros = [float(p.strip()) for p in subpartes if p.strip()]
                    if subnumeros:
                        numeros.append(sum(subnumeros) / len(subnumeros))
                except:
                    continue
            else:
                try:
                    numeros.append(float(parte))
                except:
                    continue

        if numeros:
            return int(sum(numeros) / len(numeros))  # Retorna a média dos números encontrados
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
        match = re.match(r'(\d{1,2}) de (\w+) de (\d{4})', data) or re.match(r'(\d{1,2}) de (\w+) de (\d{3})', data)
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
        match = re.match(r'(\w+) de (\d{4})', data) or re.match(r'(\w+) de (\d{3})', data)
        if match:
            mes_ext, ano = match.groups()
            mes = meses.get(mes_ext)
            if mes:
                return f"00-{mes}-{ano}"
        
        # Apenas ano (formato genérico)
        match = re.match(r'^\d{4}$', data) or re.match(r'^\d{2}$', data)
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

        # Separa a frase por vírgula e pega apenas a última parte
        partes = localizacao.split(',')
        localizacao = partes[-1].strip() if partes else localizacao

        # Substitui " e " por ", " para padronizar múltiplos países
        localizacao = localizacao.replace(' e ', ', ')

        # Substitui pontos duplos, vírgulas duplas, espaços extras
        localizacao = re.sub(r'\s*,\s*', ', ', localizacao)  # espaço após vírgula
        localizacao = re.sub(r'\s+', ' ', localizacao).strip()  # remove espaços duplicados
        localizacao = re.sub(r',$', '', localizacao)  # remove vírgula no final

        return localizacao

    def deriva_data(df):
        df['Dia'] = df['Data'].str[:2]
        df['Mês'] = df['Data'].str[3:5]
        df['Ano'] = df['Data'].str[6:]

        df['Dia'] = df['Dia'].replace('00','')
        df['Mês'] = df['Mês'].replace('00','')
        df['Ano'] = df['Ano'].replace('00','')

        return df
    
    def estimar_data(data):
        if pd.isna(data):
            return None

        partes = data.split('-')
        if len(partes) == 3:
            dia = partes[0] if partes[0] != '00' else '01'
            mes = partes[1] if partes[1] != '00' else '01'
            ano = partes[2]
            return f"{dia}-{mes}-{ano}"
        return data
    
    df['Data'] = df['Data'].apply(normalizar_data)
    df['Data estimada'] = df['Data'].apply(estimar_data)
    df['Número de mortos'] = df['Número de mortos'].apply(limpar_mortos)
    df['Tipo'] = df['Tipo'].astype(str).str.strip().str.capitalize()
    df['Localização'] = df['Localização'].apply(limpar_localizacao)

    df = df.rename(columns={'Localização': 'País'})
    df = deriva_data(df)

    return df

