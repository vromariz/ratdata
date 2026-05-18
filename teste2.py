import pandas as pd

arquivo = "/home/vinicius/Downloads/microdados_enem_2024/DADOS/RESULTADOS_2024.csv"

colunas = [
    "SG_UF_PROVA",
    "CO_PROVA_MT",
    "TX_RESPOSTAS_MT",
    "TX_GABARITO_MT"
]

print("Lendo dados...")

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin1",
    usecols=colunas,
    low_memory=False
)

# filtro do estado

df = df[
    df["SG_UF_PROVA"] == "PI"
].copy()

print("Quantidade:", len(df))

# editar esse filtro das provas para pegar todas 1407-1418

mapa_provas = {
    "AZUL": 1407,
    "AMARELA": 1408,
    "VERDE": 1409,
    "CINZA": 1410,
    #"VERDE2": 1411,
    #"VERDE3": 1412,
    #"LARANJA": 1413,
    #"LARANJA2": 1414,
    #"ROXA": 1415,
    #"ROXA2": 1416,
    #"ROXA3": 1417,
    #"LEITOR TELA": 1418
}

# posicao editar que é o mais errado, olhar no excel

itens_por_cor = {
    "AZUL": [138, 169, 180, 165],
    "AMARELA": [165, 149, 139, 140],
    "VERDE": [156, 171, 164, 174],
    "CINZA": [148, 149, 141, 151],
    #"VERDE2": [156, 171, 164, 174],
    #"VERDE3": [156, 171, 164, 174],
    #"LARANJA": [156, 171, 164, 174],
    #"LARANJA2": [156, 171, 164, 174],
    #"ROXA": [156, 171, 164, 174],
    #"ROXA2": [156, 171, 164, 174],
    #"ROXA3": [156, 171, 164, 174],
    #"LEITOR TELA": [156, 171, 164, 174]
}

# posicao 136 -> índice 0
# posicao 180 -> índice 44
# somando 45 posicoes

def pegar_letra(texto, posicao):

    if pd.isna(texto):
        return None

    texto = str(texto)

    indice = posicao - 136

    if indice < 0 or indice >= len(texto):
        return None

    return texto[indice]

resultado = []

for cor, posicoes in itens_por_cor.items():

    codigo_prova = mapa_provas[cor]

    print(f"\nProcessando {cor}...")

    df_cor = df[
        df["CO_PROVA_MT"] == codigo_prova
    ]

    total_validos = 0
    total_acertos = 0

    for row in df_cor.itertuples(index=False):

        respostas = row.TX_RESPOSTAS_MT
        gabarito = row.TX_GABARITO_MT

        if pd.isna(respostas) or pd.isna(gabarito):
            continue

        respondeu_todas = True
        acertou_todas = True

        for posicao in posicoes:

            r = pegar_letra(respostas, posicao)
            g = pegar_letra(gabarito, posicao)

            # não respondeu
            if r in [None, ".", "*"]:
                respondeu_todas = False
                break

            # errou
            if r != g:
                acertou_todas = False

        if respondeu_todas:

            total_validos += 1

            if acertou_todas:
                total_acertos += 1

    porcentagem = 0

    if total_validos > 0:
        porcentagem = (
            total_acertos / total_validos
        ) * 100

    resultado.append({
        "COR": cor,
        "TOTAL_VALIDOS": total_validos,
        "ACERTARAM_4": total_acertos,
        "PORCENTAGEM": round(porcentagem, 4)
    })

df_final = pd.DataFrame(resultado)

print("\nRESULTADO FINAL\n")
print(df_final)

saida = "/home/vinicius/Downloads/resultado_mt_pi4.csv"

df_final.to_csv(
    saida,
    sep=";",
    index=False
)

print("\nArquivo salvo em:")
print(saida)