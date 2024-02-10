# vlsm_calculator.py

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
