from mininet.topo import Topo

class TopoAnel(Topo):
    """ Topologia em Anel/Linha com N hosts """
    def build(self, num_hosts=4):
        switch = self.addSwitch('s1')# preciso usar um switch no mininet para emular uma topologia de anel?
        for i in range(1, num_hosts + 1):
            ip_host = f"10.0.0.{i}/24"
            host = self.addHost(f'h{i}', ip=ip_host)
            self.addLink(host, switch)