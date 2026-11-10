# Definição da Topologia
# Este arquivo importa as configurações do config.py para
# construir a topologia de forma dinâmica.


# topologia.py

from mininet.topo import Topo
from config import HOST_1, HOST_2, SWITCH_NAME


class MinhaTopo(Topo):

    def build(self):
        # Cria os hosts utilizando os dados do arquivo de configuração
        h1 = self.addHost(HOST_1['name'], ip=HOST_1['ip'])
        h2 = self.addHost(HOST_2['name'], ip=HOST_2['ip'])

        # Cria o switch
        s1 = self.addSwitch(SWITCH_NAME)

        # Conecta os links
        self.addLink(h1, s1)
        self.addLink(h2, s1)