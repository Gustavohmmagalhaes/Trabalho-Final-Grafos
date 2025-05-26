class Grafo:
    
    def __init__(self, quantidadeDeVertices):
        
        self.quantidadeDeVertices = quantidadeDeVertices
        self.matriz_adj = [[float('inf')] * quantidadeDeVertices for _ in range(quantidadeDeVertices)]
        self.matriz_adj_retorno = [[float('inf')] * quantidadeDeVertices for _ in range(quantidadeDeVertices)]
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
                        self.matriz_adj_retorno[esquinaDeSaida-1][esquinaDeChegada-1] = custoDeTransito
                        self.matriz_adj_retorno[esquinaDeChegada-1][esquinaDeSaida-1] = custoDeTransito
                    
                        
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

            # Processa as linhas de dados
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
                       
                        custo_total = (custoDeTransito + custoDeServico)
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custo_total
                        self.matriz_adj[esquinaDeChegada-1][esquinaDeSaida-1] = custo_total
                        self.matriz_adj_retorno[esquinaDeSaida-1][esquinaDeChegada-1] = custoDeTransito
                        self.matriz_adj_retorno[esquinaDeChegada-1][esquinaDeSaida-1] = custoDeTransito
                        
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

                # Verifica se tem ao menos 6 partes: índice, saída, chegada, custo, demanda, serviço
                    if len(partes) < 6:
                        continue

                    try:
                        esquinaDeSaida = int(partes[1])
                        esquinaDeChegada = int(partes[2])
                        custoDeTransito = int(partes[3])
                        demanda = int(partes[4])
                        custoDeServico = int(partes[5])
                     
                        custo_total = (custoDeTransito + custoDeServico)
                        self.matriz_adj[esquinaDeSaida-1][esquinaDeChegada-1] = custo_total
                        self.matriz_adj_retorno[esquinaDeSaida-1][esquinaDeChegada-1] = custoDeTransito
                        
                        
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
                        self.matriz_adj_retorno[esquinaDeSaida-1][esquinaDeChegada-1] = custoDeTransito
                  
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
                    # Encerra se chegar em outra seção
                    if linha.strip().startswith(('ReE.', 'ReA.', 'ARC', '#', 'EDGE')):
                        return self.nos_requeridos  # Retorna aqui ao detectar outra seção

                    partes = linha.strip().split()

                    if len(partes) < 3:
                        continue  # pula linhas mal formatadas

                    try:
                        # Remove o 'N' e converte para inteiro
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

        return self.nos_requeridos  # Caso não encontre outra seção, retorna no final

    
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
    
    def floyd_warshall_retorno(self):
        matriz_dist = [row[:] for row in self.matriz_adj_retorno]  
        matriz_pred = [[-1 if i == j or self.matriz_adj_retorno[i][j] == float('inf') else i 
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
        return None  # se não encontrar
    
    def get_demanda_aresta(self, de, para):
    # Tenta buscar a demanda do sentido direto
        for dados in self.elementos_requeridos.values():
            if dados['tipo'] == 'aresta':
                if (dados['de'] == de and dados['para'] == para) or (dados['de'] == para and dados['para'] == de):
                    return dados.get('demanda', 0)
        return 0  # se não encontrar a aresta
    
    def get_demanda_normal(self, de, para):
    # Tenta buscar a demanda do sentido direto
        for dados in self.elementos_requeridos.values():
                if (dados['de'] == de and dados['para'] == para):
                    return dados.get('demanda', 0)
        return 0  # se não encontrar a aresta
            


def contar_elementos_requeridos(matriz_adjacencia):
        total = 0
        tamanho = len(matriz_adjacencia)
        
        for i in range(tamanho):
            for j in range(tamanho):
                if matriz_adjacencia[i][j] > 0:
                    total += 1
        
        return total


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


def imprimir_dicionario(dados):
    for chave, valor in dados.items():
        print(f"{chave}: {valor}")


def construir_rotas_ordenadas(g: "Grafo", capacidade_maxima_veiculo: int, no_inicial: int, debug=False):
    import copy, time

    custo_total_global = 0
    rotas_formatadas = []
    servicos_restantes = copy.deepcopy(g.elementos_requeridos)
    rota_id = 1

    clocks_inicio = time.perf_counter_ns()

    dist_total, pred = g.floyd_warshall()
    
    dist_total_retorno, pred_retorno = g.floyd_warshall_retorno()
    
    while servicos_restantes:
        if debug:
            print(f"\n=== Iniciando nova rota {rota_id} ===")

        rota = []
        no_atual = no_inicial
        carga_atual = 0
        custo_total_rota = 0
        demanda_total_rota = 0
        visitas_rota = 1
        rota_encerrada = False
        
        rota.append(("D", 0, no_inicial, no_inicial))
        ids_ordenados = sorted(servicos_restantes.keys())

        for id_req in ids_ordenados:
            
            if rota_encerrada:
                break  # Não coleta mais se rota encerrada

            servico = servicos_restantes.get(id_req)
            if servico is None:
                continue
            
            tipo = servico['tipo']
            u, v = servico['de'], servico['para']
            
            if tipo in ('no', 'arco'):
                destino = u
            elif tipo == 'aresta':
                custo_u = dist_total[no_atual-1][u-1]
                custo_v = dist_total[no_atual-1][v-1]
                destino = u if custo_u <= custo_v else v
            else:
                continue

            # Reconstruir caminho
            caminho = []
            no_temp = destino - 1
            deposito = no_atual - 1
            while no_temp != deposito:
                caminho.append(no_temp)
                no_temp = pred[deposito][no_temp]
                if no_temp == -1:
                    if debug:
                        print("Sem caminho para o destino")
                    break
            caminho.append(deposito)
            caminho.reverse()

            for i in range(len(caminho)-1):
                if rota_encerrada:
                    break  # Parar se rota encerrada durante o percurso

                de = caminho[i] + 1
                para = caminho[i+1] + 1

                servico_direto = g.get_indice_requerido(de, para)
                servico_inverso = g.get_indice_requerido(para, de)

                # Só considera o inverso se for uma aresta não-direcionada
                if servico_direto in servicos_restantes:
                    id_servico = servico_direto
                    tipo_servico = servicos_restantes[id_servico]['tipo']
                elif servico_inverso in servicos_restantes and servicos_restantes[servico_inverso]['tipo'] == 'aresta':
                    id_servico = servico_inverso
                    tipo_servico = 'aresta'
                else:
                    id_servico = None
                
                if id_servico is not None:
                    demanda_ares = g.get_demanda_aresta(de, para) if tipo_servico == 'aresta' else g.get_demanda_normal(de, para)
                    if carga_atual + demanda_ares > capacidade_maxima_veiculo:
                        if debug:
                            print("Capacidade excedida durante percurso na aresta")
                        rota_encerrada = True
                        break

                    if debug:
                        print(f"Coletando serviço {'bidirecional' if tipo_servico == 'aresta' else 'direcional'} na {de} -> {para}")
                    rota.append(("S", id_servico, de, para))
                    visitas_rota += 1
                    carga_atual += demanda_ares
                    demanda_total_rota += demanda_ares
                    del servicos_restantes[id_servico]
                    

                # Coleta em nó
                def coletar_servico_no(vertice):
                    nonlocal visitas_rota, carga_atual, demanda_total_rota, rota_encerrada
                    for chave, serv in list(servicos_restantes.items()):
                        if serv['de'] == vertice and serv['para'] == vertice:
                            demanda_no = g.get_demanda_normal(vertice, vertice)
                            if demanda_no == 0:
                                if debug:
                                    print(f"Serviço no nó {vertice} tem demanda zero e será ignorado.")
                                del servicos_restantes[chave]
                                return True
                            if carga_atual + demanda_no > capacidade_maxima_veiculo:
                                if debug:
                                    print("Capacidade excedida coletando no nó")
                                rota_encerrada = True
                                return False
                            if debug:
                                print(f"Coletando demanda no nó {vertice}")
                            rota.append(("S", chave, vertice, vertice))
                            visitas_rota += 1
                            carga_atual += demanda_no
                            demanda_total_rota += demanda_no
                            del servicos_restantes[chave]
                            return True
                    return True

                if not coletar_servico_no(para):
                    rota_encerrada = True
                    break

                custo_total_rota += dist_total[de-1][para-1]
                no_atual = para

            if rota_encerrada:
                break

            # Coleta final do serviço
            if id_req in servicos_restantes:
                if tipo == 'aresta':
                    demanda_serv = g.get_demanda_aresta(u, v)
                else:
                    demanda_serv = g.get_demanda_normal(u, v)

                if demanda_serv == 0:
                    if debug:
                        print(f"Serviço {id_req} tem demanda zero e será ignorado.")
                    del servicos_restantes[id_req]
                    continue

                if carga_atual + demanda_serv > capacidade_maxima_veiculo:
                    if debug:
                        print("Capacidade máxima seria excedida após coletar serviço final, encerrando rota.")
                    rota_encerrada = True 
                    break  # interrompe coleta

                # Se ainda não encerrou a rota, coleta o serviço
                rota.append(("S", id_req, u, v))
                visitas_rota += 1
                carga_atual += demanda_serv
                demanda_total_rota += demanda_serv
                del servicos_restantes[id_req]
                

        # Retorno ao depósito
        if no_atual != no_inicial:
            if debug:
                print(f"Retornando do nó {no_atual} ao depósito...")
            caminho_retorno = []
            no_temp = no_inicial - 1
            deposito_atual = no_atual - 1
            while no_temp != deposito_atual:
                caminho_retorno.append(no_temp)
                no_temp = pred_retorno[deposito_atual][no_temp]
                if no_temp == -1:
                    if debug:
                        print("Sem caminho para retorno ao depósito")
                    break
            caminho_retorno.append(deposito_atual)
            caminho_retorno.reverse()

            for i in range(len(caminho_retorno)-1):
                de = caminho_retorno[i] + 1
                para = caminho_retorno[i+1] + 1
                custo_total_rota += dist_total_retorno[de-1][para-1]
                no_atual = para

        rota.append(("D", 0, no_inicial, no_inicial))
        visitas_rota += 1

        rotas_formatadas.append({
            "indice": rota_id,
            "demanda": demanda_total_rota,
            "custo": custo_total_rota,
            "visitas": visitas_rota,
            "trajeto": rota
        })

        custo_total_global += custo_total_rota
        rota_id += 1

    clocks_fim = time.perf_counter_ns()
    clocks_execucao = clocks_fim - clocks_inicio
    clocks_solucao = clocks_execucao // 100

    return rotas_formatadas, custo_total_global, clocks_execucao, clocks_solucao


def ler_capacidade(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        for linha in f:
            if linha.strip().startswith('Capacity:'):
                partes = linha.strip().split()
                if len(partes) >= 2:
                    return int(partes[1])
    return None  

import os

def executar_testes_em_pasta(pasta_testes, pasta_saida):
   
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    for nome_arquivo in os.listdir(pasta_testes):
        if nome_arquivo.endswith(".dat"):
            caminho_completo_arquivo = os.path.join(pasta_testes, nome_arquivo)
            print(f"Processando arquivo: {nome_arquivo}")

            try:
                # Carregar o grafo e dados
                num_vertices = quantidadeDeVertices(caminho_completo_arquivo)
                g = Grafo(num_vertices)
                g.adiciona_nos_requeridos(caminho_completo_arquivo)
                g.adiciona_aresta_requerida(caminho_completo_arquivo)
                g.adiciona_aresta_Normal(caminho_completo_arquivo)
                g.adiciona_arco_Requerido(caminho_completo_arquivo)
                g.adiciona_arco_Normal(caminho_completo_arquivo)

                # Obter a capacidade do veículo
                capacidade_maxima_veiculo = ler_capacidade(caminho_completo_arquivo)
                if capacidade_maxima_veiculo is None:
                    print(f"Aviso: Capacidade do veículo não encontrada no arquivo {nome_arquivo}. Pulando.")
                    continue

                # Executar o algoritmo de construção de rotas
                rotas, custo_total_global, tempo_execucao, tempo_solucao = construir_rotas_ordenadas(
                    g,
                    capacidade_maxima_veiculo=capacidade_maxima_veiculo,
                    no_inicial=1  # Assumindo que o depósito é sempre o nó 1
                )

                # Gerar o nome do arquivo de saída
                nome_base = os.path.splitext(nome_arquivo)[0]
                caminho_arquivo_saida = os.path.join(pasta_saida, f"sol-{nome_base}.dat")

                # Escrever os resultados no arquivo de saída
                with open(caminho_arquivo_saida, 'w') as f:
                    f.write(f"{custo_total_global}\n")
                    f.write(f"{len(rotas)}\n")
                    f.write(f"{tempo_execucao}\n")
                    f.write(f"{tempo_solucao}\n")

                    demanda_total_recolhida = 0
                    for rota in rotas:
                        f.write(f"0 1 {rota['indice']} {rota['demanda']} {rota['custo']} {rota['visitas']}")
                        demanda_total_recolhida += rota['demanda']
                        for t in rota["trajeto"]:
                            tipo, id_s, x, y = t
                            if tipo == "D":
                                f.write(f" (D {0},{x},{y})")
                            elif tipo == "S":
                                f.write(f" (S {id_s},{x},{y})")
                        f.write("\n")

                print(f"Resultados salvos em: {caminho_arquivo_saida}")

            except Exception as e:
                print(f"Erro ao processar o arquivo {nome_arquivo}: {e}")

import os
import sys
import tempfile
import shutil

if __name__ == "__main__":
    # Define a pasta de saída padrão (Resultados no mesmo diretório do script)
    diretorio_atual_script = os.path.dirname(os.path.abspath(__file__))
    pasta_resultados_saida = os.path.join(diretorio_atual_script, "Resultados")

    # Mensagem informativa para o usuário
    print(">>> Por favor, informe um ARQUIVO .dat ou uma PASTA com arquivos .dat.")
    print(">>> Uso esperado:")
    print(f"    python {os.path.basename(__file__)} arquivo.dat [pasta_saida]")
    print(f"    python {os.path.basename(__file__)} pasta_com_arquivos [pasta_saida]")
    print("")

    if len(sys.argv) > 1:
        entrada = sys.argv[1]
        caminho_entrada = os.path.join(diretorio_atual_script, entrada)

        # Se passar uma pasta de saída personalizada
        if len(sys.argv) > 2:
            if os.path.isabs(sys.argv[2]):
                pasta_resultados_saida = sys.argv[2]
            else:
                pasta_resultados_saida = os.path.join(diretorio_atual_script, sys.argv[2])

        # Verifica se é um único arquivo .dat
        if os.path.isfile(caminho_entrada) and caminho_entrada.endswith(".dat"):
            with tempfile.TemporaryDirectory() as pasta_temp:
                shutil.copy(caminho_entrada, pasta_temp)
                executar_testes_em_pasta(pasta_temp, pasta_resultados_saida)

        # Ou se é uma pasta com vários arquivos
        elif os.path.isdir(caminho_entrada):
            executar_testes_em_pasta(caminho_entrada, pasta_resultados_saida)

        else:
            print(f"Erro: '{entrada}' não é um arquivo .dat nem uma pasta válida.")
    
    else:
        print(" Nenhum argumento fornecido.")
