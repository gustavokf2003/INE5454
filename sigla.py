import pandas as pd

def get_country_codes():
    url = "https://pt.wikipedia.org/wiki/Lista_de_pa%C3%ADses_por_c%C3%B3digo_do_COI"
    tables = pd.read_html(url)
    df = pd.DataFrame(tables[0])
    df.rename(columns={
        'Código': 'ISO',
        'País / Designação segundo o COI': 'País'
    }, inplace=True)
    print(df[df['ISO'] == 'IRI']['País'].str.split('designação').str[0].str.strip())

    df['País'] = df['País'].str.split('designação').str[0].str.strip()
    df['País'] = df['País'].replace('Irão', 'Irã')

    df2 = pd.DataFrame(tables[1])
    df2.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in df2.columns]
    df2.rename(columns={
        'Código Código': 'ISO',
        'Designação COI Designação COI': 'País'
    }, inplace=True)

    df3 = pd.DataFrame(tables[3], columns=['Código', 'País / Território'])
    df3.rename(columns={
        'Código': 'ISO',
        'País / Território': 'País'
    }, inplace=True)

    df = pd.concat([df, df2, df3], ignore_index=True)

    return df[['País', 'ISO']].drop_duplicates()


