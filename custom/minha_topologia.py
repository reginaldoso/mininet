from mininet.topo import Topo

class TopologiaPersonalizada(Topo):
    def build(self):
        # Criação dos hosts
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')
        
        # Criação do switch
        s1 = self.addSwitch('s1')
        
        # Conexões
        self.addLink(h1, s1)
        self.addLink(h2, s1)

topos = { 'custom_topo': (lambda: TopologiaPersonalizada()) }