import math


class Grafo:
    
    
    def __init__(self, quantidadeDeVertices,capacidade_veiculo):
        
        self.quantidadeDeVertices = quantidadeDeVertices
        self.matriz_adj = [[float('inf')] * quantidadeDeVertices for _ in range(quantidadeDeVertices)]
        self.capacidade_veiculo = capacidade_veiculo
        for i in range(quantidadeDeVertices):
            self.matriz_adj[i][i] = 0

    def adiciona_aresta_Normal(self, nomeDoArquivo):
        numeroDeArestasNormais = 0
        lendo_sequencia = False
        with open(nomeDoArquivo.split('/')[-1], 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('EDGE'):
                    lendo_sequencia = True
                    continue

                if lendo_sequencia and linha.strip() != "":
                    partes = linha.strip().split()

                    if len(partes) < 4:
                        continue  

                    try:
                        esquinaDeSaida = int(partes[1])
                        esquinaDeChegada = int(partes[2])
                        custoDeTransito = int(partes[3])
                    

                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custoDeTransito
                        self.matriz_adj[esquinaDeChegada-1][esquinaDeSaida-1] = custoDeTransito
                    
                        numeroDeArestasNormais += 1
                    except ValueError as e:
                       
                        continue

                elif linha.strip() == "":
                    lendo_sequencia = False

        return numeroDeArestasNormais

        
    def adiciona_aresta_requerida(self, nomeDoArquivo):
        numeroDeArestasRequeridas = 0
        lendo_sequencia = False
        num_voltas = 1
        with open(nomeDoArquivo.split('/')[-1], 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('ReE.'):
                    lendo_sequencia = True
                    continue
                if lendo_sequencia and linha.strip().startswith(('EDGE', 'ReN.', '#', 'ARC')):
                    lendo_sequencia = False
                    continue

            # Processa as linhas de dados
                if lendo_sequencia and linha.strip() != "":
                    partes = linha.strip().split()

                    if len(partes) < 4:
                     
                        continue

                    try:
                 
                        esquinaDeSaida = int(partes[1])
                        esquinaDeChegada = int(partes[2])
                        custoDeTransito = int(partes[3])

                    # Checa se há mais de 4 partes (caso tenha demanda e custo de serviço)
                        if len(partes) >= 5:
                            demanda = int(partes[4])
                        else:
                            demanda = 0  # Se não houver demanda, assume-se que não há

                        if len(partes) >= 6:
                            custoDeServico = int(partes[5])
                        else:
                            custoDeServico = 0  
                        if self.capacidade_veiculo < demanda:
                            num_voltas = math.ceil(demanda / self.capacidade_veiculo)
                            
                        custo_total = (custoDeTransito + custoDeServico) * num_voltas
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custo_total
                        self.matriz_adj[esquinaDeChegada-1][esquinaDeSaida-1] = custo_total

                        numeroDeArestasRequeridas += 1

                    except ValueError as e:
                        
                        continue
                    
        return numeroDeArestasRequeridas
         
    def adiciona_arco_Requerido(self, nomeDoArquivo):
        numeroDeArcosRequeridos = 0
        lendo_sequencia = False
        num_voltas = 1
        with open(nomeDoArquivo.split('/')[-1], 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('ReA.'):
                    lendo_sequencia = True
                    continue

                if lendo_sequencia:
                    partes = linha.strip().split()

                # Verifica se tem ao menos 6 partes: índice, saída, chegada, custo, demanda, serviço
                    if len(partes) < 6:
                        continue

                    try:
                        esquinaDeSaida = int(partes[1])
                        esquinaDeChegada = int(partes[2])
                        custoDeTransito = int(partes[3])
                        demanda = int(partes[4])
                        custoDeServico = int(partes[5])
                        if self.capacidade_veiculo < demanda:
                            num_voltas = math.ceil(demanda / self.capacidade_veiculo)
                        custo_total = (custoDeTransito + custoDeServico) * num_voltas
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custo_total
                        numeroDeArcosRequeridos += 1
                    except ValueError:
                       
                        continue

                elif linha.startswith('NR'):
                    lendo_sequencia = False

        return numeroDeArcosRequeridos

    def adiciona_arco_Normal(self, nomeDoArquivo):
        numeroDeArcosNormais = 0
        lendo_sequencia = False
        with open(nomeDoArquivo.split('/')[-1], 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('ARC'):
                    lendo_sequencia = True
                    continue

                if lendo_sequencia:
                    partes = linha.strip().split()

                    if len(partes) < 4:
                        continue  # evita acesso inválido

                    try:
                        esquinaDeSaida = int(partes[1])
                        esquinaDeChegada = int(partes[2])
                        custoDeTransito = int(partes[3])
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custoDeTransito
                        numeroDeArcosNormais += 1
                    except ValueError:
                        continue  

                elif linha.startswith('the'):
                    lendo_sequencia = False

        return numeroDeArcosNormais        
    
    
    def mostra_matriz(self):
        for linha in self.matriz_adj:
            for valor in linha:
                if valor == float('inf'):
                    print("INF".ljust(6), end=' ')
                else:
                    print(str(valor).ljust(6), end=' ')
            print()
            
            
    def densidadeGrafo(self, nomeDoArquivo):
        parte1 = (g.adiciona_aresta_Normal(nomeDoArquivo) + g.adiciona_aresta_requerida(nomeDoArquivo))*2 + g.adiciona_arco_Normal(nomeDoArquivo) + g.adiciona_arco_Requerido(nomeDoArquivo)
        parte2 = g.quantidadeDeVertices * (g.quantidadeDeVertices - 1)
        return parte1 / parte2 if parte2 > 0 else 0

    def encontrarComponentes(self):
        esquinasVisitadas = set()
        componentes = []
        
        for esquina in range(self.quantidadeDeVertices):
            if esquina not in esquinasVisitadas:
                componente = self.buscaEmLarguraMatriz(esquina, esquinasVisitadas)
                componentes.append(componente)
                       
        return componentes
            
    def buscaEmLarguraMatriz(self, esquinaInicial, esquinasVisitadas):
        fila = []
        componente = []
        
        fila.append(esquinaInicial)
        esquinasVisitadas.add(esquinaInicial)
        
        while fila:
            esquinaAtual = fila.pop(0)
            componente.append(esquinaAtual)
            for esquinaVizinha in range(self.quantidadeDeVertices):
              
                if self.matriz_adj[esquinaAtual][esquinaVizinha] != 0 and self.matriz_adj[esquinaAtual][esquinaVizinha] != float('inf') and esquinaVizinha not in esquinasVisitadas:
                    esquinasVisitadas.add(esquinaVizinha)
                    fila.append(esquinaVizinha)
                                  
        return componente
        
    def grauMaximo(self):
        
        grauMaximoAtual = 0
        for esquinaSaida in range(self.quantidadeDeVertices):
            contEsquinas = 0
            for esquinaChegada in range(self.quantidadeDeVertices):
                if self.matriz_adj[esquinaSaida][esquinaChegada] != 0 and self.matriz_adj[esquinaSaida][esquinaChegada] != float('inf'):
                    contEsquinas += 1
                    
            if grauMaximoAtual < contEsquinas:
                grauMaximoAtual = contEsquinas
    
            
        return grauMaximoAtual
    
    def grauMinimo(self):
        
        grauMinimoAtual = float('inf')
        for esquinaSaida in range(self.quantidadeDeVertices):
            contEsquinas = 0
            for esquinaChegada in range(self.quantidadeDeVertices):
                if self.matriz_adj[esquinaSaida][esquinaChegada] != 0 and self.matriz_adj[esquinaSaida][esquinaChegada] != float('inf'):
                    contEsquinas += 1
                    
            if grauMinimoAtual > contEsquinas:
                grauMinimoAtual = contEsquinas
            
        return grauMinimoAtual
    
    def floyd_warshall(self):
        matriz_dist = [row[:] for row in self.matriz_adj]  
        matriz_pred = [[-1 if i == j or self.matriz_adj[i][j] == float('inf') else i 
                        for j in range(self.quantidadeDeVertices)] 
                    for i in range(self.quantidadeDeVertices)]
        

        for k in range(self.quantidadeDeVertices):
            for i in range(self.quantidadeDeVertices):
                for j in range(self.quantidadeDeVertices):
                    if matriz_dist[i][k] + matriz_dist[k][j] < matriz_dist[i][j]:
                        matriz_dist[i][j] = matriz_dist[i][k] + matriz_dist[k][j]
                        matriz_pred[i][j] = matriz_pred[k][j]


        return matriz_dist, matriz_pred


    def intermediacao(self, matriz_pred):
        inter = [0] * self.quantidadeDeVertices
        for k in  range(self.quantidadeDeVertices):
            for i in range(self.quantidadeDeVertices):
                for j in range(self.quantidadeDeVertices):
                    if i != j:
                        if matriz_pred[i][j] == k:
                            inter[k] += 1
                    

        return inter
    
    def imprimir_matriz(self, matriz):
        for linha in matriz:
            for valor in linha:
                if valor == float('inf'):
                    print("INF".ljust(6), end=' ')
                else:
                    print(str(valor).ljust(6), end=' ')
                    
            print()


    def caminho_medio(self, matriz_dist):
        soma = 0
        count = 0
        for i in range(self.quantidadeDeVertices):
            for j in range(self.quantidadeDeVertices):
                if i != j and matriz_dist[i][j] != float('inf'):
                    soma += matriz_dist[i][j]
                    count += 1

        return soma / count if count > 0 else 0


    def diametroDoGrafo(self):
        matriz_dist, _ = self.floyd_warshall() #pega só a matriz de distancias e ignora o segundo retorno da floyd warshall (matriz predeceçora)
        diametro = 0

        for i in range(self.quantidadeDeVertices):
            for j in range(self.quantidadeDeVertices):
                if i != j and matriz_dist[i][j] != float('inf'):
                    diametro = max(diametro, matriz_dist[i][j])

        return diametro
        

def quantidadeDeVertices(nomeDoArquivo):
    verticesDiferentes = []
    lendo_sequencia = False  # flag para indicar que estamos em uma seção de dados
    with open(nomeDoArquivo.split('/')[-1], 'r') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas[:-1]:
            linha = linha.strip()

            if linha.startswith(('ReE.', 'EDGE', 'ReA.', 'ARC')):
                lendo_sequencia = True
                continue  

            # Se estamos em uma seção válida, e a linha não está vazia
            if lendo_sequencia and linha != "":
                partes = linha.split()

                if partes[1] not in verticesDiferentes:
                    verticesDiferentes.append(partes[1])
                if partes[2] not in verticesDiferentes:
                    verticesDiferentes.append(partes[2])
                    

            elif linha == "":
                lendo_sequencia = False

    return len(verticesDiferentes)


def quantidadeDeVerticesRequeridos(nomeDoArquivo):
    qntLinhas = 0
    lendo_sequencia = False
    
    with open(nomeDoArquivo.split('/')[-1], 'r') as arquivo:
        for linha in arquivo:

            if linha.startswith('ReN.'):
                lendo_sequencia = True
                continue
 
            if lendo_sequencia and linha.strip() != "":
                qntLinhas += 1

            elif linha.strip() == "":
                lendo_sequencia = False
                
    return qntLinhas


def capacidadeDosVeiculos(nomeDoArquivo):
   
    with open(nomeDoArquivo.split('/')[-1], 'r') as arquivo:
        for linha in arquivo:
            if linha.startswith('Capacity:'):
                partes = linha.strip().split()
                capacidade = int(partes[1])
                
    return capacidade



arquivo = "BHW1.dat"    
        
g = Grafo(quantidadeDeVertices(arquivo),capacidadeDosVeiculos(arquivo))

