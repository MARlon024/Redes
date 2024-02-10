import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from VLSM.vlsm_calcu import Subnet, VLSM
import ipaddress


def clear_entries(ip_entry, prefix_entry, num_subnets_entry, host_entries):
    # Borrar el contenido de cada campo de entrada
    ip_entry.delete(0, tk.END)
    prefix_entry.delete(0, tk.END)
    num_subnets_entry.delete(0, tk.END)
    for entry in host_entries:
        entry.delete(0, tk.END)

def clear_host_entries(host_widgets, host_entries):
    # Destruir cada widget de entrada de hosts
    for label, entry in host_widgets:
        label.destroy()
        entry.destroy()
    host_entries.clear()
    host_widgets.clear()

def create_host_entries(vlsm_frame, num_subnets_entry, host_entries, host_widgets):
    # Crear campos de entrada para el número de hosts por subred
    for i in range(1, int(num_subnets_entry.get()) + 1):
        host_label = tk.Label(vlsm_frame, text=f"Introduzca el número de hosts para la subred {i}:")
        host_label.pack()
        host_entry = tk.Entry(vlsm_frame)
        host_entry.pack()
        host_entries.append(host_entry)
        host_widgets.append((host_label, host_entry))
  

def calculate_vlsm(root, ip_entry, num_subnets_entry, prefix_entry, var, host_entries, host_widgets):
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
    network = ip + '/' + str(prefix)

    # Solicitar al usuario el número de subredes y la cantidad de hosts por cada subred
    subnets = []
    for i in range(1, num_subnets + 1):
        hosts = int(host_entries[i-1].get())
        subnets.append(Subnet(f'Subred {i}', hosts))

    vlsm = VLSM(network, subnets)
    total_hosts_requested, total_addresses_required, results = vlsm.calculate()
    total_hosts_available=pow(2,(32-prefix))-2

    # Crear una nueva ventana para mostrar los resultados
    result_window = tk.Toplevel(root)

    # Crear un Treeview para mostrar los resultados en formato de tabla
    tree = ttk.Treeview(result_window, columns=('Subred', 'Nº de Hosts', 'IP de red', 'Máscara', 'Primer Host', 'Último Host', 'Broadcast'), show='headings')

    # Configurar las columnas
    for col in ('Subred', 'Nº de Hosts', 'IP de red', 'Máscara', 'Primer Host', 'Último Host', 'Broadcast'):
        tree.heading(col, text=col)

    # Añadir los datos a la tabla
    for name, net in results:
        num_hosts = net.num_addresses - 2
        tree.insert('', 'end', values=(name, num_hosts, f'{net.network_address}/{net.prefixlen}', net.netmask, net.network_address + 1, net.broadcast_address - 1, net.broadcast_address))

    tree.pack()


    clear_entries(ip_entry, prefix_entry, num_subnets_entry, host_entries)
    clear_host_entries(host_widgets, host_entries)
 