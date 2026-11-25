from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import OVSSwitch


class Topologia(Topo):

    def build(self):

        # Criação dos hosts.
        h1 = self.addHost(
            'h1',
            ip='10.0.0.1/24'
        )

        h2 = self.addHost(
            'h2',
            ip='10.0.0.2/24'
        )

        h3 = self.addHost(
            'h3',
            ip='10.0.0.3/24'
        )

        h4 = self.addHost(
            'h4',
            ip='10.0.0.4/24'
        )

        # Criação do switch.
        s1 = self.addSwitch(
            's1',
            failMode='standalone'
        )

        # Conexão dos hosts ao switch.
        self.addLink(h1, s1, cls=TCLink, delay='10ms')
        self.addLink(h2, s1, cls=TCLink, delay='10ms')
        self.addLink(h3, s1, cls=TCLink, delay='10ms')
        self.addLink(h4, s1, cls=TCLink, delay='10ms')


if __name__ == '__main__':

    topo = Topologia()

    net = Mininet(
        topo=topo,
        controller=None,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True
    )

    try:

        net.start()

        print("\nTopologia iniciada com sucesso!")

        print("\nTestando conectividade entre os hosts...")

        net.pingAll()

        CLI(net)

    finally:

        net.stop()
