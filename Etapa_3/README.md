# Objetivo 📌
Esse projeto tem como objetivo solucionar um problema de logística, visando otimizar o fluxo de bens e serviços, resultando em maior eficiencia e redução de custos no transporte, através de estruturas de dados baseadas em grafos.

# Ferramentas 💻
Utilizamos a linguagem de programação Python e o Google Colab para visualização das informações.

# Descrição das funções 📜
- Primeiramente temos um construtor init que salva o número de vértices, cria uma matriz de adjacência (matriz_adj) com float('inf'), representando que inicialmente não há conexões entre os vértices e define a diagonal da matriz como 0.

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

- executar_testes_em_pastas(pasta_testes, pasta_saida): executa testes automatizados, criando a pasta de saída se não existir, percorre todos os arquivos '.dat' da pasta de testes. Para cada arquivo: carrega os dados do grafo, lê a capacidade do veículo, executa o algoritmo de construção de rotas, salva os resultados em um arquivo '.dat' formatado na pasta de saída.

- coletar_servico_no(vertice, ...): coleta serviços do tipo nó presentes no vértice atual, respeitando a capacidade do veículo. Atualiza o trajeto e remove o serviço da lista.

- encontrar_servico_mais_proximo(servicos_restantes, no_atual, dist_total, ...): seleciona o próximo serviço obrigatório mais próximo (nó, aresta ou arco), considerando a soma da distância e custo de serviço como critério guloso.

- mover_e_coletar(no_atual, destino, ...): reconstrói o caminho entre dois vértices e coleta serviços de arestas/arcos no trajeto, respeitando a capacidade e atualizando o custo total da rota.

- reconstruir_caminho(pred, origem, destino): reconstrói o caminho mais curto entre dois nós com base na matriz de predecessores do algoritmo de Floyd-Warshall

- extrair_sequencia_nos_rota(rota_original, no_inicial): gera a sequência de nós visitados em uma rota original, usada para aplicar otimização posterior (como 2-opt).

- calcular_custo_caminho(caminho, dist_total): soma os custos de transporte entre nós consecutivos em uma sequência.

- two_opt_swap(caminho, i, k): executa uma operação de 2-opt, invertendo o trecho do caminho entre os índices i e k para tentar melhorar a rota.

- otimizar_rota_2opt(sequencia_nos, dist_total): aplica o algoritmo 2-opt para otimizar a ordem de visita aos nós, reduzindo o custo total do trajeto.

- recalcular_custo_total_rota_otimizada(...): recalcula o custo total da rota otimizada (apenas deslocamento entre nós), usando a matriz de distâncias.

- ler_no_inicial(nome_arquivo): lê o arquivo de entrada e retorna o número do nó correspondente ao depósito inicial, identificado pela linha que começa com Depot node: (insensível a maiúsculas/minúsculas). Caso a linha não seja encontrada ou contenha erro, retorna o valor padrão 1.

- imprimir_dicionario(dados): exibe no terminal todas as chaves e valores de um dicionário passado como argumento, formatando cada par como chave: valor. Útil para inspeção e depuração de dados estruturados.


# Manual de uso
- Instale todas as bibliotecas incluindo a pip install pandas matplotlib networkx, para o arquivo de visualização.

- Certifique-se de ter Grafo.py, Leitor_dados.py, Main.py, Otimizacao.py, Solucao.py, Utilitarios.py e a pasta de arquivos de testes (ou arquivos de testes individuais) no mesmo diretório (Etapa_3).

- Para executar todos os arquivos de testes juntos, apenas execute "python Main.py <nome_pasta>".

- Para executar apenas um arquivo por vez, execute "python Main.py <nome_arquivo.dat>".
