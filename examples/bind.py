#!/usr/bin/env python

"""
Aqui está a tradução do texto para o português:

**bind.py: Exemplo de montagem por ligação (bind mount)**

Isto cria hosts com diretórios privados especificados pelo usuário. Estes hosts podem ter diretórios persistentes que estarão disponíveis ao longo de múltiplas sessões do Mininet, ou diretórios temporários que durarão apenas durante uma sessão do Mininet. Para especificar um diretório persistente, adicione uma tupla a uma lista de diretórios privados:

```
[ ( 'diretório a ser montado em', 'diretório a ser montado' ) ]

```

A expansão de strings pode ser usada para criar um modelo de diretório para cada host. Para fazer isso, adicione `%(name)s` no lugar do nome do host ao criar sua lista de diretórios:

```
[ ( '/var/run', '/tmp/%(name)s/var/run' ) ]

```

Se nenhum diretório persistente for especificado, os diretórios padrão serão temporários e privados. Para fazer isso, basta criar uma lista dos diretórios que devem se tornar privados. Um sistema de arquivos em memória (`tmpfs`) será então montado sobre eles.

Você pode usar diretórios temporários e persistentes ao mesmo tempo. Na seguinte string de `privateDirs`, cada host terá um diretório persistente no sistema de arquivos raiz em `"/tmp/(nome_do_host)/var/run"` montado em `"/var/run"`. Cada host também terá um diretório privado temporário montado em `"/var/log"`.

```
[ ( '/var/run', '/tmp/%(name)s/var/run' ), '/var/log' ]

```

Este exemplo possui diretórios persistentes montados em `'/var/log'` e `'/var/run'`. Ele também possui um diretório privado temporário montado em `'/var/mn'`.
"""

from functools import partial

from mininet.net import Mininet
from mininet.node import Host
from mininet.cli import CLI
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel, info


# Exemplo de uso

def testHostWithPrivateDirs():
    "Test bind mounts"
    topo = SingleSwitchTopo( 10 )
    privateDirs = [ ( '/var/log', '/tmp/%(name)s/var/log' ),
                    ( '/var/run', '/tmp/%(name)s/var/run' ),
                      '/var/mn' ]
    host = partial( Host,
                    privateDirs=privateDirs )
    net = Mininet( topo=topo, host=host, waitConnected=True )
    net.start()
    directories = [ directory[ 0 ] if isinstance( directory, tuple )
                    else directory for directory in privateDirs ]
    info( 'Private Directories:', directories, '\n' )
    CLI( net )
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    testHostWithPrivateDirs()
    info( 'Done.\n')
