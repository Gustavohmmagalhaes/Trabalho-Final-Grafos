def extrair_sequencia_nos_rota(rota_detalhada, no_inicial):
   
    sequencia_nos = [no_inicial] 
    
    for item in rota_detalhada:
        if item[0] == 'S': 
            if item[2] == item[3]: 
                if item[2] not in sequencia_nos: 
                    sequencia_nos.append(item[2])
            elif item[3] not in sequencia_nos: 
                sequencia_nos.append(item[3])
        elif item[0] == 'D' and item[2] == no_inicial and len(sequencia_nos) > 1 and sequencia_nos[-1] != no_inicial:
            sequencia_nos.append(no_inicial)

    if sequencia_nos[-1] != no_inicial:
        sequencia_nos.append(no_inicial)
    
    return sequencia_nos

def calcular_custo_caminho(caminho_nos, dist_total):

    if not isinstance(caminho_nos, list):
        print("ERRO FATAL: calcular_custo_caminho recebeu um não-lista para 'caminho_nos'!")
        raise TypeError(f"Argumento 'caminho_nos' deve ser uma lista, mas é {type(caminho_nos).__name__} com valor: {caminho_nos}")

    custo = 0

    for i in range(len(caminho_nos) - 1):
        n1 = caminho_nos[i]  
        n2 = caminho_nos[i+1] 
        
        custo += dist_total[n1 - 1][n2 - 1]
        
    return custo

def two_opt_swap(route_nodes, i, k):

    return route_nodes[0:i] + route_nodes[k:i-1:-1] + route_nodes[k+1:]

def otimizar_rota_2opt(rota_nodes_original, dist_total):
    if len(rota_nodes_original) < 4:
        return list(rota_nodes_original), calcular_custo_caminho(rota_nodes_original, dist_total)

    melhor_rota_nos = list(rota_nodes_original)
    melhor_custo_transporte = calcular_custo_caminho(melhor_rota_nos, dist_total)

    melhoria_encontrada = True 

    while melhoria_encontrada:
        melhoria_encontrada = False
        for i in range(1, len(melhor_rota_nos) - 2): 
            custo_velho_atual_i = float('inf') 
            custo_novo_atual_i = float('inf') 

            for k in range(i + 1, len(melhor_rota_nos) - 1): 
                custo_velho = dist_total[melhor_rota_nos[i-1]-1][melhor_rota_nos[i]-1] + \
                              dist_total[melhor_rota_nos[k]-1][melhor_rota_nos[k+1]-1]

                custo_novo = dist_total[melhor_rota_nos[i-1]-1][melhor_rota_nos[k]-1] + \
                             dist_total[melhor_rota_nos[i]-1][melhor_rota_nos[k+1]-1]

                if custo_novo < custo_velho:
                    nova_rota_nos = two_opt_swap(melhor_rota_nos, i, k)
                    
                    if not isinstance(nova_rota_nos, list):
                        print(f"ERRO: nova_rota_nos não é uma lista! É um {type(nova_rota_nos)} com valor {nova_rota_nos}")
                        raise TypeError("Problema no two_opt_swap: não retornou uma lista.")
                    
                    novo_custo_transporte = calcular_custo_caminho(nova_rota_nos, dist_total)
                    
                    if novo_custo_transporte < melhor_custo_transporte:
                        melhor_rota_nos = nova_rota_nos
                        melhor_custo_transporte = novo_custo_transporte
                        melhoria_encontrada = True 
                        break 
            if melhoria_encontrada:
                break 
    
    return melhor_rota_nos, melhor_custo_transporte

def recalcular_custo_total_rota_otimizada(rota_nodes_otimizada, rota_original_detalhada, dist_total, g, capacidade_veiculo):
   
    custo_total_recalculado = 0
    carga_atual = 0
    demanda_total_atendida = 0
    
    servicos_a_atender = {}
    for item in rota_original_detalhada:
        if item[0] == 'S':
            service_id = item[1]
            servicos_a_atender[service_id] = g.elementos_requeridos[service_id]

    for i in range(len(rota_nodes_otimizada) - 1):
        de_node = rota_nodes_otimizada[i]
        para_node = rota_nodes_otimizada[i+1]
        
        custo_total_recalculado += dist_total[de_node - 1][para_node - 1]
        
        for s_id, s_details in list(servicos_a_atender.items()):
            if s_details['tipo'] == 'no' and s_details['de'] == de_node:
                dem = g.get_demanda_normal(de_node, de_node)
                if carga_atual + dem <= capacidade_veiculo: 
                    custo_total_recalculado += s_details['custo-servico']
                    carga_atual += dem
                    demanda_total_atendida += dem
                    del servicos_a_atender[s_id] 
                else:
                    pass

        serv_id_direto = g.get_indice_requerido(de_node, para_node)
        serv_id_inverso = g.get_indice_requerido(para_node, de_node)

        serv_atendido_no_segmento = None
        if serv_id_direto in servicos_a_atender:
            serv_atendido_no_segmento = servicos_a_atender[serv_id_direto]
 
            if serv_atendido_no_segmento['tipo'] == 'arco' and \
               (serv_atendido_no_segmento['de'] != de_node or serv_atendido_no_segmento['para'] != para_node):
                serv_atendido_no_segmento = None
        
        if serv_atendido_no_segmento is None and serv_id_inverso in servicos_a_atender:
            temp_serv = servicos_a_atender[serv_id_inverso]
            if temp_serv['tipo'] == 'aresta': 
                serv_atendido_no_segmento = temp_serv
                serv_id_direto = serv_id_inverso 
            
        if serv_atendido_no_segmento:
            dem = g.get_demanda_aresta(de_node, para_node) if serv_atendido_no_segmento['tipo'] == 'aresta' else g.get_demanda_normal(de_node, para_node)
            if carga_atual + dem <= capacidade_veiculo: 
                custo_total_recalculado += serv_atendido_no_segmento['custo-servico']
                carga_atual += dem
                demanda_total_atendida += dem
                del servicos_a_atender[serv_id_direto] 

    if len(rota_nodes_otimizada) >= 2: 
        final_node_before_depot = rota_nodes_otimizada[-2] 
        for s_id, s_details in list(servicos_a_atender.items()):
            if s_details['tipo'] == 'no' and s_details['de'] == final_node_before_depot:
                dem = g.get_demanda_normal(final_node_before_depot, final_node_before_depot)
                if carga_atual + dem <= capacidade_veiculo:
                    custo_total_recalculado += s_details['custo-servico']
                    carga_atual += dem
                    demanda_total_atendida += dem
                    del servicos_a_atender[s_id]

    return custo_total_recalculado