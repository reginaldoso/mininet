#!/usr/bin/env python

"""
cpu.py: testa a largura de banda do iperf para diferentes limites de CPU.

Como estamos limitando apenas os hosts, devemos esperar que os processos do iperf sejam afetados, 
assim como qualquer processamento do sistema que seja contabilizado como pertencente aos hosts.
Reservamos mais de 50% dos ciclos da CPU para o processamento do sistema; presumimos que isso 
seja suficiente para que ele não afete os resultados. Os hosts são limitados a 40% do total de
ciclos, o que presumimos ser suficiente para torná-los limitados pela CPU (CPU-bound).
À medida que o desempenho das CPUs aumenta ao longo do tempo, talvez seja necessário reduzir a 
alocação total de CPU para que o processamento dos hosts continue sendo limitado pela CPU (CPU-bound).
Isso talvez seja um argumento a favor de especificar o desempenho de uma maneira mais independente do sistema.
Também seria interessante ter um controle melhor sobre a limitação dos ciclos da CPU destinados ao processamento
de pacotes. Não está totalmente claro para mim como esses ciclos são contabilizados entre os processos de usuário
e os processos do sistema quando utilizamos o OVS com um kernel datapath. Com um user datapath, é mais fácil 
contabilizá-los, mas o desempenho geral geralmente é menor.
Embora o cliente iperf utilize mais CPU e devesse estar limitado pela CPU (CPU-bound) (?), medimos os dados 
recebidos no servidor, pois a taxa de transmissão do cliente inclui o preenchimento de buffers.
"""

from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.topolib import TreeTopo
from mininet.util import custom, waitListening, decode
from mininet.log import setLogLevel, info
from mininet.clean import cleanup

def bwtest( cpuLimits, period_us=100000, seconds=10 ):
    """Example/test of link and CPU bandwidth limits
       cpu: cpu limit as fraction of overall CPU time"""

    topo = TreeTopo( depth=1, fanout=2 )

    results = {}

    for sched in 'rt', 'cfs':
        info( '*** Testing with', sched, 'bandwidth limiting\n' )
        for cpu in cpuLimits:
            # cpu is the cpu fraction for all hosts, so we divide
            # it across two hosts
            host = custom( CPULimitedHost, sched=sched,
                           period_us=period_us,
                           cpu=.5*cpu )
            try:
                net = Mininet( topo=topo, host=host, waitConnected=True )
            # pylint: disable=bare-except
            except:  # noqa
                info( '*** Skipping scheduler %s and cleaning up\n' % sched )
                cleanup()
                break
            net.start()
            net.pingAll()
            hosts = [ net.getNodeByName( h ) for h in topo.hosts() ]
            client, server = hosts[ 0 ], hosts[ -1 ]
            info( '*** Starting iperf with %d%% of CPU allocated to hosts\n' %
                  ( 100.0 * cpu ) )
            # We measure at the server because it doesn't include
            # the client's buffer fill rate
            popen = server.popen( 'iperf -yc -s -p 5001' )
            waitListening( client, server, 5001 )
            client.cmd( 'iperf -yc -t %s -c %s' % ( seconds, server.IP() ) )
            # ignore empty result from waitListening/telnet for old iperf
            svals = {}
            while not svals or int( svals[ 'rate' ] ) == 0:
                line = decode( popen.stdout.readline() )
                # Probably shouldn't depend on an internal method, but
                # this is the easiest way
                svals = Mininet._iperfVals(  # pylint: disable=protected-access
                    line, server.IP() )
            bps = float( svals[ 'rate' ] )
            popen.terminate()
            net.stop()
            updated = results.get( sched, [] )
            updated += [ ( cpu, bps ) ]
            results[ sched ] = updated

    return results


def dump( results ):
    "Dump results"

    fmt = '%s\t%s\t%s\n'

    info( '\n' )
    info( fmt % ( 'sched', 'cpu', 'received bits/sec' ) )

    for sched in sorted( results.keys() ):
        entries = results[ sched ]
        for cpu, bps in entries:
            pct = '%d%%' % ( cpu * 100 )
            mbps = '%.2e' % bps
            info( fmt % ( sched, pct, mbps ) )


if __name__ == '__main__':
    setLogLevel( 'info' )
    # These are the limits for the hosts/iperfs - the
    # rest is for system processes
    limits = [ .5, .4, .3, .2, .1 ]
    out = bwtest( limits )
    dump( out )
