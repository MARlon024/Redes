import tkinter as tk
from FLSM.flsm_gui import calculate_flsm

def create_flsm_widget(root):
    flsm_frame = tk.Frame(root)

    # Widgets para VLSM
    ip_label = tk.Label(flsm_frame, text="Introduzca una dirección IP:")
    ip_label.pack()
    ip_entry = tk.Entry(flsm_frame)
    ip_entry.pack()

    prefix_label = tk.Label(flsm_frame, text="¿Desea introducir un prefijo?")
    prefix_label.pack()
    var = tk.StringVar(value="no")
    prefix_yes = tk.Radiobutton(flsm_frame, text="Yes", variable=var, value="yes", command=lambda: show_prefix_entry())
    prefix_yes.pack()
    prefix_no = tk.Radiobutton(flsm_frame, text="No", variable=var, value="no", command=lambda: hide_prefix_entry())
    prefix_no.pack()

    prefix_entry_label = tk.Label(flsm_frame, text="Introduzca un prefijo (1-32):")
    prefix_entry = tk.Entry(flsm_frame)

    num_subnets_label = tk.Label(flsm_frame, text="Introduzca el número de subredes:")
    num_subnets_label.pack()
    num_subnets_entry = tk.Entry(flsm_frame)
    num_subnets_entry.pack()

    result_text = tk.StringVar()
    result_label = tk.Label(flsm_frame, textvariable=result_text)
    result_label.pack()

    calculate_button = tk.Button(flsm_frame, text="Calcular", command=lambda: calculate_flsm(root, ip_entry, num_subnets_entry, prefix_entry, var))
    calculate_button.pack()

    def show_prefix_entry():
        num_subnets_label.pack_forget()
        num_subnets_entry.pack_forget()
        result_label.pack_forget()
        calculate_button.pack_forget()
        prefix_entry_label.pack()
        prefix_entry.pack()
        num_subnets_label.pack()
        num_subnets_entry.pack()
        result_label.pack()
        calculate_button.pack()

    def hide_prefix_entry():
        prefix_entry_label.pack_forget()
        prefix_entry.pack_forget()

    if var.get() == "no":
        hide_prefix_entry()

    return flsm_frame
