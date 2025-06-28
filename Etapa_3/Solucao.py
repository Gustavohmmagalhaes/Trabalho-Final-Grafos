from Utilitarios import reconstruir_caminho


def coletar_servico_no(vertice, servicos_restantes, g, carga_atual, capacidade,
                        demanda_total_rota, rota, visitas_rota, debug):
    for chave, serv in list(servicos_restantes.items()):
        if serv['de'] == vertice and serv['para'] == vertice:
            dem = g.get_demanda_normal(vertice, vertice)
            if dem == 0:
                if debug:
                    print(f"Servico no nó {vertice} demanda zero, ignorando.")
                del servicos_restantes[chave]
                return True, carga_atual, demanda_total_rota, visitas_rota, rota, False
            if carga_atual + dem > capacidade:
                return False, carga_atual, demanda_total_rota, visitas_rota, rota, True
            if debug:
                print(f"Coletando serviço no nó {vertice} (demanda={dem})")
            rota.append(("S", chave, vertice, vertice))
            visitas_rota += 1
            carga_atual += dem
            demanda_total_rota += dem
            del servicos_restantes[chave]
            return True, carga_atual, demanda_total_rota, visitas_rota, rota, False
    return True, carga_atual, demanda_total_rota, visitas_rota, rota, False


def encontrar_servico_mais_proximo(servicos_restantes, no_atual, dist_total):
    menor = float('inf')
    melhor_id = None
    melhor_destino = None

    for id_req, serv in servicos_restantes.items():
        tipo, u, v = serv['tipo'], serv['de'], serv['para']
        if tipo == 'no':
            d = 0 if u == no_atual else dist_total[no_atual - 1][u - 1]
            cand_dest = u
        elif tipo == 'arco':
            if u == no_atual:
                continue
            d = dist_total[no_atual - 1][u - 1]
            cand_dest = u
        elif tipo == 'aresta':
            du = dist_total[no_atual - 1][u - 1]
            dv = dist_total[no_atual - 1][v - 1]
            if u == no_atual and v == no_atual:
                continue
            elif u == no_atual:
                d, cand_dest = dv, v
            elif v == no_atual:
                d, cand_dest = du, u
            else:
                d, cand_dest = (du, u) if du <= dv else (dv, v)
        else:
            continue

        if d < menor:
            menor = d
            melhor_id = id_req
            melhor_destino = cand_dest

    return melhor_id, melhor_destino


def mover_e_coletar(no_atual, destino, g, dist_total, pred,
                    servicos_restantes, carga, capacidade,
                    demanda, rota, visitas, debug):
    caminho = reconstruir_caminho(pred, no_atual - 1, destino - 1)
    caminho = [n + 1 for n in caminho] if caminho else []

    if debug and caminho:
        print(f"Caminho até {destino}: {caminho}")

    custo = 0
    for i in range(len(caminho) - 1):
        de, para = caminho[i], caminho[i + 1]
        tipo_coleta = None
        serv_d = g.get_indice_requerido(de, para)
        serv_i = g.get_indice_requerido(para, de)

        if serv_d in servicos_restantes:
            tipo_coleta = servicos_restantes[serv_d]['tipo']
            id_coleta = serv_d
        elif serv_i in servicos_restantes and servicos_restantes[serv_i]['tipo'] == 'aresta':
            tipo_coleta = 'aresta'
            id_coleta = serv_i
        else:
            id_coleta = None

        if id_coleta is not None:
            dem = g.get_demanda_aresta(de, para) if tipo_coleta == 'aresta' else g.get_demanda_normal(de, para)
            if carga + dem > capacidade:
                if debug:
                    print("Excederia capacidade ao coletar serviço no caminho, encerrando rota.")
                return no_atual, carga, demanda, visitas, custo, True
            if debug:
                print(f"Coletando serviço {tipo_coleta} {de}->{para} (demanda={dem})")
            rota.append(("S", id_coleta, de, para))
            visitas += 1
            carga += dem
            demanda += dem
            del servicos_restantes[id_coleta]

        custo += dist_total[de - 1][para - 1]
        no_atual = para

    return no_atual, carga, demanda, visitas, custo, False


def construir_rotas_ordenadas(g, capacidade_maxima_veiculo, no_inicial, debug=False):
    import copy, time
    servicos_restantes = copy.deepcopy(g.elementos_requeridos)
    dist_total, pred = g.floyd_warshall()
    dist_retorno, pred_retorno = g.floyd_warshall_retorno()
    resultado_rotas = []
    custo_total_global = 0
    inicio = time.perf_counter_ns()
    rota_id = 1

    while servicos_restantes:
        rota = [("D", 0, no_inicial, no_inicial)]
        no_atual = no_inicial
        carga, demanda_rota, custo_rota = 0, 0, 0
        visitas = 1
        rota_encerrada = False

        while servicos_restantes and not rota_encerrada:
            ok, carga, demanda_rota, visitas, rota, encerra = coletar_servico_no(
                no_atual, servicos_restantes, g, carga, capacidade_maxima_veiculo, demanda_rota, rota, visitas, debug)
            if encerra:
                break

            id_req, destino = encontrar_servico_mais_proximo(servicos_restantes, no_atual, dist_total)
            if id_req is None:
                break

            no_atual, carga, demanda_rota, visitas, custo, rota_encerrada = mover_e_coletar(
                no_atual, destino, g, dist_total, pred, servicos_restantes, carga, capacidade_maxima_veiculo, demanda_rota, rota, visitas, debug)
            custo_rota += custo
            if rota_encerrada:
                break

            if id_req in servicos_restantes:
                serv = servicos_restantes[id_req]
                dem = g.get_demanda_aresta(serv['de'], serv['para']) if serv['tipo'] == 'aresta' else g.get_demanda_normal(serv['de'], serv['para'])

                if dem == 0:
                    del servicos_restantes[id_req]
                    continue

                if carga + dem > capacidade_maxima_veiculo:
                    rota_encerrada = True
                    break

                rota.append(("S", id_req, serv['de'], serv['para']))
                visitas += 1
                carga += dem
                demanda_rota += dem
                del servicos_restantes[id_req]

                if serv['tipo'] == 'aresta':
                    no_atual = serv['para'] if no_atual == serv['de'] else serv['de']
                elif serv['tipo'] == 'arco':
                    no_atual = serv['para']
                else:
                    no_atual = serv['de']

        if no_atual != no_inicial:
            caminho = reconstruir_caminho(pred_retorno, no_atual - 1, no_inicial - 1)
            caminho = [n + 1 for n in caminho]
            for i in range(len(caminho) - 1):
                de, para = caminho[i], caminho[i + 1]
                custo_rota += dist_retorno[de - 1][para - 1]
                no_atual = para

        rota.append(("D", 0, no_inicial, no_inicial))
        visitas += 1

        resultado_rotas.append({
            "indice": rota_id,
            "demanda": demanda_rota,
            "custo": custo_rota,
            "visitas": visitas,
            "trajeto": rota
        })

        custo_total_global += custo_rota
        rota_id += 1

    fim = time.perf_counter_ns()
    tempo_exec = fim - inicio
    tempo_us = tempo_exec // 1000

    return resultado_rotas, custo_total_global, tempo_exec, tempo_us