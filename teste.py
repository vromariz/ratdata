import pandas as pd

ITENS_PATH = "/home/vinicius/Downloads/microdados_enem_2024/DADOS/ITENS_PROVA_2024.csv"

MICRODATA_PATH = "/home/vinicius/Downloads/microdados_enem_2024/DADOS/RESULTADO_2024.csv"

itens = pd.read_csv(
    ITENS_PATH,
    sep=';',
    encoding='latin-1'
)

df = pd.read_csv(
    MICRODATA_PATH,
    sep=';',
    encoding='latin-1'
)

itens_alvo = [60335, 111706, 125923, 29021]

itens = itens[
    (itens['SG_AREA'] == 'MT') &
    (itens['IN_ITEM_ABAN'] == 0)
]

mapa_posicoes = {}

for _, row in itens.iterrows():

    chave = (row['CO_PROVA'], row['CO_ITEM'])

    mapa_posicoes[chave] = row['CO_POSICAO']

df = df[
    df['TX_RESPOSTAS_MT'].notna()
]

def acertou_todas(row):

    prova = row['CO_PROVA_MT']

    respostas = row['TX_RESPOSTAS_MT']

    gabarito = row['TX_GABARITO_MT']

    for item in itens_alvo:

        chave = (prova, item)

        if chave not in mapa_posicoes:
            return 0

        co_posicao = mapa_posicoes[chave]

        indice = co_posicao - 136

        resposta_aluno = respostas[indice]

        resposta_correta = gabarito[indice]

        if resposta_aluno != resposta_correta:
            return 0

    return 1

df['ACERTOU_TODAS'] = df.apply(
    acertou_todas,
    axis=1
)

df_filtrado = df[
    df['ACERTOU_TODAS'] == 1
]

def calcular_percentual(row):

    respostas = row['TX_RESPOSTAS_MT']

    gabarito = row['TX_GABARITO_MT']

    acertos = 0

    for i in range(45):

        if respostas[i] == gabarito[i]:
            acertos += 1

    return (acertos / 45) * 100

df_filtrado['PERCENTUAL_MT'] = df_filtrado.apply(
    calcular_percentual,
    axis=1
)

resultado = (
    df_filtrado
    .groupby('NO_MUNICIPIO_PROVA')
    .agg({
        'NU_INSCRICAO': 'count',
        'PERCENTUAL_MT': 'mean',
        'NU_NOTA_MT': 'mean'
    })
    .rename(columns={
        'NU_INSCRICAO': 'QTD_ALUNOS',
        'PERCENTUAL_MT': 'MEDIA_PERCENTUAL_MT',
        'NU_NOTA_MT': 'MEDIA_NOTA_MT'
    })
    .sort_values(
        'QTD_ALUNOS',
        ascending=False
    )
)

print("\nRESULTADO FINAL\n")

print(resultado)

resultado.to_csv(
    "resultado_municipios.csv"
)

df_filtrado.to_csv(
    "alunos_acertaram_todas.csv",
    index=False
)