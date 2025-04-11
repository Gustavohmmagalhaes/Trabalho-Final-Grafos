import math


class Grafo:
    
    
    def __init__(self, quantidadeDeVertices):
        
        self.quantidadeDeVertices = quantidadeDeVertices
        self.matriz_adj = [[float('inf')] * quantidadeDeVertices for _ in range(quantidadeDeVertices)]
       
        for i in range(quantidadeDeVertices):
            self.matriz_adj[i][i] = 0

    def adiciona_aresta_Normal(self, nomeDoArquivo):
        
        lendo_sequencia = False
        with open(nomeDoArquivo, 'r') as arquivo:
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
                    
                        
                    except ValueError as e:
                       
                        continue

                elif linha.strip() == "":
                    lendo_sequencia = False
                    
    def quantidadeDeArestas(self, nomeDoArquivo):
        
        with open(nomeDoArquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('#Edges:'):
                    partes =linha.strip().split()
                    try:
                        qntArestas = int(partes[1])
                        
                    except ValueError as e:
                       
                        continue
    
        return qntArestas


        
    def adiciona_aresta_requerida(self, nomeDoArquivo):
      
        lendo_sequencia = False
      
        with open(nomeDoArquivo, 'r') as arquivo:
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

                        if len(partes) >= 6:
                            custoDeServico = int(partes[5])
                        else:
                            custoDeServico = 0  
                       
                        custo_total = (custoDeTransito + custoDeServico)
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custo_total
                        self.matriz_adj[esquinaDeChegada-1][esquinaDeSaida-1] = custo_total

                

                    except ValueError as e:
                        
                        continue
                    
    def quantidadeDeArestasRequeridas(self, nomeDoArquivo):
        
        with open(nomeDoArquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('#Required E:'):
                    partes =linha.strip().split()
                    try:
                        qntArestasRequeridas = int(partes[2])
                        
                    except ValueError as e:
                       
                        continue
    
        return qntArestasRequeridas
                    

    def adiciona_arco_Requerido(self, nomeDoArquivo):
   
        lendo_sequencia = False

        with open(nomeDoArquivo, 'r') as arquivo:
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
                  
                        custoDeServico = int(partes[5])
                     
                        custo_total = (custoDeTransito + custoDeServico)
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custo_total
                 
                    except ValueError:
                       
                        continue

                elif linha.startswith('NR'):
                    lendo_sequencia = False

    def quantidadeDeArcosRequeridos(self, nomeDoArquivo):
        
        with open(nomeDoArquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('#Required A:'):
                    partes =linha.strip().split()
                    try:
                        qntArcosRequeridos = int(partes[2])
                        
                    except ValueError as e:
                       
                        continue
    
        return qntArcosRequeridos

    def adiciona_arco_Normal(self, nomeDoArquivo):
        
        lendo_sequencia = False
        with open(nomeDoArquivo, 'r') as arquivo:
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
                  
                    except ValueError:
                        continue  

                elif linha.startswith('the'):
                    lendo_sequencia = False

          
    def quantidadeDeArcos(self, nomeDoArquivo):
        
        with open(nomeDoArquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('#Arcs:'):
                    partes =linha.strip().split()
                    try:
                        qntArcos = int(partes[1])
                        
                    except ValueError as e:
                       
                        continue
    
        return qntArcos
    
    def mostra_matriz(self):
        for linha in self.matriz_adj:
            for valor in linha:
                if valor == float('inf'):
                    print("INF".ljust(6), end=' ')
                else:
                    print(str(valor).ljust(6), end=' ')
            print()
            
            
    def densidadeGrafo(self, nomeDoArquivo):
        parte1 = (self.quantidadeDeArestas(nomeDoArquivo) + self.quantidadeDeArestasRequeridas(nomeDoArquivo))*2 + self.quantidadeDeArcos(nomeDoArquivo) + self.quantidadeDeArcosRequeridos(nomeDoArquivo)
        parte2 = self.quantidadeDeVertices * (self.quantidadeDeVertices - 1)
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
        
        with open(nomeDoArquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('#Nodes:'):
                    partes =linha.strip().split()
                    try:
                        qntVertices = int(partes[1])
                        
                    except ValueError as e:
                       
                        continue
    
        return qntVertices


def quantidadeDeVerticesRequeridos(nomeDoArquivo):
        
        with open(nomeDoArquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('#Required N:'):
                    partes =linha.strip().split()
                    try:
                        qntVerticesRequeridos = int(partes[2])
                        
                    except ValueError as e:
                       
                        continue
    
        return qntVerticesRequeridos
    
    
def verticesRequeridos(nomeDoArquivo):
    vertices = set()
    lendo = False

    with open(nomeDoArquivo, 'r') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if linha.startswith('ReN.'):
                lendo = True
                continue
            if lendo and linha:
                partes = linha.split()
                if partes:
                    rotulo = partes[0]
                    if rotulo.startswith('N') and rotulo[1:].isdigit():
                        numero = int(rotulo[1:])
                        vertices.add(numero)
                    else:
                        continue


    return vertices


def arestasRequeridas(arquivo):
    arestas = set()
    with open(arquivo, 'r') as f:
        lines = f.readlines()

    lendo = False
    for line in lines:
        line = line.strip()
        if line.startswith("ReE."):
            lendo = True
            continue
        if lendo:
            if line == "":  # Parar ao chegar em ARCS
                break
            partes = line.split()
            if len(partes) >= 2:
                u, v = int(partes[1]), int(partes[2])
                arestas.add((min(u, v), max(u, v)))  # Evita duplicidade tipo (2,3) e (3,2)

    return arestas


def arcosRequeridos(arquivo):
    arcos = set()
    with open(arquivo, 'r') as f:
        lines = f.readlines()

    lendo = False
    for line in lines:
        line = line.strip()
        if line.startswith("ReA."):
            lendo = True
            continue
        if lendo:
            if line == "":  # Parar ao chegar em outra seção
                break
            partes = line.split()
            if len(partes) >= 2:
                u, v = int(partes[1]), int(partes[2])
                arcos.add((u, v))  # Ordem importa em arco

    return arcos