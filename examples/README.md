Exemplos do Mininet
========================================================

Estes exemplos destinam-se a ajudar você a começar a usar
a API em Python do Mininet.

========================================================

#### baresshd.py:

Este exemplo usa a API de médio nível do Mininet para criar um processo sshd em execução em um namespace. Não utiliza OpenFlow.

#### bind.py:

Este exemplo mostra como você pode criar diretórios privados para cada nó em uma topologia do Mininet.

#### cluster.py:

Este exemplo contém todo o código para a edição experimental em cluster. Classes remotas e a `MininetCluster` podem ser importadas a partir daqui para criar uma topologia com nós em máquinas remotas.

#### clusterSanity.py:

Este exemplo executa a edição em cluster localmente como um teste de sanidade para verificar a funcionalidade básica.

#### clustercli.py:

Este exemplo contém uma CLI para a edição experimental em cluster.

#### clusterdemo.py:

Este exemplo é uma demonstração básica da edição em cluster em 3 servidores com uma topologia em árvore de profundidade 3 e *fanout* 3.

#### consoles.py:

Este exemplo cria uma grade de janelas de console, uma para cada nó, e permite a interatividade e o monitoramento de cada console, incluindo monitoramento gráfico.

#### controllers.py:

Este exemplo cria uma rede com múltiplos controladores, utilizando uma subclasse customizada de `Switch()`.

#### controllers2.py:

Este exemplo cria uma rede com múltiplos controladores criando uma rede vazia, adicionando nós a ela e iniciando os switches manualmente.

#### controlnet.py:

Este exemplo mostra como você pode modelar a rede de controle assim como a rede de dados, criando efetivamente dois objetos Mininet.

#### cpu.py:

Este exemplo testa a largura de banda com o `iperf` para diferentes limites de CPU.

#### emptynet.py:

Este exemplo demonstra a criação de uma rede vazia (ou seja, sem objeto de topologia) e a adição de nós a ela.

#### hwintf.py:

Este exemplo mostra como adicionar uma interface (por exemplo, uma interface de hardware real) a uma rede após a rede ter sido criada.

#### intfoptions.py:

Este exemplo reconfigura uma `TCIntf` durante o tempo de execução com diferentes comandos de controle de tráfego para testar largura de banda, perda e atraso.

#### limit.py:

Este exemplo mostra como usar limites de enlace (*link*) e de CPU.

#### linearbandwidth.py:

Este exemplo mostra como criar uma topologia personalizada via código herdando a classe `Topo`, e como executar uma série de testes nela.

#### linuxrouter.py:

Este exemplo mostra como criar e configurar um roteador no Mininet que utiliza o redirecionamento IP (*IP forwarding*) do Linux.

#### miniedit.py:

Este exemplo demonstra a criação de uma rede por meio de um editor gráfico.

#### mobility.py:

Este exemplo demonstra o desligamento de uma interface de um switch e sua conexão a outro, como uma forma básica de mover um host pela rede.

#### multiLink.py:

Este exemplo demonstra a criação de múltiplos enlaces entre nós utilizando uma classe personalizada de topologia.

#### multiping.py:

Este exemplo demonstra um método para monitorar a saída de múltiplos hosts utilizando `node.monitor()`.

#### multipoll.py:

Este exemplo demonstra o monitoramento de arquivos de saída de múltiplos hosts.

#### multitest.py:

Este exemplo cria uma rede e executa múltiplos testes nela.

#### nat.py:

Este exemplo mostra como conectar uma rede do Mininet à Internet usando NAT. Ele também responde à eterna pergunta: "por que não consigo dar ping no `google.com`?"

#### natnet.py:

Este exemplo demonstra como criar uma rede usando um nó NAT para conectar hosts à internet.

#### numberedports.py:

Este exemplo verifica se os números de porta do Mininet (`ofport`) coincidem com os números de porta do OVS. Também verifica se os números de porta coincidem com os números das interfaces.

#### popen.py:

Este exemplo monitora vários hosts usando `host.popen()` e `pmonitor()`.

#### popenpoll.py:

Este exemplo demonstra o monitoramento da saída de múltiplos hosts utilizando a interface `node.popen()` (que retorna objetos `Popen`) e o `pmonitor()`.

#### scratchnet.py, scratchnetuser.py:

Estes dois exemplos demonstram como criar uma rede usando as funções de mais baixo nível do Mininet. Geralmente, a API de alto nível é mais fácil de usar, mas o *scratchnet* mostra o que está acontecendo por trás dos panos.

#### simpleperf.py:

Um exemplo simples de configuração de limites de largura de banda de rede e CPU.

#### sshd.py:

Este exemplo mostra como executar um processo `sshd` em cada host, permitindo que você faça login via `ssh`. Isso requer a conexão da rede de dados do Mininet a uma interface no namespace raiz (geralmente a rede de controle já reside no namespace raiz, portanto não precisa ser conectada explicitamente).

#### tree1024.py:

Este exemplo tenta criar uma rede de 1024 hosts e, em seguida, executa a CLI nela. Ele pode atingir limites de escalabilidade, dependendo da memória disponível e da configuração do `sysctl` (veja o arquivo `INSTALL`).

#### treeping64.py:

Este exemplo cria uma rede em árvore com 64 hosts e tenta verificar a conectividade total usando `ping`, para diferentes tipos de switch/datapath.

#### vlanhost.py:

Um exemplo de como criar uma subclasse de `Host` para usar uma VLAN em sua interface principal.