class Grafo:
    def __init__(self, quantidadeDeVertices):
        
        self.quantidadeDeVertices = quantidadeDeVertices
        self.matriz_adj = [[float('inf')] * quantidadeDeVertices for _ in range(quantidadeDeVertices)]
        
        self.elementos_requeridos = {}
        self.indice_requerido = 1 
       
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

                if lendo_sequencia and linha.strip() != "":
                    partes = linha.strip().split()

                    if len(partes) < 4: 
                        continue

                    try:
                        esquinaDeSaida = int(partes[1])
                        esquinaDeChegada = int(partes[2])
                        custoDeTransito = int(partes[3])
                        demanda = int(partes[4])

                        if len(partes) >= 6:
                            custoDeServico = int(partes[5])
                        else:
                            custoDeServico = 0  
                       
                        custo_total = custoDeTransito
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custo_total
                        self.matriz_adj[esquinaDeChegada-1][esquinaDeSaida-1] = custo_total
                        
                        self.elementos_requeridos[self.indice_requerido] = {
                            'tipo': 'aresta',
                            'de': esquinaDeSaida,
                            'para': esquinaDeChegada,
                            'demanda': demanda,
                            'custo-servico': custoDeServico
                        }
                        
                        self.indice_requerido += 1
                
                    except ValueError as e:
                        
                        continue
                    

    def adiciona_arco_Requerido(self, nomeDoArquivo):
   
        lendo_sequencia = False

        with open(nomeDoArquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('ReA.'):
                    lendo_sequencia = True
                    continue

                if lendo_sequencia:
                    partes = linha.strip().split()

                    if len(partes) < 6:
                        continue

                    try:
                        esquinaDeSaida = int(partes[1])
                        esquinaDeChegada = int(partes[2])
                        custoDeTransito = int(partes[3])
                        demanda = int(partes[4])
                        custoDeServico = int(partes[5])
                     
                        custo_total = custoDeTransito
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custo_total
                                    
                        self.elementos_requeridos[self.indice_requerido] = {
                            'tipo': 'arco',
                            'de': esquinaDeSaida,
                            'para': esquinaDeChegada,
                            'demanda': demanda,
                            'custo-servico': custoDeServico
                        }
                       
                        self.indice_requerido += 1
                        
                    except ValueError:
                       
                        continue

                elif linha.startswith('NR'):
                    lendo_sequencia = False


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
                    
    def adiciona_nos_requeridos(self, nomeDoArquivo):
        lendo_sequencia = False
        self.nos_requeridos = {}

        with open(nomeDoArquivo, 'r') as arquivo:
            for linha in arquivo:
                if linha.startswith('ReN.'):
                    lendo_sequencia = True
                    continue

                if lendo_sequencia:
                    if linha.strip().startswith(('ReE.', 'ReA.', 'ARC', '#', 'EDGE')):
                        return self.nos_requeridos

                    partes = linha.strip().split()

                    if len(partes) < 3:
                        continue 

                    try:
                        no = int(partes[0][1:])
                        demanda = int(partes[1])
                        custoDeServico = int(partes[2])
                        self.elementos_requeridos[self.indice_requerido] = {
                            'tipo': 'no',
                            'de': no,
                            'para': no,
                            'demanda': demanda,
                            'custo-servico': custoDeServico
                        }
                        self.indice_requerido += 1
                        
                    except ValueError:
                        continue

    
    def mostra_matriz(self):
        for linha in self.matriz_adj:
            for valor in linha:
                if valor == float('inf'):
                    print("INF".ljust(6), end=' ')
                else:
                    print(str(valor).ljust(6), end=' ')
            print()
            
    
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
    

    def imprimir_matriz(self, matriz):
        for linha in matriz:
            for valor in linha:
                if valor == float('inf'):
                    print("INF".ljust(6), end=' ')
                else:
                    print(str(valor).ljust(6), end=' ')
                    
            print()
            
    def get_indice_requerido(self, de, para):
        for indice, dados in self.elementos_requeridos.items():
            if dados['de'] == de and dados['para'] == para:
                return indice
        return None 
    
    def get_demanda_aresta(self, de, para):
        for dados in self.elementos_requeridos.values():
            if dados['tipo'] == 'aresta':
                if (dados['de'] == de and dados['para'] == para) or (dados['de'] == para and dados['para'] == de):
                    return dados.get('demanda', 0)
        return 0 
    
    def get_demanda_normal(self, de, para):
        for dados in self.elementos_requeridos.values():
                if (dados['de'] == de and dados['para'] == para):
                    return dados.get('demanda', 0)
        return 0 
            

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