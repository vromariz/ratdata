import pandas as pd

arquivo = "/home/vinicius/Downloads/microdados_enem_2024/DADOS/RESULTADOS_2024.csv"

colunas = [
    "SG_UF_PROVA",
    "CO_PROVA_MT"
]

print("Lendo dados...")

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin1",
    usecols=colunas,
    low_memory=False
)

df = df[
    df["SG_UF_PROVA"] == "PE"
].copy()

print("Quantidade total PE:", len(df))

mapa_provas = {
    "AZUL": 1407,
    "AMARELA": 1408,
    #"VERDE": 1409,
    #"CINZA": 1410,
    #"VERDE2": 1411,
    #"VERDE3": 1412,
    #"LARANJA": 1413,
    #"LARANJA2": 1414,
    #"ROXA": 1415,
    #"ROXA2": 1416,
    #"ROXA3": 1417,
    #"LEITOR TELA": 1418
}

resultado = []

for nome_cor, codigo_prova in mapa_provas.items():

    quantidade = (
        df["CO_PROVA_MT"] == codigo_prova
    ).sum()

    print(f"{nome_cor}: {quantidade}")

    resultado.append({
        "COR": nome_cor,
        "CO_PROVA_MT": codigo_prova,
        "QUANTIDADE": quantidade
    })

df_final = pd.DataFrame(resultado)

print("\nRESULTADO FINAL\n")
print(df_final)

saida = "/home/vinicius/Downloads/quantidade_provas_pe.csv"

df_final.to_csv(
    saida,
    sep=";",
    index=False
)

print("\nArquivo salvo em:")
print(saida)