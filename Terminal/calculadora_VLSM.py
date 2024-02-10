import ipaddress

class Subnet:
    def __init__(self, name, hosts):
        self.name = name
        self.hosts = hosts

class VLSM:
    def __init__(self, ip, subnets):
        self.ip = ipaddress.ip_network(ip)
        self.subnets = sorted(subnets, key=lambda x: x.hosts, reverse=True)

    def calculate(self):
        results = []
        total_hosts_requested = 0
        total_addresses_required = 0
        for subnet in self.subnets:
            n = 32
            while (2 ** (32 - n)) - 2 < subnet.hosts:
                n -= 1
            net = list(self.ip.subnets(new_prefix=n))[0]
            self.ip = list(self.ip.subnets(new_prefix=n))[1]
            total_hosts_requested += subnet.hosts
            total_addresses_required += net.num_addresses - 2  # Restamos 2 para excluir la dirección de red y de broadcast
            results.append((subnet.name, net))
        return total_hosts_requested, total_addresses_required, results
    
while True:
    ip = input("Introduzca una dirección IP: ")
    try:
        ipaddress.IPv4Address(ip)
        break
    except ValueError:
        print("Dirección IP inválida. Por favor, introduzca una dirección IP válida.")

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
network = ip + '/' + str(prefijo)

# Solicitar al usuario el número de subredes y la cantidad de hosts por cada subred
subnets = []
num_subnets = int(input("Introduzca el número de subredes: "))
for i in range(1, num_subnets + 1):
    while True:
        hosts = input(f"Introduzca el número de hosts para la subred {i}: ")
        try:
            hosts = int(hosts)
            if hosts < 1:
                raise ValueError
            subnets.append(Subnet(f'Subred {i}', hosts))
            break
        except ValueError:
            print("Número de hosts inválido. Por favor, introduzca un número entero mayor que 0.")

vlsm = VLSM(network, subnets)
total_hosts_requested, total_addresses_required, results = vlsm.calculate()
total_hosts_available=pow(2,(32-prefijo))-2
print(f"Número total de hosts solicitados: {total_hosts_requested}")
print(f"Número de direcciones requeridas: {total_addresses_required}")
print(f"Número total de hosts disponibles: {total_hosts_available}")
print(f"Número de IPv4: {network}")

print("...........")
print("Subred\tNº de Hosts\tIP de red\tMáscara\tPrimer Host\tÚltimo Host\tBroadcast")
for name, net in results:
    print(f'{name}\t{net.num_addresses - 2}\t{net.network_address}/{net.prefixlen}\t{net.netmask}\t{net.network_address + 1}\t{net.broadcast_address - 1}\t{net.broadcast_address}')
