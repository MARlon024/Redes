#flsm_gui.py
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ipaddress

def clear_entries(ip_entry, prefix_entry, num_subnets_entry):
    # Borrar el contenido de cada campo de entrada
    ip_entry.delete(0, tk.END)
    prefix_entry.delete(0, tk.END)
    num_subnets_entry.delete(0, tk.END)

def calculate_flsm(root, ip_entry, num_subnets_entry, prefix_entry, var):
    ip = ip_entry.get()
    num_subnets = int(num_subnets_entry.get())
    prefix_yes_no = var.get()

    if prefix_yes_no == 'yes':
        try:
            prefix = int(prefix_entry.get())
            if prefix < 1 or prefix > 32:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Prefijo inválido. Se asumirá el prefijo por defecto según la clase de IP.")
            prefix = None
    else:
        prefix = None

    if prefix is None:
        if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network('0.0.0.0/8'):
            prefix = 8  # Clase A
        elif ipaddress.IPv4Address(ip) in ipaddress.IPv4Network('128.0.0.0/16'):
            prefix = 16  # Clase B
        else:
            prefix = 24  # Clase C

    # Crear una red utilizando la dirección IP y el prefijo por defecto si no se introdujo un prefijo
    network = ipaddress.ip_network(ip + '/' + str(prefix))
    
    # Calcular el nuevo prefijo
    if math.log2(num_subnets).is_integer():
        new_prefix = network.prefixlen + int(math.log2(num_subnets))
    else:
        new_prefix = network.prefixlen + int(math.log2(num_subnets)) + 1

    # Crear las subredes
    subnets = list(network.subnets(new_prefix=new_prefix))

    # Crear una nueva ventana para mostrar los resultados
    result_window = tk.Toplevel(root)

    # Crear un Treeview para mostrar los resultados en formato de tabla
    tree = ttk.Treeview(result_window, columns=('Subred', 'Nº de Hosts', 'IP de red', 'Máscara', 'Primer Host', 'Último Host', 'Broadcast'), show='headings')

    # Configurar las columnas
    for col in ('Subred', 'Nº de Hosts', 'IP de red', 'Máscara', 'Primer Host', 'Último Host', 'Broadcast'):
        tree.heading(col, text=col)

    # Añadir los datos a la tabla
    for i, net in enumerate(subnets[:num_subnets], 1):
        num_hosts = len(list(net.hosts()))
        tree.insert('', 'end', values=(f'Subred {i}', num_hosts, f'{net.network_address} /{new_prefix}', net.netmask, net.network_address + 1, net.broadcast_address - 1, net.broadcast_address))

    tree.pack()

    
    clear_entries(ip_entry, prefix_entry, num_subnets_entry)
