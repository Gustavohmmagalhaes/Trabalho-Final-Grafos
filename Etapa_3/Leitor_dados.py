import os

def ler_capacidade(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        for linha in f:
            if linha.strip().startswith('Capacity:'):
                partes = linha.strip().split()
                if len(partes) >= 2:
                    return int(partes[1])
    return None

def quantidadeDeVertices(nomeDoArquivo):
    with open(nomeDoArquivo, 'r') as arquivo:
        for linha in arquivo:
            if linha.startswith('#Nodes:'):
                partes = linha.strip().split()
                try:
                    return int(partes[1])
                except ValueError:
                    continue
    raise ValueError("Número de vértices não encontrado no arquivo.")

def ler_no_inicial(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        for linha in f:
            if linha.strip().lower().startswith('depot node:'):
                partes = linha.strip().split()
                try:
                    return int(partes[-1])
                except ValueError:
                    continue
    return 1 
