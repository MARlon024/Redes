import ipaddress
import math

# Dirección IP y número de subredes
# Solicitar la dirección IP al usuario
while True:
    ip = input("Introduzca una dirección IP: ")
    try:
        ipaddress.IPv4Address(ip)
        break
    except ValueError:
        print("Dirección IP inválida. Por favor, introduzca una dirección IP válida.")

while True:
    num_subnets = input("Introduzca el número de subredes: ")
    try:
        num_subnets = int(num_subnets)
        if num_subnets < 1:
            raise ValueError
        break
    except ValueError:
        print("Número de subredes inválido. Por favor, introduzca un número entero mayor que 0.")

# Pregunta al usuario si desea introducir un prefijo
introducir_prefijo = input("¿Desea introducir un prefijo? (Yes?): ").lower()

# Si el usuario desea introducir un prefijo, se le pide que lo haga
if introducir_prefijo == 'yes':
    try:
        prefijo = int(input("Introduzca un prefijo (1-32): "))
        if prefijo < 1 or prefijo > 32:
            raise ValueError
    except ValueError:
        print("Prefijo inválido. Se asumirá el prefijo por defecto según la clase de IP.")
        prefijo = None
else:
    prefijo = None

# Si el prefijo es None, calculamos el prefijo por defecto basándonos en la clase de la dirección IP
if prefijo is None:
    if ipaddress.IPv4Address(ip) in ipaddress.IPv4Network('0.0.0.0/8'):
        prefijo = 8  # Clase A
    elif ipaddress.IPv4Address(ip) in ipaddress.IPv4Network('128.0.0.0/16'):
        prefijo = 16  # Clase B
    else:
        prefijo = 24  # Clase C

# Crear una red utilizando la dirección IP y el prefijo por defecto si no se introdujo un prefijo
network = ipaddress.ip_network(ip + '/' + str(prefijo), strict=False)

# Calcular el nuevo prefijo
if math.log2(num_subnets).is_integer():
    new_prefix = network.prefixlen + int(math.log2(num_subnets))
else:
    new_prefix = network.prefixlen + int(math.log2(num_subnets)) + 1

# Crear las subredes
subnets = list(network.subnets(new_prefix=new_prefix))

# Imprimir la tabla de subredes
print('Subred\tNº de Hosts\tIP de red\tMáscara\tPrimer Host\tÚltimo Host\tBroadcast')
for i, subnet in enumerate(subnets[:num_subnets], 1):
    num_hosts = len(list(subnet.hosts()))
    print(f'Subred {i}\t{num_hosts}\t{subnet.network_address} /{new_prefix}\t{subnet.netmask}\t{subnet.network_address + 1}\t{subnet.broadcast_address - 1}\t{subnet.broadcast_address}')
