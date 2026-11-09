import subprocess
import time

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch
from mininet.log import setLogLevel, info


class MinhaTopo(Topo):

    def build(self):
        h1 = self.addHost('h1', ip='10.0.0.1/24')
        h2 = self.addHost('h2', ip='10.0.0.2/24')

        s1 = self.addSwitch('s1')

        self.addLink(h1, s1)
        self.addLink(h2, s1)


def executar():

    info('\n*** Limpando recursos do Mininet\n')
    subprocess.run(['mn', '-c'], check=True)

    topo = MinhaTopo()
    net = Mininet(topo=topo, switch=OVSSwitch)

    captura_iniciada = False
    pid = None

    try:

        # Inicializa a rede
        net.start()

        h1 = net.get('h1')
        h2 = net.get('h2')

        info('\n*** Iniciando captura ICMP em h1\n')

        # Remove arquivo de captura anterior
        h1.cmd('rm -f /tmp/captura_icmp.txt')

        # Inicia tcpdump em segundo plano e registra seu PID
        h1.cmd(
            'tcpdump -l -i h1-eth0 -n -tttt icmp '
            '> /tmp/captura_icmp.txt 2>&1 & echo $! '
            '> /tmp/tcpdump.pid'
        )

        # Aguarda a inicialização do tcpdump
        for tentativa in range(30):

            pid = h1.cmd(
                'cat /tmp/tcpdump.pid 2>/dev/null'
            ).strip()

            if pid:
                break

            time.sleep(0.1)

        if not pid:
            raise RuntimeError('Não foi possível iniciar o tcpdump.')

        captura_iniciada = True

        info('*** PID do tcpdump: %s\n' % pid)

        # Executa o ping
        info('\n*** Executando ping de h1 para h2\n')

        resultado = h1.cmd('ping -c 4 10.0.0.2')

        info(resultado)

    finally:

        if captura_iniciada:

            info('\n*** Encerrando captura\n')

            # Envia SIGINT ao processo tcpdump
            h1.cmd('kill -INT %s' % pid)

            # Aguarda o encerramento efetivo
            encerrado = False

            for tentativa in range(50):

                estado = h1.cmd(
                    'ps -p %s -o stat= 2>/dev/null' % pid
                ).strip()

                if not estado or estado.startswith('Z'):
                    encerrado = True
                    break

                time.sleep(0.1)

            if not encerrado:
                info('*** Tempo limite atingido. Enviando SIGKILL.\n')
                h1.cmd('kill -KILL %s' % pid)

                time.sleep(0.2)

            # Exibe os pacotes capturados
            info('\n*** Pacotes capturados:\n')

            saida = h1.cmd(
                'cat /tmp/captura_icmp.txt'
            )

            info(saida)

            # Remove arquivos temporários
            h1.cmd(
                'rm -f /tmp/captura_icmp.txt /tmp/tcpdump.pid'
            )

        info('\n*** Encerrando Mininet\n')

        net.stop()

        info('\n*** Experimento finalizado!\n')


if __name__ == '__main__':

    setLogLevel('info')

    executar()
