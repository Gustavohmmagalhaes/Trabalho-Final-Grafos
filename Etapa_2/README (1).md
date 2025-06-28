# Objetivo 📌

Esse projeto tem como objetivo solucionar um problema de logística, visando otimizar o fluxo de bens e serviços, resultando em maior eficiencia e redução de custos no transporte, através de estruturas de dados baseadas em grafos.

# Ferramentas 💻

Utilizamos a linguagem de programação Python e o Google Colab para visualização das informações.

# Descrição das funções 📜

- Primeiramente temos um construtor __init__ que salva o número de vértices, cria uma matriz de adjacência (matriz_adj) com float('inf'), representando que inicialmente não há conexões entre os vértices e define a diagonal da matriz como 0.
  
- adiciona_aresta_Normal(self, nomeDoArquivo): Lê as arestas normais a partir do arquivo a partir da seção iniciada por 'EDGE'. Cada linha válida é tratada como uma aresta entre dois vértices com um custo de trânsito. A matriz é atualizada simetricamente.
  
- adiciona_aresta_requerida(self, nomeDoArquivo): Lê as arestas requeridas a partir da seção 'ReE.'. Considera o custo de trânsito e, se disponível, o custo de serviço, somando ambos para atualizar a matriz de adjacência simetricamente.
  
- adiciona_arco_Requerido(self, nomeDoArquivo): Lê os arcos direcionados requeridos da seção 'ReA.', atualizando a matriz apenas no sentido da aresta (de saída para chegada). Também soma o custo de trânsito com o de serviço.

- adiciona_arco_Normal(self, nomeDoArquivo): Adiciona arcos normais (sem demanda ou serviço) da seção 'ARC', atualizando a matriz apenas na direção do arco (de saída para chegada.

- quantidadeDeArestas(self, nomeDoArquivo):; quantidadeDeArestasRequeridas(self, nomeDoArquivo):; quantidadeDeArcosRequeridos(self, nomeDoArquivo):; quantidadeDeArcos(self, nomeDoArquivo): Cada um desses métodos lê o cabeçalho do arquivo para retornar as quantidades declaradas de arestas e arcos (normais ou requeridos).

- mostra_matriz(self): Exibe a matriz de adjacência do grafo.

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

- quantidadeDeVertices(nomeDoArquivo): Função externa à classe que retorna a quantidade de vértices do grafo com base na linha iniciada por #Nodes: no arquivo.

- quantidadeDeVerticesRequeridos(nomeDoArquivo): Lê o arquivo e extrai a quantidade de vértices requeridos presentes na seção 'ReN.' do arquivo.

- verticesRequeridos(nomeDoArquivo): Retorna um conjunto com os números dos vértices requeridos, extraídos da seção que começa com 'ReN.'.

- arestasRequeridas(arquivo): Retorna um conjunto de arestas requeridas, extraídas da seção que começa com 'ReE.'.

- arcosRequeridos(arquivo): Retorna um conjunto de arcos requeridos, da seção 'ReA.'.

- contar_elementos_requeridos(matriz_adjacencia): Conta o número de elementos positivos (> 0) na matriz de adjacência — ou seja, quantas arestas possuem peso positivo no grafo.

- construir_rotas_ordenadas(g, capacidade_maxima_veiculo, no_inicial, debug): Constrói rotas ordenadas para veículos partindo de um nó inicial, atendendo a serviços obrigatórios (arestas, nós ou arcos com demanda) presentes no grafo g. O processo é iterativo, terminando quando todos os serviços obrigatórios são coletados, respeitando a capacidade do veículo. Se a demanda exceder a capacidade, encerra a rota e volta ao depósito.

- coletar_servico_no(vertice): Coleta serviços se encontrar no caminho, verificando se a capacidade do veículo será excedida, coletando também demandas de nós (serviços no nó).

- ler_capacidade(nome_arquivo): Lê a capacidade máxima do veículo a partir de um arquivo de entrada.

- executar_testes_em_pastas(pasta_testes, pasta_saida):  executa testes automatizados, criando a pasta de saída se não existir, percorre todos os arquivos '.dat' da pasta de testes. Para cada arquivo: carrega os dados do grafo, lê a capacidade do veículo, executa o algoritmo de construção de rotas, salva os resultados em um arquivo '.dat' formatado na pasta de saída.

  
# Manual de uso 

- Instale todas as bibliotecas incluindo a pip install pandas matplotlib networkx, para o arquivo de visualização.
- Certifique-se de ter Etapa2_TrabalhoFina.py e a pasta de arquivos de testes (ou arquivos de testes individuais) no mesmo diretório.
- Abra o arquivo '.py' e altere o nome da sua pasta de resultados de saida (se quiser).
- Para executar todos os arquivos de testes juntos, apenas execute "python <Etapa2_TrabalhoFinal.py <nome_pasta>".
- Para executar apenas um arquivo por vez, execute "python Etapa2_TrabalhoFinal.py <nome_arquivo>".
