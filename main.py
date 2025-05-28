from normalization import normalization
from processing_disaster import processing_disaster
from processing_countries import processing_countries
from scraping_country import scraping_cia
from scraping import scraping_wikipedia

def main():
    # Coleta dados de desastres naturais
    desastres = scraping_wikipedia()

    # Processa os dados de desastres naturais
    desastres_corrigidos = processing_disaster(desastres)
    print(desastres_corrigidos[24:])

    # Coleta dados de países
    paises = scraping_cia()

    # Processa os dados de países
    desastres_df, paises_df, desastre_pais = normalization(desastres_corrigidos)

    # Processa os dados dos países
    paises_df = processing_countries(paises, paises_df)

    # Salva os DataFrames em arquivos CSV
    desastres_df.to_csv("data/desastres.csv", index=False, encoding='utf-8')
    paises_df.to_csv("data/paises.csv", index=False, encoding='utf-8')
    desastre_pais.to_csv("data/desastre_pais.csv", index=False, encoding='utf-8')

if __name__ == "__main__":
    main()