# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Alguma mudança no código

import tkinter as tk
import random
import string
import datetime
import json
from pymongo import MongoClient()


def increase():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value + 1}"


def decrease():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value - 1}"


class JanelaPrincipal(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.buttonquit()
        self.buttonsave()

    def buttonquit(self):
        """
        Creating Button Quit
        """
        self.quitButton = tk.Button(self, text="Sair", command=self.quit)
        self.quitButton.grid(row=0, column=0, padx=5, pady=5)

    def buttonsave(self, order=None):
        """
        Creating Button Save
        """
        if order is None or "":
            self.saveButton = tk.Button(self, text="Salvar")
            self.saveButton.grid(row=1, column=0, padx=5)
        else:
            self.saveButton = tk.Button(self, text="Salvar", command=order)
            self.saveButton.grid(row=1, column=0, padx=5)

def Salvar(self):
    arq = "teste.txt"
    dados = open('./Log/' + arq, 'r', encoding='latin-1')

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



if __name__ == '__main__':
    print('Iniciando REM - Redes de Petri Estocásticas Markovianas')

    app = JanelaPrincipal()
    app.master.title('Iniciando REM - Redes de Petri Estocásticas Markovianas')
    print("Mudança pra teste de commit")
    # app.bind("<Key>", app.buttonSave())
    criar_log_Json()
    app.mainloop()

    # janela_principal = tk.Tk()
    #
    # janela_principal.title("REM - Redes de Petri Estocásticas Markovianas")
    # janela_principal.rowconfigure(0, minsize=800, weight=1)
    # janela_principal.columnconfigure(1, minsize=800, weight=1)
    #
    # txt_edit = tk.Text(janela_principal)
    # frm_buttons = tk.Frame(janela_principal, relief=tk.RAISED, bd=2)
    # btn_open = tk.Button(frm_buttons, text="Open")
    # btn_save = tk.Button(frm_buttons, text="Save As...")
    #
    # # Dimensionando janela
    # janela_principal.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
