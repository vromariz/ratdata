import pandas as pd

pd.set_option('display.max_columns', None)   # mostra todas as colunas
pd.set_option('display.width', None)         # evita quebra de linha
pd.set_option('display.max_colwidth', None)  # mostra conteúdo completo

ITENS_PATH = "/home/vinicius/Downloads/microdados_enem_2024/DADOS/ITENS_PROVA_2024.csv"

itens = pd.read_csv(ITENS_PATH, sep=';', encoding='latin-1')

resultado = itens[
    (itens['CO_ITEM'].isin([60335, 111706, 125923, 29021]))&
    (itens['TX_COR'].isin(['AZUL', 'AMARELA', 'LARANJA', 'LEITOR TELA', 'ROXA', 'VERDE', 'BRANCA',
 'CINZA']))&
    (itens['IN_ITEM_ABAN'] == 0)
]

print(resultado.value_counts)

print(itens['TX_COR'].unique())

resultado = itens[
    (itens['SG_AREA'] == 'MT') &
    (itens['TX_COR'] == 'AMARELA') &
    (itens['IN_ITEM_ABAN'] == 0)
]

print(resultado['CO_PROVA'].value_counts())

prova_certa = itens[
    (itens['CO_PROVA'] == 1408) &
    (itens['SG_AREA'] == 'MT') &
    (itens['TX_COR'] == 'AMARELA')
]

prova_certa = prova_certa[
    prova_certa['CO_POSICAO'].isin([139, 140, 149, 165])
]

#1408 e a prova certa para ser estudada

print(prova_certa[['CO_POSICAO', 'CO_ITEM', 'CO_PROVA']])