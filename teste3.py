import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ARQUIVO = "/home/vinicius/Downloads/microdados_enem_2024/DADOS/PARTICIPANTES_2024.csv"

colunas = [
    "SG_UF_PROVA",
    "TP_COR_RACA",
    "Q006",
    "TP_SEXO",
    "TP_FAIXA_ETARIA"
]

print("Lendo arquivo...")

df = pd.read_csv(
    ARQUIVO,
    sep=";",
    encoding="latin1",
    usecols=colunas,
    low_memory=False
)

print("Dados carregados!")

# --------------------------------
# MAPEAMENTOS
# --------------------------------

# Sexo
mapa_sexo = {
    "M": "Masculino",
    "F": "Feminino"
}

# Cor/Raça
mapa_cor_raca = {
    0: "Não declarado",
    1: "Branca",
    2: "Preta",
    3: "Parda",
    4: "Amarela",
    5: "Indígena",
    6: "Sem informação"
}

# Faixa etária
mapa_idade = {
    1: "Menor de 17",
    2: "17 anos",
    3: "18 anos",
    4: "19 anos",
    5: "20 anos",
    6: "21 anos",
    7: "22 anos",
    8: "23 anos",
    9: "24 anos",
    10: "25 anos",
    11: "26 a 30 anos",
    12: "31 a 35 anos",
    13: "36 a 40 anos",
    14: "41 a 45 anos",
    15: "46 a 50 anos",
    16: "51 a 55 anos",
    17: "56 a 60 anos",
    18: "Mais de 60 anos"
}

# Renda simplificada do PARTICIPANTES_2024.csv
mapa_renda = {
    "A": "Menor renda",
    "B": "Maior renda"
}

df["SEXO"] = df["TP_SEXO"].map(mapa_sexo)
df["COR_RACA"] = df["TP_COR_RACA"].map(mapa_cor_raca)
df["IDADE"] = df["TP_FAIXA_ETARIA"].map(mapa_idade)
df["RENDA"] = df["Q006"].map(mapa_renda)

df = df.dropna()

# --------------------------------
# Função majoritária
# --------------------------------
def majoritario(serie):
    return serie.mode().iloc[0]

# --------------------------------
# Resultado por estado
# --------------------------------
resultado = df.groupby("SG_UF_PROVA").agg(
    participantes=("SG_UF_PROVA", "count"),

    sexo_majoritario=("SEXO", majoritario),
    idade_majoritaria=("IDADE", majoritario),
    cor_raca_majoritaria=("COR_RACA", majoritario),
    renda_majoritaria=("RENDA", majoritario),

    # percentual de maior renda
    percentual_maior_renda=(
        "Q006",
        lambda x: round((x == "B").mean() * 100, 2)
    ),

    # percentual de menor renda
    percentual_menor_renda=(
        "Q006",
        lambda x: round((x == "A").mean() * 100, 2)
    )

).reset_index()

resultado = resultado.sort_values("SG_UF_PROVA")

# --------------------------------
# Mostrar resultado
# --------------------------------
print("\nPERFIL MAJORITÁRIO DOS ESTADOS\n")
print(resultado)

# --------------------------------
# Salvar CSV
# --------------------------------
resultado.to_csv(
    "perfil_majoritario_estados_2024.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo salvo: perfil_majoritario_estados_2024.csv")

# --------------------------------
# Pernambuco
# --------------------------------
pe = resultado[resultado["SG_UF_PROVA"] == "PE"]

print("\nPERNAMBUCO:")
print(pe.T)

# --------------------------------
# Gráfico
# --------------------------------
plt.figure(figsize=(12, 7))

sns.barplot(
    data=resultado.sort_values(
        "percentual_maior_renda",
        ascending=False
    ),
    x="percentual_maior_renda",
    y="SG_UF_PROVA"
)

plt.title("Percentual de participantes da faixa de maior renda")
plt.xlabel("% Faixa B (maior renda)")
plt.ylabel("Estado")

plt.tight_layout()
plt.show()