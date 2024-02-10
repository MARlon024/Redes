# main.py

import tkinter as tk
from VLSM.vlsm_widget import create_vlsm_widget
from FLSM.flsm_widget import create_flsm_widget

vlsm_frame = None
flsm_frame = None

def show_vlsm():
    global vlsm_frame, flsm_frame
    # Destruir el frame de FLSM anterior si existe
    if flsm_frame is not None:
        flsm_frame.destroy()
    # Destruir el frame de VLSM anterior si existe
    if vlsm_frame is not None:
        vlsm_frame.destroy()
    # Crear y mostrar widgets de VLSM
    vlsm_frame = create_vlsm_widget(root)
    vlsm_frame.pack()

def show_flsm():
    global vlsm_frame, flsm_frame
    # Destruir el frame de VLSM anterior si existe
    if vlsm_frame is not None:
        vlsm_frame.destroy()
    # Crear y mostrar widgets de FLSM
    flsm_frame = create_flsm_widget(root)
    flsm_frame.pack()

root = tk.Tk()

button_frame = tk.Frame(root)
button_frame.pack()

button1 = tk.Button(button_frame, text="Calculadora VLSM", command=show_vlsm)
button1.pack(side=tk.LEFT)

button2 = tk.Button(button_frame, text="Calculadora FLSM", command=show_flsm)
button2.pack(side=tk.LEFT)

root.mainloop()
