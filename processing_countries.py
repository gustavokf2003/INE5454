import pandas as pd
from googletrans import Translator
from countries import inverse_countries
from sigla import get_country_codes

def processing_countries(df, df_paises):
    translator = Translator()

    for column in ['Location', 'Climate', 'Map references']:
        df[column] = df[column].apply(lambda x: translator.translate(x, src='en', dest='pt').text if isinstance(x, str) else x)

    def convert_coordinates(coord):
        if isinstance(coord, str):
            try:
                parts = coord.split(',')

                if len(parts) != 2:
                    raise ValueError(f"Invalid coordinate format: {coord}")
                
                lat_str = parts[0].strip().split(' ')
                lat = float(f'{lat_str[0]}.{lat_str[1]}') * (1 if lat_str[2] == 'N' else -1)

                lon_str = parts[1].strip().split(' ')
                lon = float(f'{lon_str[0]}.{lon_str[1]}') * (1 if lon_str[2] == 'E' else -1)

                return f"{lat}, {lon}"
            except (ValueError, IndexError) as e:
                return None  # Return None for invalid coordinates
        return coord

    def type_areas(area):
        if isinstance(area, str):
            area = area.strip()  
            if area == '' or not area[:-6].replace(',', '').isdigit():
                return None 
            area = float(area[:-6].replace(',', ''))
            return int(area)
        return area

    df['Geographic coordinates'] = df['Geographic coordinates'].apply(convert_coordinates)
    df['Area Total'] = df['Area Total'].apply(type_areas)
    df['Area Land'] = df['Area Land'].apply(type_areas)
    df['Area Water'] = df['Area Water'].apply(type_areas)
    df['Country'] = df['Country'].apply(lambda x: inverse_countries[x])

    df = df.rename(columns={
        'Country': 'País',
        'Location': 'Localização',
        'Climate': 'Clima',
        'Map references': 'Referências do mapa',
        'Geographic coordinates': 'Coordenadas geográficas',
        'Area Total': 'Área total',
        'Area Land': 'Área terrestre',
        'Area Water': 'Área aquática'
    })

    df_paises = df_paises.merge(df, on='País', how='left')
    siglas = get_country_codes()
    df_paises = df_paises.merge(siglas, on='País', how='left')
    print(df_paises)

    return df_paises