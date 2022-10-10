""" Trabalho Final de Graduação - UNIFEI 05.2023 - 10/10/2022-10:49 - testando tkinter gerado online
Obtenção do vetor de probabilidades dos estados de uma rede de petri limitada e estocástica
utilizando cadeias de markov.
Autor: Luis Gustavo Dias Simão
Orientador: Luiz Edival de Souza
"""
import pandas as pd
import numpy as np
import random
import string
import datetime
import json
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog
# # from pymongo import MongoClient
# from pm4py.objects.petri.petrinet import PetriNet, Marking
# from pm4py.objects.petri import utils, reachability_graph
# from pm4py.visualization.transition_system import visualizer
# import pm4py as pm
import prompt_toolkit.widgets


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
    key = 0

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
    initial_mark = 0.0
    capacity = -1.0
    key = 0

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
    begin_key = 0
    finish_key = 0
    weight = 0.0
    tipo = ""

    def __init__(self, beg_k, fin_k, wei, tip):
        self.begin_key = beg_k
        self.finish_key = fin_k
        self.weight = wei
        self.tipo = tip


def criar_log_Json():
    """
    Esta funcao cria um arquivo Json teste para a rede Petri
    """
    # proteção para inserção múltipla
    inseridos = False

    # semente para os geradores aleatórios
    random.seed(int(input('Forneça sua matrícula: ')))

    # lista de letras maiusculas e números
    letras = string.ascii_uppercase + string.digits

    # gerando dispositivos e sensores  com texto aleatório
    dispositivos = []
    for _ in range(random.randint(2, 4)):
        # nome do dispositivo aleatório
        nome_dispositivo = ''.join(random.choice(letras) for i in range(7))
        # sensores do dispositivo
        sensores = []
        for _ in range(random.randint(4, 10)):
            # nome do sensor aleatório
            nome_sensor = ''.join(random.choice(letras) for i in range(5))
            tipo = random.choice(['booleano', 'float', 'int', 'texto'])
            sensores.append({'sensor': nome_sensor, 'tipo': tipo})
        # adiciondo dispositivo
        dispositivos.append({'dispositivo': nome_dispositivo, 'sensores': sensores})
    print(f'Dispositivos ({len(dispositivos)}):')
    for d in dispositivos:
        print('   ', d)

    # gerando instantes de medição
    instantes = []
    inicio = datetime.datetime(2022, random.randint(1, 5), random.randint(1, 28))
    for i in range(random.randint(30000, 40000)):
        inicio += datetime.timedelta(seconds=1)
        instantes.append(inicio)

    # gerando medidas
    medidas = []
    for instante in instantes:
        for dispositivo in dispositivos:
            # gerando valores nos sensores
            valores = []
            for sensor in dispositivo['sensores']:
                if sensor['tipo'] == 'booleano':
                    valores.append(random.choice([False, True]))
                elif sensor['tipo'] == 'float':
                    valores.append(round(random.random() * 200.0 - 100.0, 2))
                elif sensor['tipo'] == 'int':
                    valores.append(random.randint(-100, 100))
                elif sensor['tipo'] == 'texto':
                    valores.append(''.join(random.choice(letras) for i in range(3)))
            # inserindo medidas
            medida = {
                'dispositivo': dispositivo['dispositivo'],
                'instante': instante,
            }
            for s, v in zip(dispositivo['sensores'], valores):
                medida[s['sensor']] = v
            medidas.append(medida)
    # medições obtidas
    print(f'Medições ({len(medidas)}):')
    for m in medidas[:10]:
        print('   ', m)
    with open('medidas.json', 'w') as file:
        json.dump(medidas, file, indent=3, sort_keys=True, default=str)

    with open('medidas.json', 'r') as file:
        for _ in range(20):
            print(file.readline(), end='')


def loading_data(dados):
    """
    Carrega os dados em texto, cria então três vetores, com os lugares, transições e arcos
    OBS: Transições, lugares e arcos são classes definidas neste programa
    :param: dados
    :return: place_teste, transition_teste, arc_teste
    """
    arc_teste = [Arcs('', '', 0.0, '')]  # creating arc list
    arc_teste.pop(0)
    place_teste = [Places('', '', '', 0.0, -1, 0)]  # creating place list
    place_teste.pop(0)
    transition_teste = [Transitions('', '', '', 1, 0)]
    transition_teste.pop(0)

    # Strip the message to obtain the dados
    for line in dados:
        line = line.strip('     ')
        line = line.rstrip()

        # Loading...
        # Arcs
        if line.startswith('from '):
            inicio = line[line.find('from ') + len('from '):line.find(' (key')]
            begin_key = int(line[line.find(inicio) + len(inicio) + len(' (key='):line.find(') t')])
            final = 7 + line.find(str(begin_key))
            final = line[final:line.find('), t')]
            finish_key = int(final[final.find('(key=') + len('(key='):])
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
                initial_mark = float(line[(line.find('marking: ') + len('marking: ')):line.find(', capacity: ')])
            except:
                initial_mark = float(line[(line.find('marking: ') + len('marking: ')):line.find(', key:')])
            try:
                capacity = float(line[line.find('capacity: ') + len('capacity: '):line.find(', key:')])
            except:
                capacity = -1
            key = int(line[line.find('key: ') + len('key: '):])

            place_teste.append(Places(name, tipo, variable_name, initial_mark, capacity, key))

        # Transitions
        if line.startswith('name: '):
            name = line[6:line.find(', typ')]
            tipo = line[(line.find('typ: ') + len('typ: ')):line.find(', ')]
            key = int(line[line.find('key: ') + len('key: '):])
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

    return (place_teste, transition_teste, arc_teste)


def creating_matrix(transition, place, arco_teste):
    """
    A função recebe as transições, lugares e os arcos
    e retorna as matrizes de entrada, saida, inibidores, habilitadores e marcação inicial
    OBS: Transições, lugares e arcos são classes definidas neste programa
    :param transition
    :param place
    :param arco_teste
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

    for i in range(colunas): m0[0][i] = place[i].initial_mark
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


def creating_petri_net(petri_transition, petri_place, petri_arc):
    net = PetriNet("RedePetriTeste")
    init_mark = Marking()
    for place in petri_place:
        net.places.add(PetriNet.Place(place.name))
        print(f"Nome do place: {place.name}")
        init_mark[PetriNet.Place(place.name)] = place.initial_mark
        print(init_mark[PetriNet.Place(place.name)])
    for transition in petri_transition:
        net.transitions.add(PetriNet.Place(transition.name, transition.key))
    for arc in petri_arc:
        for transition in petri_transition:
            for place in petri_place:
                if transition.key == arc.finish_key and place.key == arc.begin_key and arc.tipo == 'normal':
                    utils.add_arc_from_to(PetriNet.Place(place.name),
                                          PetriNet.Transition(transition.name, transition.key), net, arc.weight)
                if transition.key == arc.begin_key and place.key == arc.finish_key and arc.tipo == 'normal':
                    utils.add_arc_from_to(PetriNet.Transition(transition.name, transition.key),
                                          PetriNet.Place(place.name), net, arc.weight)
                if transition.key == arc.finish_key and place.key == arc.begin_key and arc.tipo == 'inhibitor':
                    utils.add_arc_from_to(PetriNet.Place(place.name),
                                          PetriNet.Transition(transition.name, transition.key), net, arc.weight)
                if transition.key == arc.finish_key and place.key == arc.begin_key and arc.tipo == 'test arc':
                    utils.add_arc_from_to(PetriNet.Place(place.name),
                                          PetriNet.Transition(transition.name, transition.key), net, arc.weight)
    print(net)
    return net, init_mark


def teste_marcacao(marcacao, N):
    marcacoes_disparadas = pd.DataFrame([[-1] * len(transition_teste)], columns=nome_transitions)
    # print('As marcacoes disparadas ate agora sao:')
    # print(marcacoes_disparadas)
    m = 0
    marcacoes_teste = marcacao.copy()
    ind = 0
    for k in range(N):
        # obter uma matriz comparando a marcacao com cada uma das transicoes da matriz de entrada
        # aqui tambem deve entrar a verificacao de inibidores e habilitadores (fazer depois)
        # print("Teste da marcação:")
        print(marcacao.dtypes)
        # print('Teste da Entrada')
        teste = in_inibidores.gt(marcacao.values)
        teste += in_inibidores.eq(marcacao.iloc[0, :] * 0)
        teste *= pre_entrada.le(marcacao.values)
        teste *= en_habilitadores.le(marcacao.values)

        for i in range(len(transition_teste)):

            # verificando  conjunto
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
                    if indice == -1:
                        # print('Atualizando marcacoes')
                        marcacoes_teste = pd.concat([marcacoes_teste, marcacao], ignore_index=True)
                        # print('Novas marcacoes:')
                        # print(marcacoes_teste)
                        marcacoes_disparadas = pd.concat(
                            [marcacoes_disparadas, pd.DataFrame([[-1] * len(transition_teste)], columns=nome_transitions)],
                            ignore_index=True)
                        marcacoes_disparadas.loc[m, transition_teste[i].name] = len(marcacoes_disparadas) - 1
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
                    # print('Marcacao JA FOI testada')
                    if (i == len(marcacoes_disparadas) - 1):
                        # print('Todas as marcacoes foram testadas')
                        return (marcacoes_teste, marcacoes_disparadas)
            break
        # print('Marcacoes disparadas')
        # print(marcacoes_disparadas)

        ## Finalizando as repeticoes de busca por novas marcacoes
    return marcacoes_teste, marcacoes_disparadas


def imprimindo_latex(folha, folha_nome):
    """
    Esta função recebe uma matriz ou vetor para ser impresso, esta função não retorna nada, apenas imprime no terminal
    ou então cria um arquivo para salvar as informações.
    :param folha:
    :param folha_nome:
    """
    print(f'''
Imprimindo {folha_nome}:''')
    print(folha)
    # arq_text = open('tex_matriz.txt', 'a')
    # a = folha.style.to_latex(caption=f"matriz {folha_nome}")
    # arq_text.write(str(a))


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


def analisar(data):
    # Junto ao programa deverá existir uma pasta com o arquivo exportado do VON
    global place_teste, transition_teste, arc_teste
    # loading_data carrega os lugares, transicoes e arcos
    place_teste, transition_teste, arc_teste = loading_data(data)
    global nome_transitions, nome_places
    nome_transitions = [''] * len(transition_teste)
    nome_places = [''] * len(place_teste)
    # carregando os nomes dos lugares e transicoes *** importante que nao existam nomes repetidos
    i = 0
    for c in place_teste:
        nome_places[i] = c.name
        i += 1
    i = 0
    for l in transition_teste:
        nome_transitions[i] = l.name
        i += 1
    # creating_matrix gera as matrizes Pre, Post, In, En, M0
    # dada determinados conjuntos de [Transition], [Place], [Arc]

    pre_entrada_np, post_saida_np, in_inibidores_np, en_habilitadores_np, marcacao_inicial_np = creating_matrix(
        transition_teste, place_teste, arc_teste)
    global pre_entrada, post_saida, in_inibidores, en_habilitadores, marcacao_inicial
    # Reformatando dados para DataFrame da biblioteca do Pandas
    pre_entrada = pd.DataFrame(pre_entrada_np, index=nome_transitions, columns=nome_places)
    post_saida = pd.DataFrame(post_saida_np, index=nome_transitions, columns=nome_places)
    in_inibidores = pd.DataFrame(in_inibidores_np, index=nome_transitions, columns=nome_places)
    en_habilitadores = pd.DataFrame(en_habilitadores_np, index=nome_transitions, columns=nome_places)
    marcacao_inicial = pd.DataFrame(marcacao_inicial_np, columns=nome_places)

    # post_saida recebe os valores negativos por isso a soma abaixo
    incidencia = pre_entrada + post_saida

def gerar_matriz_alcancabilidade():

    N = 100
    global marcacoes, disparos
    marcacoes = marcacao_inicial.copy()
    try:
        N = int(N)
    except:
        N = 10
    print(f'Realizando {N} repetições.')
    marcacoes, disparos = teste_marcacao(marcacao_inicial, N)
    matriz_q = [[0] * len(disparos)] * len(disparos)
    print(f'Tamanho disparos: {len(disparos)}')
    matriz_q = pd.DataFrame(matriz_q, index=disparos.index, columns=disparos.index)
    for i in range(len(disparos)):
        for j in range(len(disparos.iloc[0, :])):
            if disparos.iloc[i, j] != -2:
                matriz_q.iloc[i, disparos.iloc[i, j]] = transition_teste[j].time_firing
                print(f'disparo{i}x{disparos.iloc[i, j]} = {transition_teste[j].time_firing}')
        matriz_q.iloc[i, i] = -sum(matriz_q.iloc[i, :])
    print('Matriz Q:')
    print(matriz_q)
    # resolvendo ax=b para x, pi*Q=*01'
    vetor_pi = np.linalg.lstsq(np.r_[np.transpose(matriz_q.values), [[1] * len(matriz_q.iloc[0, :])]],
                               np.r_[np.zeros(len(matriz_q)), [1]], rcond=None)
    for v_pi in vetor_pi:
        print(v_pi)

    if (1 == 0):  # input("Converter arquivos para PM4PY? (S/N): ") == "S"):
        rdp_teste, rdp_marcacao_inicial = creating_petri_net(transition_teste, place_teste, arc_teste)
        print(rdp_teste)
        print(rdp_marcacao_inicial)
        rdp_marcacao_final = pm.objects.petri_net.utils.final_marking.discover_final_marking(rdp_teste)
        print(rdp_marcacao_final)

def imprimir_tex():
    # marcacoes.to_csv(r'.\my_data.csv', index=False)
    imprimindo_latex(marcacoes, 'marcacoes')
    imprimindo_latex(post_saida, "saída")
    imprimindo_latex(pre_entrada, "entrada")
    imprimindo_latex(in_inibidores, "inibidores")
    imprimindo_latex(en_habilitadores, "habilitadores")
    imprimindo_latex(marcacao_inicial, "marcacao inicial")
    imprimindo_latex(disparos, "marcacoes disparadas")



def openRdP():
    global arq
    arq = root.filename
    analisar()


class App:
    def __init__(self, root):
        #setting title
        entrada_texto_var = tk.StringVar()
        root.title("REM - Probabilidade em RdP Estocásticas Markovianas")
        #setting window size
        width=650
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        ButtonAbrir=tk.Button(root)
        ButtonAbrir["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        ButtonAbrir["font"] = ft
        ButtonAbrir["fg"] = "#000000"
        ButtonAbrir["justify"] = "center"
        ButtonAbrir["text"] = "Abrir"
        ButtonAbrir.place(x=10,y=10,width=106,height=42)
        ButtonAbrir["command"] = (lambda: self.clickOpen(ButtonExpMatrTex, ButtonGerArvAlc, ButtonGerModJson, ButtonSobrando, SaidaTextoPrompt))

        EntradaTexto=tk.Entry(root)
        EntradaTexto["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        EntradaTexto["font"] = ft
        EntradaTexto["textvariable"] = entrada_texto_var
        EntradaTexto["fg"] = "#333333"
        EntradaTexto["justify"] = "center"
        EntradaTexto["text"] = "Entrada"
        EntradaTexto.place(x=30,y=280,width=80,height=30)

        SaidaTextoPrompt=tk.Message(root)
        SaidaTextoPrompt["bg"] = "#e3e3e3"
        ft = tkFont.Font(family='Times',size=10)
        SaidaTextoPrompt["font"] = ft
        SaidaTextoPrompt["fg"] = "#333333"
        SaidaTextoPrompt["justify"] = "left"
        SaidaTextoPrompt["text"] = ""
        SaidaTextoPrompt["relief"] = "flat"
        SaidaTextoPrompt.place(x=10,y=330,width=625,height=157)

        ButtonExpMatrTex=tk.Button(root)
        ButtonExpMatrTex["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        ButtonExpMatrTex["font"] = ft
        ButtonExpMatrTex["fg"] = "#000000"
        ButtonExpMatrTex["justify"] = "center"
        ButtonExpMatrTex["text"] = "Exportar Matrizes \nem Tex"
        ButtonExpMatrTex.place(x=30,y=60,width=107,height=42)
        ButtonExpMatrTex["command"] = imprimir_tex
        ButtonExpMatrTex["state"] = 'disabled'

        ButtonGerArvAlc=tk.Button(root)
        ButtonGerArvAlc["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        ButtonGerArvAlc["font"] = ft
        ButtonGerArvAlc["fg"] = "#000000"
        ButtonGerArvAlc["justify"] = "center"
        ButtonGerArvAlc["text"] = "Gerar Árvore \nde Alcançabilidade"
        ButtonGerArvAlc.place(x=30,y=110,width=106,height=43)
        ButtonGerArvAlc["command"] = gerar_matriz_alcancabilidade
        ButtonGerArvAlc["state"] = 'disabled'

        ButtonGerModJson=tk.Button(root)
        ButtonGerModJson["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        ButtonGerModJson["font"] = ft
        ButtonGerModJson["fg"] = "#000000"
        ButtonGerModJson["justify"] = "center"
        ButtonGerModJson["text"] = "Gerar Modelo \nem Json"
        ButtonGerModJson.place(x=30,y=160,width=107,height=41)
        ButtonGerModJson["command"] = self.ButtonGerModJson_command
        ButtonGerModJson["state"] = 'disabled'

        SaidaTextoLabel=tk.Label(root)
        SaidaTextoLabel["bg"] = "#ffffff"
        ft = tkFont.Font(family='Times',size=10)
        SaidaTextoLabel["font"] = ft
        SaidaTextoLabel["fg"] = "#333333"
        SaidaTextoLabel["justify"] = "left"
        SaidaTextoLabel["text"] = "label"
        SaidaTextoLabel.place(x=160,y=10,width=474,height=303)

        ButtonSobrando=tk.Button(root)
        ButtonSobrando["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        ButtonSobrando["font"] = ft
        ButtonSobrando["fg"] = "#000000"
        ButtonSobrando["justify"] = "center"
        ButtonSobrando["text"] = "Sobrando"
        ButtonSobrando.place(x=30,y=210,width=109,height=41)
        ButtonSobrando["command"] = (lambda: self.clickSave(EntradaTexto, SaidaTextoLabel))

        ButtonOk=tk.Button(root)
        ButtonOk["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        ButtonOk["font"] = ft
        ButtonOk["fg"] = "#000000"
        ButtonOk["justify"] = "center"
        ButtonOk["text"] = "Ok"
        ButtonOk.place(x=120,y=280,width=30,height=30)
        ButtonOk["command"] = self.ButtonOk_command

    def clickSave(self, text_ent, text_sai):
        """
        Teste Button to save
        """
        text_sai.config(text=text_sai['text']+"\n"+text_ent.get())

    def clickOpen(self, buttonE, buttonG, buttonJ, buttonS, textoPrompt):
        """
        Abrir RedePetri
        """
        self.filename = filedialog.askopenfile(initialdir="./RdP", title="Select file",
                                               filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        textoPrompt.config(text=f"Abrindo: {self.filename.name}", justify="left")
        analisar(self.filename)
        textoPrompt.config(text=textoPrompt["text"]+"\nFechando..", justify="left")
        buttonE.config(state="normal")
        buttonG.config(state="normal")

    def ButtonOk_command(self):
        print("command")

    def ButtonGerModJson_command(self):
        print('commad')

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