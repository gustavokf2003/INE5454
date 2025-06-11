import pandas as pd

def get_country_codes():
    url = "https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_c%C3%B3digo_do_COI"
    tables = pd.read_html(url)
    tables = tables[0:1]
    df = pd.DataFrame(tables[0])
    df.rename(columns={
        'Código': 'Sigla',
        'País / Designação segundo o COI': 'País'
    }, inplace=True)

    df['País'] = df['País'].str.split(' ').str[0]

    return df[['País', 'Sigla']].drop_duplicates()

