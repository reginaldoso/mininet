# Projetos de Algoritmos Distribuídos com Mininet

## Objetivo

Desenvolver, testar e manter algoritmos distribuídos utilizando o Mininet como ambiente de experimentação.
Este repositório foi usado durante a disciplina Projeto Final de Curso 2, em 2026.2.

## Estrutura do repositório

O repositório contém uma organização personalizada. Os experimentos de algoritmos distribuídos serão adicionados à pasta `algoritmos/`, preservando os diretórios e arquivos originais do Mininet.

A estrutura proposta é:

```text
mininet/
├── .github/
├── algoritmos/
│   ├── README.md               # Documentação dos experimentos
│   ├── 01_basic_communication.py
│   ├── 02_multiple_hosts.py
│   ├── 03_broadcast.py
│   ├── 04_gather.py
│   ├── 05_leader_election.py
│   ├── 06_lamport_clock.py
│   ├── 07_mutual_exclusion.py
│   ├── 08_heartbeat.py
│   ├── 09_distributed_average.py
│   └── hosts/
│       ├── client.py           # Cliente de comunicação reutilizável
│       └── server.py           # Servidor de comunicação reutilizável
├── bin/
├── build/
├── custom/
├── debian/
├── doc/
├── examples/
├── mininet/                        # Implementação original do Mininet
├── mininet.egg-info/
├── rascunhos/
├── util/
├── .gitattributes
├── .gitignore
├── .pylintrc
├── CONTRIBUTORS
├── INSTALL
├── LICENSE
├── Makefile
├── mn.1
├── mnexec
├── mnexec.1
├── mnexec.c
├── projetos.md                     # Planejamento dos experimentos
├── README.md                       # Documentação original do Mininet
└── setup.py
```

**Observação:** os diretórios originais do Mininet devem ser preservados.

### Responsabilidade de diretórios e arquivos

* **`custom/`**: contém os códigos que geram as topologias personalizadas de rede.
* **`examples/`**: contém exemplos de utilização do Mininet.
* **`examples/distributed/`**: contém os scripts responsáveis por criar as topologias, iniciar os processos e executar os algoritmos distribuídos.
* **`algoritmos/hosts/`**: contém programas auxiliares executados pelos hosts virtuais, como clientes e servidores de comunicação.
* **`algoritmos/README.md`**: documenta os experimentos, os requisitos e os procedimentos de execução.
* **`README.md`**: mantém o planejamento geral, a ordem de implementação e as instruções de desenvolvimento.
* **`mininet/`**: contém a implementação original do Mininet. Não deve ser utilizado como diretório para armazenar os algoritmos experimentais.
* **`util/`**: contém ferramentas auxiliares do Mininet. Não deve ser utilizado para armazenar a lógica dos algoritmos distribuídos.

## Como utilizar a estrutura

### Acessar o diretório dos experimentos

Todos os comandos devem ser executados a partir da raiz do repositório, salvo indicação contrária.

Para acessar a pasta dos experimentos:

```bash
cd examples/distributed
```

Para voltar à raiz do repositório:

```bash
cd ../..
```

Para listar os experimentos disponíveis:

```bash
ls -la examples/distributed
```

Para consultar a documentação específica dos experimentos:

```bash
cat examples/distributed/README.md
```

### Executar os experimentos

Os scripts de experimentação serão responsáveis por criar uma topologia Mininet, iniciar os hosts virtuais, executar os programas necessários e apresentar os resultados.

Para executar um experimento, utilize o Python 3:

```bash
sudo python3 examples/distributed/01_basic_communication.py
```

O comando acima pressupõe que o script esteja implementado para criar e gerenciar sua própria instância do Mininet.
Os programas auxiliares poderão ser executados nos hosts virtuais por meio dos métodos de execução de comandos disponibilizados pelo Mininet.

Por exemplo, um script poderá utilizar:

```python
from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel

def main():
    topo = SingleSwitchTopo(k=2)
    net = Mininet(topo=topo)

    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')

    print('IP de h1:', h1.IP())
    print('IP de h2:', h2.IP())

    # Iniciar os programas e executar o experimento.

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    main()
```

Esse código é apenas um exemplo de criação da topologia. Os experimentos completos implementam também a inicialização dos processos, a troca de mensagens e o encerramento adequado da rede.

Para verificar a conectividade entre hosts, também é possível utilizar o CLI do Mininet:

```bash
sudo mn --topo single,2 --mac
```

Dentro do CLI:

```text
mininet> pingall
mininet> h1 ip addr
mininet> h2 ip addr
mininet> exit
```

A opção `--mac` solicita a atribuição de endereços MAC associados aos identificadores dos hosts, facilitando a identificação dos participantes durante os experimentos.

**Importante:** antes de executar um novo experimento, verifique se não há instâncias anteriores do Mininet em execução. Encerre cada topologia adequadamente para evitar conflitos de recursos e interfaces virtuais.

### Como atualizar um algoritmo existente

Cada algoritmo deverá possuir um arquivo próprio. Para modificar um experimento, abra o arquivo correspondente e atualize sua implementação.

Por exemplo:

```bash
nano examples/distributed/01_basic_communication.py
```

Ou abra o arquivo no editor de código utilizado no projeto.

Após modificar o código:

1. Salve as alterações.
2. Execute novamente o experimento.
3. Verifique se a topologia é criada corretamente.
4. Confira se os hosts conseguem trocar mensagens.
5. Analise os resultados e as mensagens de erro.
6. Atualize a documentação caso o comportamento ou a forma de execução tenha mudado.

*Sempre que possível, preserve uma versão funcional do algoritmo antes de introduzir modificações maiores. Isso facilita a comparação entre implementações e a identificação de erros.*

### Como adicionar um novo algoritmo

Para incluir um novo experimento:

1. Consulte este arquivo para verificar a sequência planejada.
2. Escolha um nome descritivo e uma numeração coerente com a ordem dos experimentos.
3. Crie o arquivo na pasta `examples/distributed/`.
4. Implemente a topologia e a lógica do algoritmo.
5. Reutilize os programas auxiliares de `hosts/` quando isso for apropriado.
6. Execute o experimento e valide seus resultados.
7. Documente o funcionamento no `examples/distributed/README.md`.
8. Atualize este arquivo se a inclusão modificar o planejamento geral.

Exemplo de criação de um novo experimento:

```bash
touch examples/distributed/10_new_algorithm.py
```

O nome definitivo deverá refletir o algoritmo implementado.

Se o novo projeto exigir um programa auxiliar específico, crie-o na pasta `hosts/` ou em um subdiretório dedicado, conforme a complexidade do experimento.

Não é necessário criar uma pasta separada para cada algoritmo simples. Um arquivo Python por experimento é suficiente enquanto os projetos compartilharem uma estrutura semelhante.
Quando um algoritmo crescer e exigir vários módulos, arquivos de configuração ou diferentes implementações, poderá ser organizado em uma subpasta própria.

### Como reutilizar a comunicação entre hosts

Os programas em `hosts/` poderão fornecer funcionalidades comuns, como:

* Inicialização de um servidor TCP.
* Conexão de um cliente a outro host.
* Envio e recebimento de mensagens.
* Serialização de mensagens em JSON.
* Identificação de remetentes e destinatários.
* Tratamento de desconexões.
* Registro de eventos.

Os algoritmos deverão reutilizar essas funcionalidades sempre que possível, evitando duplicar código.

Por exemplo, uma mensagem poderá seguir o formato:

```json
{
  "type": "REQUEST",
  "sender": "h1",
  "receiver": "h2",
  "message_id": "h1-001",
  "payload": {
    "value": 10
  }
}
```

Os campos e tipos de mensagem deverão ser adaptados às necessidades de cada algoritmo.

É importante lembrar que TCP fornece um fluxo de bytes, não uma sequência de mensagens com limites automaticamente definidos pela aplicação. Portanto, a implementação deverá estabelecer um mecanismo de delimitação ou enquadramento das mensagens, como mensagens JSON terminadas por uma quebra de linha.

Também será necessário definir como cada conexão será estabelecida e encerrada.

### Como testar e validar os algoritmos

Cada experimento deverá ser testado inicialmente em uma topologia pequena. Depois, a quantidade de hosts e a complexidade da rede poderão ser aumentadas.

Durante os testes, verifique:

* Se todos os participantes esperados foram iniciados.
* Se os endereços IP estão corretos.
* Se as mensagens são enviadas e recebidas corretamente.
* Se o algoritmo termina nas condições previstas.
* Se mensagens duplicadas são tratadas adequadamente.
* Se mensagens atrasadas ou respostas ausentes são tratadas conforme o projeto.
* Se os recursos são liberados ao final do experimento.
* Se os resultados são consistentes com as propriedades esperadas do algoritmo.

Quando aplicável, registre o número de mensagens trocadas, o tempo de execução e o comportamento diante de falhas simuladas.

## Sequência de algoritmos

### Projeto 1 — Comunicação básica entre dois hosts

**Arquivo:** `01_basic_communication.py`

Uma aplicação cliente-servidor com sockets TCP. O servidor aguarda conexões e responderá às mensagens recebidas. O cliente estabelece uma conexão, envia uma mensagem e aguarda a resposta.

**Objetivos:**
* Compreender sockets TCP.
* Identificar hosts por seus endereços IP e portas.
* Executar processos independentes em hosts virtuais.
* Enviar e receber mensagens.
* Gerenciar conexões e encerramentos.

**Critério:** dois hosts conseguem trocar mensagens de maneira consistente?

### Projeto 2 — Comunicação entre múltiplos hosts

**Arquivo:** `02_multiple_hosts.py`

Expande a comunicação para três ou mais hosts. Um processo deverá enviar mensagens a vários participantes e coletar suas respostas.

**Objetivos:**
* Gerenciar múltiplos participantes.
* Identificar remetentes e destinatários.
* Controlar respostas pendentes.
* Trabalhar com várias conexões.

**Critério:** um host consegue enviar mensagens a todos os participantes definidos e receber suas respostas?

### Projeto 3 — Disseminação de mensagens

**Arquivo:** `03_broadcast.py`

Implementação de um broadcast centralizado, no qual um host envia uma mensagem a todos os participantes. E também uma implementação de flooding, no qual cada host encaminha mensagens novas aos vizinhos.
Cada mensagem deverá possuir um identificador único para evitar retransmissões duplicadas.

**Objetivos:**
* Estudar disseminação de informações.
* Identificar mensagens duplicadas.
* Controlar retransmissões.
* Comparar custos de comunicação.

**Critério:** todos os participantes esperados recebem a mensagem sem que o encaminhamento gere um ciclo infinito?

### Projeto 4 — Coleta de respostas

**Arquivo:** `04_gather.py`

Um host solicita informações aos demais participantes, coleta as respostas e finaliza quando todas as respostas esperadas forem recebidas ou quando um prazo for ultrapassado.

**Objetivos:**
* Implementar requisições e respostas.
* Controlar participantes pendentes.
* Utilizar temporizadores.
* Tratar respostas ausentes.

**Critério:** o processo solicitante consegue reunir as respostas recebidas e registrar os participantes que não responderam dentro do prazo?

### Projeto 5 — Eleição de líder

**Arquivo:** `05_leader_election.py`

Implementação de uma versão didática de eleição de líder baseada em identificadores únicos. Os participantes trocam informações e chegam a uma decisão comum.
Como evolução, uma implementação do algoritmo de Bully e uma eleição em anel.

**Objetivos:**
* Compreender coordenação distribuída.
* Trocar identificadores entre participantes.
* Anunciar o resultado da eleição.
* Investigar a reeleição após a saída do líder.

**Critério:** os participantes ativos identificam o líder de acordo com as regras definidas para o algoritmo?

### Projeto 6 — Relógios lógicos de Lamport

**Arquivo:** `06_lamport_clock.py`

Implementação de um relógio lógico local em cada processo. O contador é incrementado antes de eventos locais e envios de mensagens. Ao receber uma mensagem com timestamp `t`, um processo atualiza seu relógio segundo a regra: `C = max(C, t) + 1`

**Objetivos:**
* Estudar causalidade.
* Ordenar eventos logicamente.
* Comparar eventos locais e eventos de comunicação.
* Compreender a relação entre mensagens e relógios lógicos.

**Critério:** os registros dos participantes incluem timestamps coerentes com as regras do relógio de Lamport.

### Projeto 7 — Exclusão mútua distribuída

**Arquivo:** `07_mutual_exclusion.py`

Implementação de um mecanismo centralizado de controle de acesso a um recurso compartilhado. Desenvolvimento de uma versão distribuída baseada em mensagens de requisição e resposta, como o algoritmo de Ricart–Agrawala.

**Objetivos:**
* Controlar o acesso concorrente a recursos.
* Implementar requisições e permissões.
* Garantir exclusão mútua.
* Investigar o comportamento diante de falhas.

**Critério:** em condições compatíveis com as hipóteses do algoritmo, nenhum par de processos entra simultaneamente na seção crítica?

### Projeto 8 — Detecção de falhas por heartbeat

**Arquivo:** `08_heartbeat.py`

Implementação do envio periódico de mensagens de heartbeat. Cada processo monitora o tempo desde a última mensagem recebida e pode classificar participantes como suspeitos quando um limite for ultrapassado.

**Objetivos:**
* Utilizar temporizadores.
* Monitorar participantes.
* Detectar ausência de mensagens.
* Compreender as limitações da detecção de falhas.

**Critério:** o sistema identifica participantes que deixam de enviar heartbeats dentro do prazo configurado?
*(Obs.: a ausência de heartbeat deverá ser tratada como suspeita de falha, pois também pode decorrer de atrasos ou problemas de comunicação).*

### Projeto 9 — Média distribuída

**Arquivo:** `09_distributed_average.py`

Atribui um valor numérico a cada host e calcula a média global. Inicialmente, um coordenador coleta os valores, calcula a média e distribui o resultado. Depois, a implementação avança para agregar somas parciais e quantidades de participantes.

**Objetivos:**
* Agregar informações distribuídas.
* Representar resultados parciais em mensagens.
* Evitar contabilizações duplicadas.
* Comparar abordagens centralizadas e distribuídas.

**Critério:** o resultado corresponde à média dos valores dos participantes definidos para o experimento?

## Requisitos gerais para os experimentos

Todos os algoritmos deverão seguir, quando aplicável, estas diretrizes:

* Utilizar os recursos do Mininet para criar e executar a topologia.
* Executar cada participante como um processo independente.
* Utilizar sockets TCP ou UDP conforme os requisitos do experimento.
* Definir os tipos e formatos das mensagens trocadas.
* Manter o estado local necessário ao funcionamento do algoritmo.
* Registrar eventos relevantes para facilitar a depuração.
* Encerrar conexões, processos e topologias adequadamente.
* Documentar os procedimentos de execução e os resultados esperados.
* Evitar alterações no código-fonte original do Mininet quando elas não forem necessárias.
* Identificar explicitamente as hipóteses de funcionamento e as limitações de cada algoritmo.

A utilização de TCP ou UDP deverá ser uma decisão consciente. TCP facilita a comunicação confiável entre dois pontos enquanto a conexão permanece operacional, mas não garante que a aplicação remota tenha processado uma mensagem. UDP permite estudar a comunicação por datagramas, mas não fornece garantias de entrega, ordenação ou eliminação de duplicatas.

## Documentação dos experimentos

O arquivo `examples/distributed/README.md` deverá explicar como configurar o ambiente, executar os experimentos e interpretar seus resultados.

Para cada algoritmo, documentar:

* Nome e objetivo.
* Topologia utilizada.
* Quantidade de hosts.
* Papel de cada participante.
* Tipos de mensagens trocadas.
* Estado local mantido pelos processos.
* Comando de execução.
* Resultado esperado.
* Testes realizados.
* Limitações conhecidas.

O arquivo `README.md` da pasta raíz permanecerá como documento geral de planejamento. Os detalhes de execução de cada algoritmo deverão ficar em `examples/distributed/README.md` ou em arquivos adicionais, quando necessário.

## Referências

* [Repositório oficial do Mininet](https://github.com/mininet/mininet)
* [Tutorial oficial do Mininet](https://mininet.org/walkthrough/)
* [Documentação do Python](https://docs.python.org/3/)
* [Documentação de sockets em Python](https://docs.python.org/3/library/socket.html)
