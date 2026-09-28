import pandas as pd

# ============================================================
# ARQUIVOS
# ============================================================

ARQUIVO = "/home/vinicius/Downloads/microdados_enem_2024/DADOS/PARTICIPANTES_2024.csv"
SAIDA = "enem_2024_pe_gom.csv"

# ============================================================
# COLUNAS
# ============================================================

colunas = [
    "SG_UF_PROVA",
    "TP_COR_RACA",
    "Q007",
    "TP_SEXO",
    "TP_FAIXA_ETARIA"
]

df = pd.read_csv(
    ARQUIVO,
    sep=";",
    encoding="latin1",
    usecols=colunas,
    low_memory=False
)

print("Total Brasil:", len(df))

# ============================================================
# FILTRAR APENAS PERNAMBUCO
# ============================================================

df = df[df["SG_UF_PROVA"] == "PE"].copy()

print("Total Pernambuco:", len(df))

# ============================================================
# SEXO
# 1 = Masculino
# 2 = Feminino
# ============================================================

df["SEXO"] = df["TP_SEXO"].map({
    "M": 1,
    "F": 2
})

# ============================================================
# COR / RAÇA
# Mantém os códigos originais
#
# 0 = Não declarado
# 1 = Branca
# 2 = Preta
# 3 = Parda
# 4 = Amarela
# 5 = Indígena
# 6 = Sem informação
# ============================================================

df["COR_RACA"] = df["TP_COR_RACA"]

# ============================================================
# IDADE AGRUPADA
#
# 1 = Até 17
# 2 = 18–20
# 3 = 21–24
# 4 = 25–30
# 5 = 31–40
# 6 = 41–50
# 7 = 51+
# ============================================================

mapa_idade = {
    1: 1,
    2: 1,

    3: 2,
    4: 2,
    5: 2,

    6: 3,
    7: 3,
    8: 3,
    9: 3,

    10: 4,
    11: 4,

    12: 5,
    13: 5,

    14: 6,
    15: 6,

    16: 7,
    17: 7,
    18: 7
}

df["IDADE"] = df["TP_FAIXA_ETARIA"].map(mapa_idade)

# ============================================================
# RENDA AGRUPADA EM 7 FAIXAS
#
# 1 = A-B
#     Nenhuma renda até R$ 1.412
#
# 2 = C-D
#     R$ 1.412,01 até R$ 2.824
#
# 3 = E-F
#     R$ 2.824,01 até R$ 4.236
#
# 4 = G-H
#     R$ 4.236,01 até R$ 7.060
#
# 5 = I-K
#     R$ 7.060,01 até R$ 11.296
#
# 6 = L-N
#     R$ 11.296,01 até R$ 16.944
#
# 7 = O-Q
#     Acima de R$ 16.944
# ============================================================

mapa_renda = {
    "A": 1,
    "B": 1,

    "C": 2,
    "D": 2,

    "E": 3,
    "F": 3,

    "G": 4,
    "H": 4,

    "I": 5,
    "J": 5,
    "K": 5,

    "L": 6,
    "M": 6,
    "N": 6,

    "O": 7,
    "P": 7,
    "Q": 7
}

df["RENDA"] = df["Q007"].map(mapa_renda)

# ============================================================
# REMOVER REGISTROS SEM INFORMAÇÕES NECESSÁRIAS
# ============================================================

df = df.dropna(
    subset=[
        "SEXO",
        "COR_RACA",
        "IDADE",
        "RENDA"
    ]
)

# ============================================================
# CONVERTER PARA INTEIRO
# ============================================================

df["SEXO"] = df["SEXO"].astype(int)
df["COR_RACA"] = df["COR_RACA"].astype(int)
df["IDADE"] = df["IDADE"].astype(int)
df["RENDA"] = df["RENDA"].astype(int)

# ============================================================
# CRIAR ID
# ============================================================

df = df.reset_index(drop=True)

df["ID"] = range(1, len(df) + 1)

# ============================================================
# TABELA FINAL PARA O GOM
# ============================================================

gom = df[
    [
        "ID",
        "SEXO",
        "COR_RACA",
        "IDADE",
        "RENDA"
    ]
].copy()

# ============================================================
# VERIFICAÇÕES
# ============================================================

print("\nPrimeiras linhas:")
print(gom.head(20))

print("\nTotal utilizado no GoM:", len(gom))

print("\nSexo:")
print(gom["SEXO"].value_counts().sort_index())

print("\nCor/Raça:")
print(gom["COR_RACA"].value_counts().sort_index())

print("\nIdade:")
print(gom["IDADE"].value_counts().sort_index())

print("\nRenda:")
print(gom["RENDA"].value_counts().sort_index())

# ============================================================
# SALVAR
# ============================================================

gom.to_csv(
    SAIDA,
    sep=";",
    index=False,
    encoding="utf-8-sig"
)

print(f"\nArquivo criado: {SAIDA}")