#!/usr/bin/env python

import sys
import subprocess
from mininet.node import Host
from mininet.util import ensureRoot, waitListening
from mininet.log import info, warn, output

print("*** Limpando recursos residuais...")
subprocess.run(['mn', '-c'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ensureRoot()
timeout = 5

info( "*** Creating nodes\n" )
h1 = Host( 'h1' )
root = Host( 'root', inNamespace=False )

info( "*** Creating link\n" )
h1.linkTo( root )

info( "*** Configuring nodes\n" )
h1.setIP( '10.0.0.1', 8 )
root.setIP( '10.0.0.2', 8 )

# Ativa a interface loopback dentro do namespace do h1
h1.cmd( 'ifconfig lo up' )

info( "*** Creating banner file\n" )
with open( '/tmp/%s.banner' % h1.name, 'w' ) as f:
    f.write( 'Welcome to %s at %s\n' % ( h1.name, h1.IP() ) )

info( "*** Running sshd\n" )
cmd = '/usr/sbin/sshd -o UseDNS=no -u0 -o "Banner /tmp/%s.banner"' % h1.name
if len( sys.argv ) > 1:
    cmd += ' ' + ' '.join( sys.argv[ 1: ] )

# Executa o sshd dentro do h1
h1.cmd( cmd )

# Passa explicitamente o IP do h1 (10.0.0.1) para o waitListening
listening = waitListening( server=h1.IP(), port=22, timeout=timeout )

if listening:
    output( "*** You may now ssh into", h1.name, "at", h1.IP(), '\n' )
else:
    # Se falhar, mostra o erro do sshd executando em modo interativo/test
    warn( "*** Debugging sshd error:\n" )
    warn( h1.cmd( '/usr/sbin/sshd -t' ) )