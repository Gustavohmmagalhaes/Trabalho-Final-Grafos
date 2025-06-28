import os
import sys
import tempfile
import shutil

from Grafo import Grafo
from Leitor_dados import ler_capacidade, quantidadeDeVertices, ler_no_inicial, listar_instancias, garantir_pasta
from Solucao import construir_rotas_ordenadas

def executar_testes_em_pasta(pasta_testes, pasta_saida):
    garantir_pasta(pasta_saida)

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
                    no_inicial= ler_no_inicial(caminho_completo_arquivo),
                    debug=True
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

if __name__ == "__main__":
    diretorio_atual_script = os.path.dirname(os.path.abspath(__file__))
    pasta_resultados_saida = os.path.join(diretorio_atual_script, "Resultados")

    print(">>> Por favor, informe um ARQUIVO .dat ou uma PASTA com arquivos .dat.")
    print(">>> Uso esperado:")
    print(f"    python {os.path.basename(__file__)} arquivo.dat [pasta_saida]")
    print(f"    python {os.path.basename(__file__)} pasta_com_arquivos [pasta_saida]")
    print("")

    if len(sys.argv) > 1:
        entrada = sys.argv[1]
        caminho_entrada = os.path.join(diretorio_atual_script, entrada)

        if len(sys.argv) > 2:
            if os.path.isabs(sys.argv[2]):
                pasta_resultados_saida = sys.argv[2]
            else:
                pasta_resultados_saida = os.path.join(diretorio_atual_script, sys.argv[2])

        if os.path.isfile(caminho_entrada) and caminho_entrada.endswith(".dat"):
            with tempfile.TemporaryDirectory() as pasta_temp:
                shutil.copy(caminho_entrada, pasta_temp)
                executar_testes_em_pasta(pasta_temp, pasta_resultados_saida)

        elif os.path.isdir(caminho_entrada):
            executar_testes_em_pasta(caminho_entrada, pasta_resultados_saida)

        else:
            print(f"Erro: '{entrada}' não é um arquivo .dat nem uma pasta válida.")

    else:
        print(" Nenhum argumento fornecido.")
