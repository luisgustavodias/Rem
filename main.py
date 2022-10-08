# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# Alguma mudança no código

import tkinter as tk

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def increase():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value + 1}"

def decrease():
    value = int(lbl_value["text"])
    lbl_value["text"] = f"{value - 1}"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    print('Mudando um pouquinho')
    a = 1
    window = tk.Tk()
    janela_principal = tk.Tk()
    janela_principal.title("REM - Redes de Petri Estocásticas Markovianas")

    janela_principal.rowconfigure(0, minsize=800, weight=1)
    janela_principal.columnconfigure(1, minsize=800, weight=1)

    txt_edit = tk.Text(janela_principal)
    frm_buttons = tk.Frame(janela_principal, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(frm_buttons, text="Open")
    btn_save = tk.Button(frm_buttons, text="Save As...")

    window.resizable(width=True, height=True)
    #Dimensionando janela

    window.rowconfigure(0, minsize=50, weight=1)
    window.columnconfigure([0, 1, 2], minsize=50, weight=1)

    btn_decrease = tk.Button(master=window, text="-", command=decrease)
    btn_decrease.grid(row=0, column=0, sticky="nsew")

    lbl_value = tk.Label(master=window, text="0")
    lbl_value.grid(row=0, column=1)

    btn_increase = tk.Button(master=window, text="+", command=increase)
    btn_increase.grid(row=0, column=2, sticky="nsew")
    window.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
