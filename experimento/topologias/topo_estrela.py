from mininet.topo import Topo

class TopoEstrela(Topo):
    """ Topologia em Estrela simples com N hosts """
    def build(self, num_hosts=4):
        switch_central = self.addSwitch('s1')
        for i in range(1, num_hosts + 1):
            ip_host = f"10.0.0.{i}/24"
            host = self.addHost(f'h{i}', ip=ip_host)
            self.addLink(host, switch_central)