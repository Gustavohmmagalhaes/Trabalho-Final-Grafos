from Otimizacao import (
    extrair_sequencia_nos_rota,
    otimizar_rota_2opt,
    recalcular_custo_total_rota_otimizada
)
from Utilitarios import reconstruir_caminho
import copy
import time

def coletar_servico_no(vertice, servicos_restantes, g, carga_atual, capacidade, demanda_total_rota, custo_rota, rota, visitas_rota, debug):
    
    servicos_a_processar_no_vertice = []
    for chave, serv in servicos_restantes.items():
        if serv['de'] == vertice and serv['para'] == vertice and serv['tipo'] == 'no':
            servicos_a_processar_no_vertice.append(chave)

    found_any_collectable = False 
    capacity_exceeded_for_any = False

    for chave in servicos_a_processar_no_vertice:
      
        if chave not in servicos_restantes:
            continue

        serv = servicos_restantes[chave]
        dem = g.get_demanda_normal(vertice, vertice)

        if dem == 0:
            if debug: print(f"Servico no nó {vertice} ({chave}) demanda zero, ignorando e removendo.")
            del servicos_restantes[chave]
            found_any_collectable = True
            continue 

        if carga_atual + dem > capacidade:
            if debug: print(f"Excederia capacidade ({carga_atual}+{dem} > {capacidade}) ao coletar serviço de nó {vertice} ({chave}).")
            capacity_exceeded_for_any = True
          
            continue 

        if debug: print(f"Coletando serviço no nó {vertice} ({chave}) (demanda={dem})")
        rota.append(("S", chave, vertice, vertice))
        visitas_rota += 1
        carga_atual += dem
        demanda_total_rota += dem
        custo_rota += serv['custo-servico']  
        del servicos_restantes[chave]
        found_any_collectable = True

    if capacity_exceeded_for_any:
        return False, carga_atual, demanda_total_rota, custo_rota, visitas_rota, rota, True 
    elif found_any_collectable:
        return True, carga_atual, demanda_total_rota, custo_rota, visitas_rota, rota, False 
    else:
        return False, carga_atual, demanda_total_rota, custo_rota, visitas_rota, rota, False


def encontrar_servico_mais_proximo(servicos_restantes, no_atual, dist_total, debug):
    menor_custo_total_potencial = float('inf')
    melhor_id_servico = None
    melhor_destino = None

    for id_servico, servico in servicos_restantes.items():
        destino_servico = None
        
        if servico['tipo'] == 'no':
            destino_servico = servico['de']
        
            if destino_servico == no_atual:
                if debug: print(f"[DEBUG] Encontrar_servico_mais_proximo: Pulando serviço de NÓ {id_servico} no mesmo nó {no_atual}.")
                continue
            
        elif servico['tipo'] == 'arco':
            destino_servico = servico['para']
        elif servico['tipo'] == 'aresta':
            dist_para_de = dist_total[no_atual - 1][servico['de'] - 1]
            dist_para_para = dist_total[no_atual - 1][servico['para'] - 1]
            if dist_para_de <= dist_para_para:
                destino_servico = servico['de']
            else:
                destino_servico = servico['para']
        
        if destino_servico is None:
            continue

        if dist_total[no_atual - 1][destino_servico - 1] == float('inf'):
            if debug: print(f"[DEBUG] Encontrar_servico_mais_proximo: Caminho de {no_atual} para {destino_servico} (para serviço {id_servico}) é inacessível.")
            continue

        custo_transporte = dist_total[no_atual - 1][destino_servico - 1]
        custo_servico_intrinseco = servico['custo-servico']

        custo_total_potencial = custo_transporte + custo_servico_intrinseco

        if custo_total_potencial < menor_custo_total_potencial:
            menor_custo_total_potencial = custo_total_potencial
            melhor_id_servico = id_servico
            melhor_destino = destino_servico
            
    if debug and melhor_id_servico:
        print(f"[DEBUG] Encontrar_servico_mais_proximo: Selecionado serviço {melhor_id_servico} (tipo={servicos_restantes[melhor_id_servico]['tipo']}) para destino {melhor_destino}.")
    
    return melhor_id_servico, melhor_destino


def mover_e_coletar(no_atual, destino, g, dist_total, pred, servicos_restantes, carga, capacidade, demanda, rota, visitas, debug):
    caminho = reconstruir_caminho(pred, no_atual - 1, destino - 1)

    if not caminho or (caminho and caminho[0] != no_atual -1):
        if debug: print(f"Não foi possível reconstruir o caminho de {no_atual} para {destino}.")
        return no_atual, carga, demanda, visitas, 0, True 
    
    caminho_reconst = [n + 1 for n in caminho] 
    
    if debug and caminho_reconst:
        print(f"Caminho até {destino}: {caminho_reconst}")

    custo = 0
    current_node_on_path = no_atual
    
    for i in range(len(caminho_reconst) - 1):
        de, para = caminho_reconst[i], caminho_reconst[i + 1]
        
        if de != current_node_on_path:
            if debug: print(f"Aviso: Nó inicial do segmento de caminho ({de}) difere do nó atual ({current_node_on_path}).")
            current_node_on_path = de 
            
        tipo_coleta = None
        id_coleta = None
        
        serv_d_id = g.get_indice_requerido(de, para)
        serv_i_id = g.get_indice_requerido(para, de)

        if serv_d_id in servicos_restantes:
            serv_detail = servicos_restantes[serv_d_id]
            if serv_detail['tipo'] == 'arco' and serv_detail['de'] == de and serv_detail['para'] == para:
                tipo_coleta = 'arco'
                id_coleta = serv_d_id
            elif serv_detail['tipo'] == 'aresta':
                tipo_coleta = 'aresta'
                id_coleta = serv_d_id
        
        if id_coleta is None and serv_i_id in servicos_restantes:
            serv_detail = servicos_restantes[serv_i_id]
            if serv_detail['tipo'] == 'aresta':
                tipo_coleta = 'aresta'
                id_coleta = serv_i_id


        dist = dist_total[de - 1][para - 1]
        custo_servico = 0

        if id_coleta is not None:
            dem = g.get_demanda_aresta(de, para) if tipo_coleta == 'aresta' else g.get_demanda_normal(de, para)
            custo_servico = servicos_restantes[id_coleta]['custo-servico']

            if carga + dem > capacidade:
                if debug:
                    print(f"Excederia capacidade ao coletar serviço {id_coleta} ({tipo_coleta} {de}->{para}), encerrando rota.")
                return current_node_on_path, carga, demanda, visitas, custo, True 

            if debug:
                print(f"Coletando serviço {tipo_coleta} {de}->{para} (demanda={dem})")

            rota.append(("S", id_coleta, de, para))
            visitas += 1
            carga += dem
            demanda += dem
            custo += custo_servico
            if debug:
                print(f"[DEBUG] ⤷ Movimento {de} → {para} | Distância: {dist} | Custo serviço: {custo_servico} ⇒ Total parcial: {dist + custo_servico}")
            
            del servicos_restantes[id_coleta] 

        else:
            if debug:
                print(f"[DEBUG] ⤷ Movimento {de} → {para} | Distância: {dist} | Custo serviço: 0 ⇒ Total parcial: {dist}")

        custo += dist 
        current_node_on_path = para

    return current_node_on_path, carga, demanda, visitas, custo, False


def construir_rotas_ordenadas(g, capacidade_maxima_veiculo, no_inicial, debug=False):
    servicos_restantes = copy.deepcopy(g.elementos_requeridos)
    dist_total, pred = g.floyd_warshall()

    resultado_rotas = []
    custo_total_global = 0
    inicio = time.perf_counter_ns()
    rota_id = 1

    fim = inicio
    tempo_exec = 0
    tempo_us = 0

    while servicos_restantes:
        if debug: print(f"\n=== Rota {rota_id} iniciada ===")

        no_atual = no_inicial
        rota = [("D", 0, no_inicial, no_inicial)]
        carga = 0
        demanda_rota = 0
        custo_rota = 0
        visitas = 1
        rota_encerrada = False

        while True:
            if debug: print(f"[DEBUG] Tentando coletar serviços de nó no {no_atual}.")
            
            ok_coleta_no, carga, demanda_rota, custo_rota, visitas, rota, encerra_coleta_no = coletar_servico_no(
                no_atual, servicos_restantes, g, carga, capacidade_maxima_veiculo,
                demanda_rota, custo_rota, rota, visitas, debug
            )

            if encerra_coleta_no:
                if debug: print(f"[DEBUG] Capacidade excedida ou problema ao coletar serviço de nó no {no_atual}. Encerrando rota.")
                fim = time.perf_counter_ns()
                break

            id_req_proximo, destino_proximo = encontrar_servico_mais_proximo(servicos_restantes, no_atual, dist_total, debug)

            if id_req_proximo is None:
                if debug: print("[DEBUG] Nenhum serviço proximo encontrado para coletar nesta rota. Encerrando rota atual.")
                fim = time.perf_counter_ns()
                break

            servico_proximo_detalhes = g.elementos_requeridos[id_req_proximo]

            if destino_proximo == no_atual:
                if servico_proximo_detalhes['tipo'] in ['aresta', 'arco']:
                    dem_servico = servico_proximo_detalhes['demanda']

                    if carga + dem_servico > capacidade_maxima_veiculo:
                        if debug: print(f"[DEBUG] Não pode coletar serviço {id_req_proximo} ({servico_proximo_detalhes['tipo']}) no nó {no_atual} devido a capacidade. Encerrando rota.")
                        rota_encerrada = True
                        fim = time.perf_counter_ns()
                        break

                    if debug: print(f"[DEBUG] Coletando serviço {id_req_proximo} ({servico_proximo_detalhes['tipo']}) no nó {no_atual} (já no destino do serviço).")

                    rota.append(("S", id_req_proximo, servico_proximo_detalhes['de'], servico_proximo_detalhes['para']))
                    visitas += 1
                    carga += dem_servico
                    demanda_rota += dem_servico
                    custo_rota += servico_proximo_detalhes['custo-servico']
                    del servicos_restantes[id_req_proximo]

                    if debug: print(f"[DEBUG] Custo após coleta direta de serviço {id_req_proximo}: {custo_rota}")
                    continue
                else:
                    if debug: print(f"[DEBUG] Loop potencial: Serviço {id_req_proximo} é de NÓ e destino {destino_proximo} é o nó atual. Encerrando rota para evitar loop.")
                    rota_encerrada = True
                    fim = time.perf_counter_ns()
                    break

            if debug: print(f"[DEBUG] Movendo de {no_atual} para {destino_proximo} para coletar {id_req_proximo} ({servico_proximo_detalhes['tipo']}).")
            no_atual_new, carga_new, demanda_new, visitas_new, custo_mov_serv_segmento, encerra_movimento = mover_e_coletar(
                no_atual, destino_proximo, g, dist_total, pred, servicos_restantes, carga, capacidade_maxima_veiculo, demanda_rota, rota, visitas, debug)

            no_atual, carga, demanda_rota, visitas = no_atual_new, carga_new, demanda_new, visitas_new
            custo_rota += custo_mov_serv_segmento

            if debug: print(f"[DEBUG] Custo após mover_e_coletar até {destino_proximo}: {custo_rota}")

            if encerra_movimento:
                if debug: print(f"[DEBUG] Capacidade excedida durante movimento para {destino_proximo}. Encerrando rota.")
                rota_encerrada = True
                fim = time.perf_counter_ns()
                break

        custo_retorno_ao_deposito = 0
        if no_atual != no_inicial:
            if debug: print(f"Retornando do nó {no_atual} para o depósito {no_inicial}")
            caminho_retorno = reconstruir_caminho(pred, no_atual - 1, no_inicial - 1)
            caminho_retorno_1_based = [n + 1 for n in caminho_retorno]

            if caminho_retorno_1_based:
                for i in range(len(caminho_retorno_1_based) - 1):
                    de_ret, para_ret = caminho_retorno_1_based[i], caminho_retorno_1_based[i + 1]
                    seg_dist = dist_total[de_ret - 1][para_ret - 1]
                    custo_rota += seg_dist
                    custo_retorno_ao_deposito += seg_dist
                    if debug: print(f" - Caminho de retorno: {de_ret} → {para_ret} | Custo: {seg_dist}")
                if debug: print(f" - Custo total do retorno: {custo_retorno_ao_deposito}")
            else:
                if debug: print("Aviso: Não foi possível reconstruir o caminho de retorno para o depósito. Custo de retorno pode ser impreciso.")

        rota_original_completa = list(rota)
        rota.append(("D", 0, no_inicial, no_inicial))
        visitas += 1

        custo_total_original_rota = custo_rota

        sequencia_nos_para_2opt = extrair_sequencia_nos_rota(rota_original_completa, no_inicial)
        rota_nodes_otimizada, custo_transporte_otimizado = otimizar_rota_2opt(sequencia_nos_para_2opt, dist_total)
        
        custo_total_otimizado = recalcular_custo_total_rota_otimizada(
            rota_nodes_otimizada, rota_original_completa, dist_total, g, capacidade_maxima_veiculo
        )

        custo_final_rota = custo_total_otimizado

        if debug:
            print(f"\n--- Resumo da Rota {rota_id} (ANTES da otimização) ---")
            print(f" - Custo total da rota original (gulosa): {custo_total_original_rota}")
            print(f" - Trajeto original completo: {rota_original_completa}")
            print(f"\n--- Resumo da Rota {rota_id} (APÓS otimização 2-Opt) ---")
            print(f" - Sequência de nós otimizada: {rota_nodes_otimizada}")
            print(f" - Custo de transporte otimizado (apenas movimento): {custo_transporte_otimizado}")
            print(f" - Custo TOTAL otimizado (transporte + serviços válidos): {custo_total_otimizado}")
            print("-" * 40)

        trajeto_otimizado_detalhado = reconstruir_trajeto_detalhado_otimizado(
            rota_nodes_otimizada, rota_original_completa, g, no_inicial, dist_total, pred, debug
        )

        custo_total_global += custo_final_rota

        resultado_rotas.append({
            "id": rota_id,
            "custo": custo_final_rota,
            "demanda": demanda_rota,
            "visitas": visitas, 
            "trajeto": trajeto_otimizado_detalhado 
        })

        rota_id += 1

        if not servicos_restantes:
            if debug: print("\nTodos os serviços foram atendidos. Encerrando algoritmo.")
            break
        elif rota_encerrada and not servicos_restantes: 
             if debug: print("\nRota encerrada por capacidade e não há mais serviços restantes.")
             break
        elif rota_encerrada and servicos_restantes:
             if debug: print("\nRota encerrada por capacidade, mas ainda há serviços restantes. Iniciando nova rota.")
        elif not id_req_proximo and not servicos_restantes: 
            if debug: print("\nNenhum serviço próximo encontrado e todos os serviços foram atendidos. Encerrando algoritmo.")
            break
        elif not id_req_proximo and servicos_restantes: 
             if debug: print("\nNenhum serviço próximo encontrado, mas ainda há serviços restantes. Possível problema de acessibilidade ou todos os restantes excedem capacidade. Encerrando.")
             break 

    fim = time.perf_counter_ns()
    tempo_exec = (fim - inicio) 
    tempo_us = (fim - inicio) // 1000

    if debug:
        print(f"\n--- Fim do Processamento ---")
        print(f"Custo total global de todas as rotas: {custo_total_global}")
        print(f"Tempo de execução: {tempo_exec:.4f} segundos ({tempo_us:.2f} microssegundos)")

    return resultado_rotas, custo_total_global, tempo_exec, tempo_us

def reconstruir_trajeto_detalhado_otimizado(rota_nodes_otimizada, rota_original_completa, g, no_inicial, dist_total, pred, debug=False):
    
    trajeto_final_output = []

    trajeto_final_output.append(("D", 0, no_inicial, no_inicial))
    if debug: print(f"[DEBUG_RECON] Adicionado depósito inicial: {trajeto_final_output[-1]}")

    servicos_adicionados_set = set()

    for item in rota_original_completa:
        if item[0] == "S": 
            if item not in servicos_adicionados_set:
                trajeto_final_output.append(item)
                servicos_adicionados_set.add(item)
                if debug: print(f"[DEBUG_RECON] Adicionado serviço: {item}")

    if not trajeto_final_output or trajeto_final_output[-1] != ("D", 0, no_inicial, no_inicial):
        trajeto_final_output.append(("D", 0, no_inicial, no_inicial))
        if debug: print(f"[DEBUG_RECON] Adicionado depósito final: {trajeto_final_output[-1]}")
    
    return trajeto_final_output