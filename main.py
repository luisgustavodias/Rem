# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Alguma mudança no código

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
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text="Sair", command=self.quit)
        self.quitButton.grid()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Iniciando REM - Redes de Petri Estocásticas Markovianas')
    janela_principal = tk.Tk()

    janela_principal.title("REM - Redes de Petri Estocásticas Markovianas")
    janela_principal.rowconfigure(0, minsize=800, weight=1)
    janela_principal.columnconfigure(1, minsize=800, weight=1)

    txt_edit = tk.Text(janela_principal)
    frm_buttons = tk.Frame(janela_principal, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(frm_buttons, text="Open")
    btn_save = tk.Button(frm_buttons, text="Save As...")

    # Dimensionando janela
    janela_principal.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
