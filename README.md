Mininet: Prototipagem Rápida para Redes Definidas por Software (SDN)


Versão: Mininet 2.3.1b4

![Status do Build][1]



O Mininet emula uma rede completa de hosts, links e switches em uma única máquina.

Para criar uma rede de exemplo com dois hosts e um switch, basta executar:

sudo mn


O Mininet é útil para desenvolvimento interativo, testes e demonstrações, especialmente em projetos que utilizam OpenFlow e Redes Definidas por Software (SDN — Software-Defined Networking).

Os controladores de rede baseados em OpenFlow, desenvolvidos e testados em protótipos no Mininet, geralmente podem ser transferidos para equipamentos físicos com alterações mínimas, permitindo a execução em velocidade de linha (line rate).

Como funciona?

O Mininet cria redes virtuais utilizando virtualização baseada em processos e network namespaces (espaços de nomes de rede), recursos disponíveis nos kernels Linux modernos.

No Mininet, os hosts são emulados como processos bash executados em um network namespace. Dessa forma, qualquer código que normalmente seria executado em um servidor Linux, como um servidor web ou um programa cliente, também deve funcionar normalmente dentro de um host do Mininet.

Cada host do Mininet possui sua própria interface de rede privada e consegue visualizar apenas seus próprios processos.

Os switches do Mininet são switches implementados em software, como o Open vSwitch ou o switch de referência do OpenFlow.

Os links são pares de interfaces Ethernet virtuais que existem no kernel Linux e conectam os switches emulados aos hosts emulados, que são representados por processos.

Recursos

O Mininet oferece os seguintes recursos:

Inicializador por linha de comando (mn): permite criar e instanciar redes.
API Python: facilita a criação de redes de diferentes tamanhos e topologias.
Exemplos práticos: disponíveis no diretório examples/, ajudam você a começar a utilizar a ferramenta.
Documentação completa da API: disponível por meio das docstrings acessíveis com a função help() do Python. Também é possível gerar a documentação em PDF ou HTML executando make doc.
Topologias parametrizadas: permite definir topologias por meio de subclasses de Topo, utilizando os objetos do Mininet. Por exemplo, uma rede em árvore pode ser criada com o comando:
mn --topo tree,depth=2,fanout=3

Interface de linha de comando (CLI): a classe CLI fornece comandos úteis para diagnóstico, como iperf e ping, além de permitir a execução de comandos diretamente nos nós da rede.

Por exemplo:

mininet> h11 ifconfig -a


Esse comando solicita que o host h11 execute o comando ifconfig -a.

Comando de limpeza: remove resíduos que podem permanecer no sistema após a utilização do Mininet ou de outros processos Linux, incluindo interfaces, processos e arquivos no diretório /tmp.

Se a ferramenta parar de funcionar corretamente, experimente executar:

sudo mn -c

Suporte ao Python 3
O Mininet 2.3.1b4 oferece suporte ao Python 3 e ao Python 2.
É possível instalar as versões do Mininet para Python 2 e Python 3 lado a lado. Entretanto, a instalação mais recente determinará qual versão do Python será utilizada por padrão pelo comando mn.
Você pode executar o comando mn diretamente com Python 2 ou Python 3, desde que a versão correspondente do Mininet esteja instalada.

Por exemplo, para executar o Mininet com Python 2:

sudo python2 "$(which mn)"

Mais informações sobre a compatibilidade com Python 2 e Python 3 podem ser encontradas nas notas de lançamento disponíveis na documentação oficial do Mininet.
Outras melhorias e informações

A versão 2.3.1b4 inclui as seguintes melhorias e recursos:

Suporte ao Ubuntu 22.04 LTS e ao Ubuntu 20.04.
Testes mais confiáveis e integração contínua (CI) por meio do GitHub Actions.
Suporte preliminar ao cgroups v2 e v1.
Pequenas correções de bugs na versão 2.3.1.

Informações adicionais sobre esta versão e as versões anteriores estão disponíveis nas notas de lançamento da documentação oficial do Mininet.

Instalação

Consulte o arquivo INSTALL do projeto para obter instruções detalhadas sobre a instalação.

Documentação

Além da documentação da API, que pode ser gerada com o comando make doc, há diversos materiais úteis para aprender a utilizar o Mininet.

Entre eles estão:

Site oficial: Mininet.
Tutorial prático: apresenta os principais recursos e comandos da ferramenta.
Introdução à API Python: explica como criar e configurar redes programaticamente.
Wiki: contém informações adicionais e materiais de referência.
Perguntas frequentes (FAQ): disponível em faq.mininet.org.

A comunidade incentiva os usuários a consultar a wiki e a contribuir com melhorias para a documentação.

Suporte

O Mininet é mantido com o apoio de sua comunidade.

Os usuários são incentivados a participar da lista de discussão mininet-discuss, disponível no seguinte endereço:

Lista de discussão do Mininet

Nesse espaço, é possível compartilhar dúvidas, trocar experiências e discutir assuntos relacionados ao desenvolvimento e à utilização da ferramenta.

Participe do projeto

Agradecemos novamente a todos os colaboradores e usuários do Mininet!

O Mininet é um projeto de código aberto, atualmente hospedado no GitHub:

Repositório oficial do Mininet

Você pode baixar, examinar e modificar o código-fonte, além de contribuir com:

Relatórios de bugs.
Correções de problemas.
Solicitações de novos recursos (feature requests).
Implementação de novas funcionalidades.
Relatos de outros problemas (issues).
Solicitações de integração de código (pull requests).

Agradecemos a todas as pessoas que contribuíram com o projeto. Consulte o arquivo CONTRIBUTORS para obter mais informações.

É graças ao trabalho e à dedicação de toda a comunidade que o Mininet continua crescendo e evoluindo.

Aproveite o Mininet!

Divirta-se!

Estamos ansiosos para descobrir como você utilizará o Mininet para transformar o mundo das redes de computadores.

Bob Lantz
Em nome de todos os colaboradores do Mininet.