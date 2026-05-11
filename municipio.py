import pandas as pd

MICRODATA_PATH = "/home/vinicius/Downloads/microdados_enem_2024/DADOS/RESULTADOS_2024.csv"

df = pd.read_csv(
    MICRODATA_PATH,
    sep=';',
    encoding='latin-1'
)

municipios = (
    df['NO_MUNICIPIO_PROVA']
    .dropna()
    .unique()
)

municipios = sorted(municipios)

for municipio in municipios:
    print(municipio)

print("\nQuantidade de municípios:", len(municipios))