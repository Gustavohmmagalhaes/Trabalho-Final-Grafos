# Objetivo 📌

Esse projeto tem como objetivo solucionar um problema de logística, visando otimizar o fluxo de bens e serviços, resultando em maior eficiencia e redução de custos no transporte, através de estruturas de dados baseadas em grafos.

# Ferramentas 💻

Utilizamos a linguagem de programação Python.

# Descrição das funções 📜

- Primeiramente temos um construtor __init__ que salva o número de vértices e a capacidade do veículo, cria uma matriz de adjacência (matriz_adj) com float('inf'), representando que inicialmente não há conexões entre os vértices e define a diagonal da matriz como 0.
  
- adiciona_aresta_Normal(self, nomeDoArquivo): Lê um arquivo e adiciona as arestas normais ao grafo. Procura pela linha que começa com 'EDGE' para começar a leitura das arestas e cada linha seguinte com pelo menos 4 elementos é interpretada como uma aresta com vértice de saída, vértice de chegada e custo de trânsito. Então ela atualiza a matriz de adjacência com o custo da aresta (simétrico nos dois sentidos) e retorna o número de arestas normais adicionadas.
  
- adiciona_aresta_requerida(self, nomeDoArquivo): Lê um arquivo e adiciona as arestas requeridas (que possuem demanda e custo de serviço). Inicia a leitura quando encontra uma linha que começa com 'ReE.', ignorando as linhas que indicam o fim da seção ou que não são relevantes, calcula o número de viagens necessárias com base na capacidade do veículo e na demanda, atualiza a matriz de adjacência com o custo total da aresta e retorna o número de arestas requeridas.
  
- adiciona_arco_Requerido(self, nomeDoArquivo): Adiciona arcos direcionados requeridos (com demanda e custo de serviço) ao grafo. Começa a leitura ao encontrar a linha que inicia com 'ReA.', calcula o número de viagens necessárias com base na capacidade do veículo, calcula o custo total do arco, atualiza a matriz de adjacência apenas na direção especificada (de saída para chegada) e retorna o número de arcos requeridos adicionados.

- adiciona_arco_Normal(self, nomeDoArquivo): Adiciona arcos direcionados normais (sem demanda nem serviço) ao grafo. Começa a leitura ao encontrar a linha que inicia com 'ARC', atualiza a matriz de adjacência somente na direção do arco (de saída para chegada) e retorna o número de arcos normais adicionados.

- mostra_matriz(self): Exibe a matriz de adjacência do garfo.

- densidadeGrafo(self, nomeDoArquivo): Calcula a densidade do grafo, ou seja, o quão "conectado" ele está. Usa as funções que adicionam arestas e arcos (normais e requeridos) para contar o número total de ligações e divide esse total pelo número máximo possível de ligações em um grafo direcionado.

- encontrarComponentes(self): Identifica todas as componentes conexas do grafo. Para cada vértice ainda não visitado, faz uma busca em largura para descobrir todos os vértices conectados a ele. Cada grupo de vértices conectados forma uma componente e retorna uma lista com todas as componentes encontradas (cada uma como uma lista de vértices).

- buscaEmLarguraMatriz(self, esquinaInicial, esquinasVisitadas): Executa a busca em largura (BFS) a partir de um vértice inicial.

- grauMaximo(self): Determina o grau máximo entre todos os vértices do grafo.

- grauMinimo(self): Determina o grau mínimo entre todos os vértices do grafo.

- floyd_warshall(self): Calcula os menores caminhos entre todos os pares de vértices no grafo. Cria uma cópia da matriz de adjacência (matriz_dist) para armazenar as distâncias mínimas, inicializa a matriz de predecessores (matriz_pred) com base nos vizinhos diretos e retorna uma matriz de distancia com os menores custos e uma matriz de predecessores.

- intermediacao(self, matriz_pred): Calcula a centralidade de intermediação de cada vértice e retorna uma lista com a quantidade de vezes que cada vértice atua como intermediário.

- caminho_medio(self, matriz_dist): Calcula o comprimento médio dos caminhos mínimos entre todos os pares de vértices e retorna a média dos menores caminhos.

- diametroDoGrafo(self): Determina o diâmetro do grafo, ou seja, o maior entre os menores caminhos possíveis.

- imprimir_matriz(self, matriz): Exibe uma matriz (como a de distâncias ou predecessores) de forma legível no terminal e tem como saída Uma tabela organizada.

- quantidadeDeVertices(nomeDoArquivo): Conta o número de vértices distintos (esquinas) presentes nas seções de arestas e arcos do arquivo.

- quantidadeDeVerticesRequeridos(nomeDoArquivo):  Conta quantas arestas requeridas estão presentes na seção ReN. do arquivo.

- capacidadeDosVeiculos(nomeDoArquivo): Extrai a capacidade dos veículos a partir do arquivo de entrada e retorna um número inteiro representando a capacidade máxima de carga de um veículo.
