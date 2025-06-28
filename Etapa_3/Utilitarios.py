def imprimir_dicionario(dados):
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")


def reconstruir_caminho(pred, origem, destino):
    caminho = []
    cur = destino
    
    if origem == destino:
        return [origem] 
    
    if origem < 0 or origem >= len(pred) or \
       destino < 0 or destino >= len(pred[0]) or \
       pred[origem][destino] == -1:
        return []
    
    while cur != origem:
        caminho.append(cur)
        
        if pred[origem][cur] == -1:
            return [] 
        cur = pred[origem][cur]
        
        if cur == -1: 
            return []
            
    caminho.append(origem)
    caminho.reverse()
    return caminho
