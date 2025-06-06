import pandas as pd
import countries

def normalization(df):
    # Cria IDs únicos para os desastres
    df["desastreID"] = range(1, len(df) + 1)
    desastres = df.drop(columns=["País"])  # Remove a coluna País da tabela principal

    # Extrai todos os países únicos
    todos_paises = set()
    for paises in df["País"]:
        for pais in str(paises).split(","):
            todos_paises.add(pais.strip())

    # Cria a tabela de países com ID
    paises_lista = sorted(todos_paises)
    paises_df = pd.DataFrame({
        "PaisID": range(1, len(paises_lista) + 1),
        "País": paises_lista
    })

    # Cria um dicionário para mapear país → ID
    pais_to_id = dict(zip(paises_df["País"], paises_df["PaisID"]))

    # Cria a tabela desastre_pais
    relacoes = []
    for idx, row in df.iterrows():
        desastre_id = row["desastreID"]
        for pais in str(row["País"]).split(","):
            pais_nome = pais.strip()
            relacoes.append({
                "desastreID": desastre_id,
                "PaisID": pais_to_id[pais_nome]
            })

    desastre_pais = pd.DataFrame(relacoes)

    # Salva os DataFrames em arquivos CSV
    return desastres, paises_df, desastre_pais