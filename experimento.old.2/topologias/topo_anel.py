from mininet.topo import Topo

class TopoAnel(Topo):
    """ Topologia em Anel real com N hosts conectados ponto a ponto """
    def build(self, num_hosts=4):
        hosts = [self.addHost(f'h{i}') for i in range(1, num_hosts + 1)]

        for i in range(num_hosts):
            h_atual = hosts[i]
            h_prox = hosts[(i + 1) % num_hosts]
            self.addLink(
                h_atual,
                h_prox,
                params1={'ip': f'10.0.{i + 1}.1/30'},
                params2={'ip': f'10.0.{i + 1}.2/30'}
            )