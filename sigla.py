import pandas as pd

def get_country_codes():
    url = "https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_c%C3%B3digo_do_COI"
    tables = pd.read_html(url)
    tables = tables[0:1]

    all_countries = pd.DataFrame()
    for table in tables:
        # Tenta encontrar as colunas certas em qualquer variação
        
        col_map = {}
        for col in table.columns:
            if 'código' in col.lower():
                col_map[col] = 'Sigla COI'
            elif 'país' in col.lower() or 'comitê' in col.lower():
                col_map[col] = 'País'

        # Só processa a tabela se encontrou ambas as colunas
        if 'País' in col_map.values() and 'Sigla COI' in col_map.values():
            table = table.rename(columns=col_map)[['País', 'Sigla COI']]
            table['País'] = table['País'].str.strip()

            # Elimina duplicados com base no nome do país
            if all_countries.empty:
                all_countries = table
            else:
                new_entries = table[~table['País'].isin(all_countries['País'])]
                all_countries = pd.concat([all_countries, new_entries], ignore_index=True)

    return all_countries

siglas = get_country_codes()
print(siglas.head(20))