def imprimir_dicionario(dados):
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")


def reconstruir_caminho(pred, origem, destino):
    caminho = []
    cur = destino
    while cur != origem:
        caminho.append(cur)
        cur = pred[origem][cur]
        if cur == -1:
            return []
    caminho.append(origem)
    caminho.reverse()
    return caminho


def ler_capacidade(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        for linha in f:
            if linha.strip().startswith('Capacity:'):
                partes = linha.strip().split()
                if len(partes) >= 2:
                    return int(partes[1])
    return None
