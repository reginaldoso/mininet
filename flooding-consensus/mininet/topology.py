from mininet.topo import Topo


class ConsensusTopology(Topo):

    def build(self, n=5):

        switch = self.addSwitch("s1")

        for i in range(1, n + 1):

            host = self.addHost(
                f"h{i}",
                ip=f"10.0.0.{i}/24"
            )

            self.addLink(host, switch)


topos = {
    "consensus": lambda: ConsensusTopology(n=5)
}
