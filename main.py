#

import tkinter as tk


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



if __name__ == '__main__':
    print('Iniciando REM - Redes de Petri Estocásticas Markovianas')

    app = JanelaPrincipal()
    app.master.title('Iniciando REM - Redes de Petri Estocásticas Markovianas')
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
