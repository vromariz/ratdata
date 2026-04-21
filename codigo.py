import pandas as pd

ITENS_PATH = "/workspaces/ratdata/DADOS/ITENS_PROVA_2024.csv"

itens = pd.read_csv(ITENS_PATH, sep=';', encoding='latin-1')

resultado = itens[
    (itens['CO_POSICAO'].isin([139, 140, 149, 165])) &
    (itens['SG_AREA'] == 'MT') &
    (itens['TX_COR'] == 'AMARELA')
]

print(resultado)

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