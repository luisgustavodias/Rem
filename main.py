# coding=utf-8
# Trabalho Final de Graduação - UNIFEI 05.2023 - 10/10/2022-10:49 - testando tkinter gerado online
#
# Obtenção do vetor de probabilidades dos estados de uma rede de petri limitada e estocástica
# utilizando cadeias de markov.
# Autor: Luis Gustavo Dias Simão
# Orientador: Luiz Edival de Souza

import json
import pandas as pd  # para formatar os dados.
import numpy as np # para realizar os calculos
import tkinter as tk # para a interface gráfica
import tkinter.font as tkFont  # para configurar as fontes do TKinter
from tkinter import filedialog  # para abrir os arquivos


class Transitions:
    """
    Classe transição
    :param: name (nome da transição)
            tipo (tipo: contínuo, discreto)
            time_firing (quantidade de disparos / )
            priority = 1
            key = 0
    """
    name = ''
    tipo = ''
    time_firing = 0.0  # considerando-se apenas tempos
    priority = 1
    key = ""

    def __init__(self, nam, tip, time, prior, ke):
        self.time_firing = time
        self.name = nam
        self.tipo = tip
        self.key = ke
        self.priority = prior


class Places:
    """
    Classe de Lugares
        :param: string name (Nome do Lugar)
                string tipo (tipo: contínuo, discreto)
                string variable_name (nome da variável associada ao lugar)
                float initial_mark (marcação inicial do lugar)
                float capacity (capacidade do lugar)
                int key (chave do lugar)
    """
    name = ''
    tipo = ''
    variable_name = ''
    initial_mark = 0
    capacity = -1.0
    key = ""

    def __init__(self, nam, tip, var_nam, ini_mark, capac, ke):
        self.name = nam
        self.tipo = tip
        self.variable_name = var_nam
        self.initial_mark = ini_mark
        self.capacity = capac
        self.key = ke


class Arcs:
    """
    Classe arco:
    :param: int begin_key (Chave de início do arco)
            int finish_key (chave de fim do arco)
            float weight (peso do arco)
            string tipo (tipo do arco: discreto,continuo)
    """
    begin_key = ""
    finish_key = ""
    weight = 0.0
    tipo = ""

    def __init__(self, beg_k, fin_k, wei, tip):
        self.begin_key = beg_k
        self.finish_key = fin_k
        self.weight = wei
        self.tipo = tip


def analisar(data):
    ###### AQUI EH UM LUGAR QUE PRECISA MELHORAR, INICIANDO OS DADOS COM NUMPY E CONVERTENDO PRA PANDAS?

    # Junto ao programa deverá existir uma pasta com o arquivo exportado do VON ou do WebApn do Arruda
    global place_teste, transition_teste, arc_teste
    # loading_data carrega os lugares, transicoes e arcos
    place_teste, transition_teste, arc_teste = loading_data(data)
    global nome_transitions, nome_places
    nome_transitions = [''] * len(transition_teste)
    nome_places = [''] * len(place_teste)
    # aqui faz-se o teste de verificação de nomes repetidos

    if nome_repetido(place_teste):
        return "Erro Lugares com nomes iguais"
    if nome_repetido(transition_teste):
        return "Erro Transições com nomes iguais"

    #

    i = 0
    for c in place_teste:
        nome_places[i] = c.name
        i += 1
    i = 0
    for l in transition_teste:
        nome_transitions[i] = l.name
        i += 1

    # CREATING_MATRIX gera as matrizes Pre, Post, In, En, M0
    # dada determinados conjuntos de [Transition], [Place], [Arc]
    pre_entrada_np, post_saida_np, in_inibidores_np, en_habilitadores_np, marcacao_inicial_np = creating_matrix(
        transition_teste, place_teste, arc_teste)

    global pre_entrada, post_saida, in_inibidores, en_habilitadores, marcacao_inicial

    # Reformatando dados para DataFrame da biblioteca do Pandas
    pre_entrada = pd.DataFrame(pre_entrada_np, index=nome_transitions, columns=nome_places)
    print(pre_entrada)
    post_saida = pd.DataFrame(post_saida_np, index=nome_transitions, columns=nome_places)
    in_inibidores = pd.DataFrame(in_inibidores_np, index=nome_transitions, columns=nome_places)
    en_habilitadores = pd.DataFrame(en_habilitadores_np, index=nome_transitions, columns=nome_places)
    marcacao_inicial = pd.DataFrame(marcacao_inicial_np, columns=nome_places)
    print(marcacao_inicial)
    return "Dados carregados"


def loading_data(dados):
    """
    Carrega os dados em texto, cria então três vetores, com os lugares, transições e arcos
    OBS: Transições, lugares e arcos são classes definidas neste programa
    :param: dados
    :return: place_teste, transition_teste, arc_teste
    """
    arc_teste = [Arcs('', '', 0.0, '')]  # creating arc list
    arc_teste.pop(0)
    place_teste = [Places('', '', '', 0, -1, "")]  # creating place list
    place_teste.pop(0)
    transition_teste = [Transitions('', '', '', 1, "")]
    transition_teste.pop(0)
    fornecedor = "erro"
    h = dados.read(1)

    if h == "{":
        fornecedor = "Arruda"
    elif h == "f":
        fornecedor = "VON"
    else:
        return "Arquivo desconhecido"

    # fatiando em linhas para leitura dos dados no caso dos arquivo gerado em VON
    if fornecedor == "VON":
        print("Arquivo exportado do software Virtual Object Net++ Dr. Rainer Drath service@ParamSoft.de version 2.7a")
        for line in dados:
            line = line.strip('     ')
            line = line.rstrip()

            # Loading...
            # Arcs
            if line.startswith('from '):
                inicio = line[line.find('from ') + len('from '):line.find(' (key')]
                begin_key = str(line[line.find(inicio) + len(inicio) + len(' (key='):line.find(') t')])
                final = 7 + line.find(str(begin_key))
                final = line[final:line.find('), t')]
                finish_key = str(final[final.find('(key=') + len('(key='):])
                weight = line[line.find('weight: ') + len('weight: '):]
                weight = float(weight.replace(',', '.'))
                tipo = line[(line.find('typ: ') + len('typ: ')):line.find(', weig')]
                arc_teste.append(Arcs(begin_key, finish_key, weight, tipo))

            # Places
            if line.startswith('Name: '):
                name = line[6:line.find(', typ')]
                tipo = line[(line.find('typ: ') + len('typ: ')):line.find(', var')]
                variable_name = line[(line.find('variable name: ') + len('variable name: ')):line.find(', ini')]

                try:
                    initial_mark = int(line[(line.find('marking: ') + len('marking: ')):line.find(', capacity: ')])
                except:
                    initial_mark = int(line[(line.find('marking: ') + len('marking: ')):line.find(', key:')])

                try:
                    capacity = float(line[line.find('capacity: ') + len('capacity: '):line.find(', key:')])
                except:
                    capacity = -1

                key = str(line[line.find('key: ') + len('key: '):])

                place_teste.append(Places(name, tipo, variable_name, initial_mark, capacity, key))

            # Transitions
            # aqui eu faço a divisão do código de modo a obter apenas os valores a serem armazenados na classe transições(transitions)
            if line.startswith('name: '):
                #
                name = line[6:line.find(', typ')]
                tipo = line[(line.find('typ: ') + len('typ: ')):line.find(', ')]
                key = str(line[line.find('key: ') + len('key: '):])
                try:
                    priority = int(line[line.find('priority: ') + len('priority: '):line.find(', reservation')])
                except:
                    priority = -1
                try:
                    time_speed = line[line.find('firing time: ') + len('firing time: '):(line.find(', priority:'))]
                    time_speed = float(time_speed.replace(",", "."))
                    # se for atribuído o tempo médio, usar:
                    # time_speed = 1/time_speed
                    # se for atribuída a quantidade de disparos:
                    time_speed = time_speed
                except:
                    time_speed = 1

                transition_teste.append(Transitions(name, tipo, time_speed, priority, key))

        return place_teste, transition_teste, arc_teste
    elif (fornecedor == "Arruda"):
        # Aqui fazer como se carrega-se do VON criado pelo Paulo Arruda ou pelo CPNTools, a ideia é manter o formato com
        # transições, lugares e arcos definidos por este template para os devidos cálculos, tal como realizado acima,
        # destrinchando o texto para obter as informações de cada uma das classes
        print("Arquivo do Arruda")

        with open(dados.name, 'r') as file:
            conteudo = file.read()
            data = json.loads(conteudo)

            print(data["name"])
            for transition in data["transitions"]:
                print(transition["delay"])
                if transition["delay"] != "":
                    transition_teste.append(Transitions(transition["name"], "normal", float(transition["delay"].replace(",", ".")), 1, transition["id"]))
                else:
                    transition_teste.append(Transitions(transition["name"], "normal", 0, 1, transition["id"]))
            for place in data["places"]:
                place_teste.append(Places(place["name"], "dicrete", place["name"], int(place["initialMark"]), -1, place["id"]))
            for arc in data["arcs"]:
                if arc["arcType"] == "Input":
                    arc_teste.append(Arcs(arc["placeId"], arc["transId"], float(arc["weight"]), "normal"))
                elif arc["arcType"] == "Test":
                    arc_teste.append(Arcs(arc["transId"], arc["placeId"], float(arc["weight"]), 'test arc'))
                elif arc["arcType"] == "Inhibitor":
                    arc_teste.append(Arcs(arc["transId"], arc["placeId"], float(arc["weight"]), "inhibitor"))


        return place_teste, transition_teste, arc_teste
    elif (fornecedor == "erro"):
        print("Erro em relacao ao nome do fornecedor...")
        return place_teste, transition_teste, arc_teste


def nome_repetido(vetor):
    i = 1
    aux_i = 1
    for v in vetor:
        while i < len(vetor):
            print(vetor[i].name)
            print(v.name)
            if vetor[i].name == v.name:
                return True
            i += 1
        aux_i += 1
        i = aux_i
    return False


def creating_matrix(transition, place, arco_teste):
    """
    A função recebe as transições, lugares e os arcos
    e retorna as matrizes de entrada, saida, inibidores, habilitadores e marcação inicial
    OBS: Transições, lugares e arcos são classes definidas neste programa
    :param transition Transição da Rede
    :param place Lugar da Rede
    :param arco_teste Arcos da Rede
    :return:  pre_entrada, post, ini, ena, m0
    """
    # Criando matrizes de pre_entrada e de saída
    linhas = len(transition)
    colunas = len(place)
    m0 = [[0.0] * colunas]
    pre = [[0.0] * colunas for i in range(linhas)]
    ini = [[0.0] * colunas for i in range(linhas)]
    ena = [[0.0] * colunas for i in range(linhas)]
    post = [[0.0] * colunas for i in range(linhas)]

    for i in range(colunas):
        m0[0][i] = place[i].initial_mark
    for arcos in arco_teste:
        for i in range(linhas):
            for j in range(colunas):
                if transition[i].key == arcos.finish_key and place[j].key == arcos.begin_key and arcos.tipo == 'normal':
                    pre[i][j] = arcos.weight + pre[i][j]
                if transition[i].key == arcos.finish_key and place[
                    j].key == arcos.begin_key and arcos.tipo == 'inhibitor':
                    ini[i][j] = arcos.weight + ini[i][j]
                if transition[i].key == arcos.finish_key and place[
                    j].key == arcos.begin_key and arcos.tipo == 'test arc':
                    ena[i][j] = arcos.weight + ena[i][j]
                if transition[i].key == arcos.begin_key and place[j].key == arcos.finish_key and arcos.tipo == 'normal':
                    post[i][j] = arcos.weight + post[i][j]
    return pre, post, ini, ena, m0


def gerar_matriz_alcancabilidade(prompt_saida, prompt_entrada, buttonExpMatrTex):
    buttonExpMatrTex.config(state="normal")
    prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + "Gerando matriz de alcançabilidade")
    N = prompt_entrada.get()
    global marcacoes, disparos
    marcacoes = marcacao_inicial.copy()
    try:
        N = int(N)
    except:
        N = 200
    prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + f'Realizando {N} repetições.')

    marcacoes, disparos = teste_marcacao(marcacao_inicial, N, prompt_saida)
    global matriz_q
    matriz_q = [[0] * len(disparos)] * len(disparos)
    prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + f'Tamanho disparos: {len(disparos)}')
    matriz_q = pd.DataFrame(matriz_q, index=disparos.index, columns=disparos.index)
    # Acessando os conjuntos de marcações disparadas
    for i in range(len(disparos)):
        # Acessando cada marcação e sua respectiva transição
        for j in range(len(disparos.iloc[0, :])):
            # Se o valor assinalado no disparo[i,j] for -2 significa que esta transição não ocorre para esta marcação
            if disparos.iloc[i, j] != -2:
                # Assimilando as taxas de transição descritas como "time_firing"
                matriz_q.iloc[i, disparos.iloc[i, j]] = transition_teste[j].time_firing
        # Ao final, faz-se a soma dos valores atribuidos na diagonal principal da matriz Q
        matriz_q.iloc[i, i] = -sum(matriz_q.iloc[i, :])
    prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + 'Matriz Q:')
    for m in matriz_q.values:
        prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + str(m))
    # resolvendo ax=b para x, pi*Q=*01'
    global vetor_pi
    vetor_pi = np.linalg.lstsq(np.r_[np.transpose(matriz_q.values), [[1] * len(matriz_q.iloc[0, :])]],
                               np.r_[np.zeros(len(matriz_q)), [1]], rcond=None)
    # a funcao do Numpy (linalg.lstsq recebe os valores da matriz Q e soluciona a equação linear não quadrática com uma
    # aproximação adequada para a redução dos erros associados, tal como em uma linearização de um sistema.
    print(vetor_pi[0])
    vet_pi = pd.DataFrame(vetor_pi[0])
    for v_pi in vetor_pi:
        prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + str(v_pi))


# uma bateria de testes da marcacao é realizada, primeiro criamos um DataFrame para as marcacoes disparadas
# cada transicao pode ou nao ser habilitada
def teste_marcacao(marcacao, N, prompt_saida):
    marcacoes_disparadas = pd.DataFrame([[-1] * len(transition_teste)], columns=nome_transitions)
    # print('As marcacoes disparadas ate agora sao:')
    # print(marcacoes_disparadas)
    m = 0 # determina a posição do disparo que esta sendo investigado
    # iniciand a marcacao teste com a marcacao inicial
    marcacoes_teste = marcacao.copy()
    # sao feitas N repeticoes, o sistema deve ser finito ou então não é estocástico.
    for k in range(N):
        # obter uma matriz comparando a marcacao com cada uma das transicoes da matriz de entrada
        #
        # aqui tambem deve entrar a verificacao de inibidores e habilitadores (fazer depois) $$$$$$$$$$$$$$$$$$$$$
        #
        # print("Teste da marcação:")
        # print('Teste da Entrada')
        # aqui vamos gerar uma matriz que nos diz quando os inibibores, entrada e habilitadores nos permitem operar
        teste = in_inibidores.gt(marcacao.values)
        teste += in_inibidores.eq(marcacao.iloc[0, :] * 0)
        teste *= pre_entrada.le(marcacao.values)
        teste *= en_habilitadores.le(marcacao.values)
        # dado o numero de transicoes repetimos o teste a seguir
        for i in range(len(transition_teste)):
            # verificando  se o conjunto satisfaz as condicoes de uma determinada transicao
            if all(teste.loc[transition_teste[i].name, :]):
                # print(f'Disparando: {transition_teste[i].name}')
                marcacao = marcacao - pre_entrada.loc[transition_teste[i].name]

                # verificando se a nova marcacao eh maior que zero
                if all(marcacao) > 0:
                    # print('Eh maior que zero!')
                    marcacao = marcacao + post_saida.loc[transition_teste[i].name]
                    # print('Marcacao atualizada')
                    # print(marcacao)
                    # verificando se a marcacao ja existe
                    indice = marcacao_existe(marcacao, marcacoes_teste)
                    # Se receber -1 significa que a marcacao não existe
                    if indice == -1:
                        # print('Atualizando marcacoes')
                        marcacoes_teste = pd.concat([marcacoes_teste, marcacao], ignore_index=True)
                        # print('Novas marcacoes:')
                        # print(marcacoes_teste)
                        marcacoes_disparadas = pd.concat(
                            [marcacoes_disparadas,
                             pd.DataFrame([[-1] * len(transition_teste)], columns=nome_transitions)],
                            ignore_index=True)
                        marcacoes_disparadas.loc[m, transition_teste[i].name] = len(marcacoes_disparadas) - 1
                    # caso contrario a marcação já existe
                    else:
                        # print('Marcacao ja existe')
                        marcacoes_disparadas.loc[m, transition_teste[i].name] = indice
                    marcacao = marcacao - post_saida.loc[transition_teste[i].name]
                    # print('Marcacao atualizada')
                    # print(marcacao)
                else:
                    # print('Eh menor que zero')
                    marcacoes_disparadas.loc[m, transition_teste[i].name] = -2

                # print('Revertendo disparo')
                marcacao = marcacao + pre_entrada.loc[transition_teste[i].name]
                # print('Marcacao atualizada')
                # print(marcacao)

            # caso o conjunto não satisfaça alguma condição de habilitadores ou inibidores, essa transição recebe
            # o valor -2 para denotar que não pode ser disparada por esta marcação.
            else:
                # print(f'A transição: {transition_teste[i].name} não foi disparada')
                marcacoes_disparadas.loc[m, transition_teste[i].name] = -2
            # print('Marcacao atual:')
            # print(marcacao)

        # print('As marcacoes alcancaveis sao:')
        # print(marcacoes_teste)

        # print('Diferença com a ultima marcacao')
        # print(marcacao.values - marcacoes_teste.iloc[-1:].values)
        for dif in marcacao.values - marcacoes_teste.iloc[-1:].values:
            if all(dif != 0):
                marcacao = marcacoes_teste.iloc[-1:]
                m = marcacoes_teste.iloc[-1:].index
                # print(f'Diferente de zero para {dif}')
                break
            # else:
            #     print(f'Igual a zero para {dif}')
            # print('Iniciando repeticao para nova marcacao...')

            ## Caso seja igual ao ultimo disparo
            for i in range(len(marcacoes_disparadas)):
                # print(f'Avaliando i={i}')
                # print(marcacoes_disparadas.loc[i,:].values)
                # print((all(marcacoes_disparadas.loc[i,:].values) == 0))
                tee = marcacoes_disparadas.iloc[0, :] * (0) - 1
                # print('Teste tee:')
                # print(tee)
                te = marcacoes_disparadas.eq(tee)
                # print('Teste de igualdade')
                # print(te.loc[i,:])
                if all(te.loc[i, :]):
                    # print('Marcacao NAO FOI testada')
                    marcacao = marcacoes_teste.iloc[i:(i + 1)]
                    m = marcacoes_teste.iloc[i:(i + 1)].index
                    break
                else:
                    # caso todas as marcacoes tenham sido testadas
                    # print('Marcacao JA FOI testada')
                    if (i == len(marcacoes_disparadas) - 1):
                        # print('Todas as marcacoes foram testadas')
                            return (marcacoes_teste, marcacoes_disparadas)
            break
        # print('Marcacoes disparadas')
        # print(marcacoes_disparadas)

        ## Finalizando as repeticoes de busca por novas marcacoes
    return marcacoes_teste, marcacoes_disparadas


def marcacao_existe(marcacao_teste, marcacoes_teste_ex):
    """ Recebe um vetor de marcações (marcacao_teste)
    e uma matriz com diversas marcações (marcacoes_teste_ex)
    Se já existe, retorna o indice da marcação à qual ela é igual (indice)
    Se não existe retorna menos um (-1)
    :param marcacao_teste:
    :param marcacoes_teste_ex:
    :return:
    """
    teste = marcacoes_teste_ex.eq(marcacao_teste.values)
    for i in range(len(marcacoes_teste_ex)):
        indice = teste.index[i]
        if all(teste.loc[indice, :]):
            # print('Marcação já existe')
            # print('____')

            return indice
    # print('Marcação ainda não existe')
    # print('____')
    return -1


def imprimir_tex(prompt_saida):
    # marcacoes.to_csv(r'.\my_data.csv', index=False)
    imprimindo_latex(marcacoes, 'marcacoes', prompt_saida)
    imprimindo_latex(post_saida, "saída", prompt_saida)
    imprimindo_latex(pre_entrada, "entrada", prompt_saida)
    imprimindo_latex(in_inibidores, "inibidores", prompt_saida)
    imprimindo_latex(en_habilitadores, "habilitadores", prompt_saida)
    imprimindo_latex(marcacao_inicial, "marcacao inicial", prompt_saida)
    imprimindo_latex(disparos, "marcacoes disparadas", prompt_saida)
    imprimindo_latex(vetor_pi[0], "Vetor Pi", prompt_saida)
    imprimindo_latex(matriz_q, "Matriz Q", prompt_saida)
    print(marcacoes)
    print(post_saida)
    print(pre_entrada)
    print(in_inibidores)
    print(en_habilitadores)
    print(marcacao_inicial)
    print(disparos)
    print(vetor_pi)
    print(matriz_q)


def imprimindo_latex(folha, folha_nome, prompt_saida):
    #    """
    #    Esta função recebe uma matriz ou vetor para ser impresso, esta função não retorna nada, apenas imprime no terminal
    #    ou então cria um arquivo para salvar as informações.
    #    :param folha:
    #    :param folha_nome:
    #    """
    prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + f'Imprimindo {folha_nome}:')
    try:
        for f in folha.values:
            prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + str(f))
    except:
        for f in folha:
            prompt_saida.insert(prompt_saida.index("end+1c linestart"), "\n" + str(f))
    # arq_text = open('tex_matriz.txt', 'a')
    # a = folha.style.to_latex(caption=f"matriz {folha_nome}")
    # arq_text.write(str(a))


class App:
    def __init__(self, root):
        entrada_texto_var = tk.StringVar()
        # Definindo titulo
        root.title("REM - Probabilidade em RdP Estocásticas Markovianas")
        # Definindo tamanho da janela
        width = 650
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)

        # Travando o tamanho da janela
        root.resizable(width=False, height=False)

        # Definindo botoes e seus atributos
        buttonAbrir = tk.Button(root)
        buttonAbrir["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        buttonAbrir["font"] = ft
        buttonAbrir["fg"] = "#000000"
        buttonAbrir["justify"] = "center"
        buttonAbrir["text"] = "Abrir"
        buttonAbrir.place(x=10, y=260, width=106, height=42)
        buttonAbrir["command"] = (lambda: self.clickOpen(buttonGerArvAlc, buttonExpMatrTex, saidaTextoPrompt))

        buttonLimparTela = tk.Button(root)
        buttonLimparTela["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        buttonLimparTela["font"] = ft
        buttonLimparTela["fg"] = "#000000"
        buttonLimparTela["justify"] = "center"
        buttonLimparTela["text"] = "Limpar Tela"
        buttonLimparTela.place(x=140, y=260, width=106, height=42)
        buttonLimparTela["command"] = (lambda: self.clickLimparTela(saidaTextoPrompt, saidaTextoLabel))

        buttonExpMatrTex = tk.Button(root)
        buttonExpMatrTex["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        buttonExpMatrTex["font"] = ft
        buttonExpMatrTex["fg"] = "#000000"
        buttonExpMatrTex["justify"] = "center"
        buttonExpMatrTex["text"] = "Exportar Matrizes \nem Tex"
        buttonExpMatrTex.place(x=10, y=370, width=107, height=42)
        buttonExpMatrTex["command"] = lambda: imprimir_tex(saidaTextoLabel)
        buttonExpMatrTex["state"] = 'disabled'

        buttonGerArvAlc = tk.Button(root)
        buttonGerArvAlc["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        buttonGerArvAlc["font"] = ft
        buttonGerArvAlc["fg"] = "#000000"
        buttonGerArvAlc["justify"] = "center"
        buttonGerArvAlc["text"] = "Gerar Árvore \nde Alcançabilidade"
        buttonGerArvAlc.place(x=10, y=420, width=106, height=43)
        buttonGerArvAlc["command"] = lambda: gerar_matriz_alcancabilidade(saidaTextoLabel, entradaTexto,
                                                                          buttonExpMatrTex)
        buttonGerArvAlc["state"] = 'disabled'

        buttonOk = tk.Button(root)
        buttonOk["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        buttonOk["font"] = ft
        buttonOk["fg"] = "#000000"
        buttonOk["justify"] = "center"
        buttonOk["text"] = "Ok"
        buttonOk.place(x=220, y=420, width=30, height=30)
        buttonOk["command"] = lambda: self.buttonOk_command(entradaTexto)

        frame = tk.Frame(root)
        frame.place(x=265, y=10, width=375, height=485)
        canva = tk.Canvas(frame)
        canva.pack(side="left", fill="both", expand=1)
        saidaTextoLabel = tk.Text(canva)
        saidaTextoLabel["bg"] = "#ffffff"
        # ft = tkFont.Font(family='Times', size=10)
        saidaTextoLabel["width"] = 365
        saidaTextoLabel.pack(side="left", fill="both", expand=1)
        barra_rolagem = tk.Scrollbar(frame, orient='vertical', command=saidaTextoLabel.yview)
        barra_rolagem.pack(side="right", fill="y")

        saidaTextoLabel.configure(yscrollcommand=barra_rolagem.set)
        saidaTextoLabel.bind('<Configure>', lambda e: canva.configure(scrollregion=canva.bbox("all")))

        saidaTextoPrompt = tk.Message(root)
        saidaTextoPrompt["bg"] = "#e3e3e3"
        ft = tkFont.Font(family='Times', size=10)
        saidaTextoPrompt["anchor"] = "nw"
        saidaTextoPrompt["font"] = ft
        saidaTextoPrompt["fg"] = "#333333"
        saidaTextoPrompt["justify"] = "left"
        saidaTextoPrompt["text"] = ""
        saidaTextoPrompt["width"] = 240
        saidaTextoPrompt.place(x=10, y=10, width=227, height=240)

        entradaTexto = tk.Entry(root)
        entradaTexto["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        entradaTexto["font"] = ft
        entradaTexto["textvariable"] = entrada_texto_var
        entradaTexto["fg"] = "#333333"
        entradaTexto["justify"] = "center"
        entradaTexto["text"] = "Entrada"
        entradaTexto.place(x=140, y=420, width=70, height=30)

    def ImprimirLabel(self, text_sai, text):
        """
        Exibir na label da direita
        """
        text_sai.insert(text_sai.index("end+1c linestart"), "\n" + text)

    def ImprimirPrompt(self, textoPrompt, text):
        """
        Exibir na label da esquerda
        """
        print(textoPrompt['text'])

    def clickLimparTela(self, textoPrompt, textoLabel):
        textoLabel.delete("0.0", "end")

    def clickOpen(self, buttonE, buttonG, textoPrompt):
        """
        Abrir RedePetri
        """
        self.filename = filedialog.askopenfile(initialdir="./RdP", title="Select file",
                                               filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        textoPrompt.config(text=f'Abrindo: {self.filename.name}', justify="left")
        texto = analisar(self.filename)
        if texto == "Dados carregados":
            buttonG.config(state="normal")
            buttonE.config(state="normal")
        else:
            buttonG.config(state="disable")
            buttonE.config(state="disable")
        nome_arquivo = self.filename.name[self.filename.name.find("RdP/")+len("RdP/"):]
        textoPrompt.config(text=f"Arquivo {nome_arquivo} aberto", justify="left")


    def buttonOk_command(self, entrada):
        valor = entrada.get()
        return valor


if __name__ == '__main__':
    # iniciando janela do tkinter

    # Abrir Rede Petri
    # Analisar
    # Buscar Árvore Alcançabilidade
    # Calcular vetor de propabilidade

    # Exportar Tex

    # Visualizar pm4py

    root = tk.Tk()
    myApp = App(root)
    root.mainloop()
    # # criar_log_Json()
