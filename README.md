# Projetos de Algoritmos Distribuídos com Mininet

## Objetivo

Desenvolver, testar e manter algoritmos distribuídos utilizando o Mininet como ambiente de experimentação.
Este repositório foi usado durante a disciplina Projeto Final de Curso 2, em 2026.2.

## Estrutura do repositório

O repositório contém pastas e arquivos padrão do mininet e a pasta personalizada *experimento* que guarda os arquivos gerais usados no experimento.
A pasta *experimento*, por sua vez, está organizada da seguinte forma:


* `main.py`: Orquestrador principal. Inicializa a rede Mininet com a topologia escolhida, mapeia a adjacência dos nós, gera o arquivo `rede.json`, lança os processos `nodo.py` em cada host virtual e gerencia o encerramento limpo da simulação.
* `nodo.py`: Aplicação autônoma executada internamente por cada host virtual. Lê o `rede.json`, gerencia conexões de socket (UDP/TCP) e executa a lógica do algoritmo distribuído (ex.: inundação, deduplicação de mensagens).
* `log.py`: Módulo utilitário compartilhado que padroniza o formato de impressão das mensagens no terminal e nos arquivos de log.
* `topologias/`: Diretório contendo as classes de topologia virtual do Mininet (`topo_anel.py`, `topo_estrela.py`, etc.).
* `rede.json`: Arquivo dinâmico gerado durante o boot do experimento contendo a tabela de adjacência (IPs e vizinhos de cada nó).
* `logs/`: Diretório gerado automaticamente para armazenar as saídas (`stdout` e `stderr`) individuais de cada nó (`h1.log`, `h2.log`, etc.).

**Observação:** os diretórios originais do Mininet devem ser preservados.
---

### Acessar o diretório dos experimentos

Certifique-se de estar no diretório raiz do projeto no terminal antes de executar os comandos:

```bash
cd ~/mininet

### Como executar os experimentos

Abra o terminal no diretório raiz do repositório:
   ```bash
   cd ~/mininet

Realize uma limpeza preventiva de processos antigos do Mininet:

sudo mn -c

Execute o orquestrador principal indicando o arquivo da topologia (-t) e a quantidade de nós (-n):

sudo python3 experimento/main.py -t topo_anel.py -n 6

Verifique no terminal a confirmação do carregamento da topologia, criação do rede.json e inicialização de cada nó.

Interaja com a rede utilizando a CLI do Mininet gerada ou digite exit para encerrar a simulação e fechar os processos.

### Como atualizar um algoritmo existente

Abra o arquivo experimento/nodo.py no seu editor de código.

Localize a função responsável pela escuta e repasse de mensagens (escutar_servidor).

Modifique as regras de negócio desejadas (ex.: regras de deduplicação, formato da mensagem ou filtros).

Salve o arquivo nodo.py.

Reexecute o experimento no terminal com o comando sudo python3 experimento/main.py -t topo_anel.py -n 6. As alterações serão aplicadas automaticamente a todos os hosts da rede.

### Como adicionar um novo algoritmo

Crie um novo arquivo Python no diretório experimento/ (ex.: experimento/nodo_consenso.py).

Implemente a estrutura básica de carregamento do rede.json para descoberta de adjacências e inicialize o servidor de socket na PORTA_PADRAO = 5000.

Adicione a nova lógica distribuída no script criado.

Em experimento/main.py, atualize a linha:
caminho_nodo = os.path.join(script_dir, "nodo_consenso.py")

Salve os arquivos e inicie o experimento via terminal.

## Como reutilizar a comunicação entre hosts

Importe o arquivo rede.json no início da execução do seu nó para extrair os dados de adjacência dinamicamente:

with open("rede.json", "r") as f:
    MAPA_REDE = json.load(f)

Instancie o socket ligado ao IP do próprio host e à porta padrão fixada:

sock.bind((MEU_IP, 5000))

Recupere a lista de vizinhos cadastrados em MAPA_REDE[NOME_HOST]["vizinhos"] e envie mensagens diretamente para a tupla (ip_vizinho, 5000).

Importe e utilize a função log_formatado do arquivo log.py em todas as emissões de logs para manter o padrão de rastreamento do sistema.

### Como testar e validar os algoritmos

Execute a simulação da rede via terminal principal (sudo python3 experimento/main.py -t topo_anel.py -n 4).

Abra um segundo terminal e acesse a pasta onde os logs individuais são gravados:

cd ~/mininet/experimento/logs

Monitore as mensagens trafegadas em tempo real em um host específico:
Bash

tail -f h1.log

Na CLI interativa do Mininet (mininet>), realize pings de teste ou execute comandos manuais diretamente nos hosts virtuais se necessário (ex.: h1 ping -c 2 h2).

Digite exit na CLI do Mininet para encerrar a simulação e revise todos os arquivos de log (h1.log, h2.log, etc.) para garantir que as mensagens percorreram a rede sem laços infinitos ou perdas inesperadas.

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
