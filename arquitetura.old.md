# Arquitera do projeto



## Visão Geral

mininet/experimento
│
├── sincronizacao.py
│
├── consenso.py
│
├── processo.py
│
└── topologia.py

## Responsabilidades

topologia.py: criação da rede no Mininet.

processo.py: inicialização e execução de cada processo.

sincronizacao.py: comunicação entre processos e controle das rodadas

consenso.py: implementação do algoritmo de consenso.


## Modelo do sistema distribuído

Vamos considerar um sistema composto por quatro processos:
P={P1,P2,P3,P4}

Cada processo será executado em um host diferente do Mininet.

A configuração será:

| Processo | Host Mininet | Endereço IP | Porta | Valor inicial |
| :--- | :--- | :--- | :--- | :--- |
| P1 | h1 | 10.0.0.1 | 5000 | 40 |
| P2 | h2 | 10.0.0.2 | 5000 | 20 |
| P3 | h3 | 10.0.0.3 | 5000 | 30 |
| P4 | h4 | 10.0.0.4 | 5000 | 10 |



Cada processo possui:

Um identificador único.

Um endereço IP.

Uma porta TCP para recebimento de mensagens.

Um valor inicial proposto.

Uma instância própria do mecanismo de sincronização.

Uma instância da lógica de consenso.

A comunicação acontece diretamente entre os processos.

Por exemplo:

```text
          REDE MININET

+------------------------------+

|                              |
|       Switch OpenFlow        |
|                              |
+------------------------------+

   |       |       |       |
   |       |       |       |
  h1      h2      h3      h4

   |       |       |       |
  P1      P2      P3      P4

   |       |       |       |
  40      20      30      10
```

## Funcionamento do módulo sincronizacao.py

Esse é o componente central da nossa arquitetura.

Sua responsabilidade é implementar a comunicação entre os processos e controlar a sincronização das rodadas.

O módulo utiliza três mecanismos principais:

Sockets TCP: permitem a comunicação entre os processos.

Threads: permitem receber mensagens independentemente da execução do algoritmo.

Condition Variables: permitem que o processo aguarde mensagens sem bloquear a thread responsável pelo recebimento.

### Servidor de recebimento

Quando um processo é inicializado, ele cria um servidor TCP.

Por exemplo, P1 abre a porta 5000 no endereço 10.0.0.1.

Os demais processos podem estabelecer conexões com esse servidor para enviar mensagens.

Cada processo possui seu próprio servidor.

Isso significa que P1, P2, P3 e P4 conseguem enviar e receber mensagens simultaneamente.

### Identificação das mensagens

Todas as mensagens possuem três informações:
mensagem = {
    "origem": "P1",
    "rodada": 1,
    "valor": 40
}

Essas informações são importantes por três motivos:

origem: identifica o processo que enviou a mensagem.

rodada: identifica a rodada à qual a mensagem pertence.

valor: contém a proposta ou o valor atualizado pelo processo.

A identificação da rodada é especialmente importante.

Imagine que P1 esteja processando a rodada 2, mas receba uma mensagem atrasada da rodada 1.

Como a mensagem possui o identificador da rodada, o sistema consegue armazená-la separadamente.

### Armazenamento das mensagens


Cada processo mantém um dicionário local:

python
self.mensagens = {}


As mensagens são organizadas por rodada.

Por exemplo, depois de receber as mensagens da primeira rodada, P1 poderá ter:

python
mensagens = {

    1: {
        "P2": 20,
        "P3": 30,
        "P4": 10
    }

}


Na segunda rodada, o dicionário poderá ficar:

python
mensagens = {

    1: {
        "P2": 20,
        "P3": 30,
        "P4": 10
    },

    2: {
        "P2": 10,
        "P3": 10,
        "P4": 10
    }

}

Observe que esse armazenamento é local.

P1 mantém suas próprias mensagens recebidas. P2 mantém outro dicionário independente, e assim sucessivamente.


### Controle da sincronização


A função mais importante desse módulo é:

python
executar_rodada()


Ela é responsável por coordenar a execução local de cada rodada.

Seu funcionamento pode ser dividido em quatro etapas:

Etapa 1 — Envio

O processo envia seu valor atual para todos os demais processos.

Etapa 2 — Recebimento

Os processos recebem as mensagens por meio das threads de atendimento TCP.

Etapa 3 — Espera

O processo verifica se recebeu mensagens de todos os seus vizinhos esperados.

A condição de avanço é:

∣Mir∣=N−1

Onde:

Mir: conjunto de mensagens recebidas pelo processo i na rodada r.
N: quantidade total de processos.

No nosso exemplo:

∣Mir∣=4−1=3

Portanto, cada processo precisa receber três mensagens.

Etapa 4 — Avanço

Quando todas as mensagens esperadas são recebidas, a função retorna os valores para o algoritmo de consenso.

O processo pode então executar a próxima etapa.

Caso o timeout seja atingido sem que todas as mensagens cheguem, a implementação atual informa os processos ausentes.

Na versão atual, o algoritmo interrompe a execução nesse caso.


## Funcionamento do módulo processo.py


O arquivo processo.py representa a inicialização de cada processo distribuído.

Ele é responsável por:

Identificar qual processo será executado.
Obter seu endereço IP e valor inicial.
Identificar os demais processos.
Criar o sincronizador.
Iniciar o servidor TCP.
Executar o algoritmo de consenso.

Um aspecto importante é que todos os processos executam o mesmo arquivo Python.

O que diferencia P1 de P2, por exemplo, é o argumento recebido na inicialização.

Exemplo:

bash
python3 processo.py P1


Ou:

bash
python3 processo.py P2


Cada execução cria uma instância independente.

Como os processos conhecem uns aos outros?

Atualmente, utilizamos uma configuração estática:

python
PROCESSOS = {

    "P1": {
        "ip": "10.0.0.1",
        "porta": 5000,
        "valor": 40
    },

    "P2": {
        "ip": "10.0.0.2",
        "porta": 5000,
        "valor": 20
    },

    "P3": {
        "ip": "10.0.0.3",
        "porta": 5000,
        "valor": 30
    },

    "P4": {
        "ip": "10.0.0.4",
        "porta": 5000,
        "valor": 10
    }

}


Cada processo utiliza essa configuração para conhecer os endereços dos demais participantes.

Essa abordagem é suficiente para nosso primeiro experimento.

Mais adiante, podemos implementar descoberta dinâmica de processos, caso seja necessário.


## Funcionamento do módulo consenso.py

Esse módulo contém exclusivamente a lógica do algoritmo de consenso.

Para testar a infraestrutura, escolhemos um algoritmo fictício baseado na seleção do menor valor.

Cada processo começa com uma proposta inicial.

Em cada rodada, recebe as propostas dos demais processos e calcula:

vir+1=min⁡(vir,{vjr∣j≠i})

Onde:

vir: valor atual do processo i.
vjr: valor recebido do processo j.
vir+1: novo valor do processo i.

Como todos os processos estão diretamente conectados, todos recebem os valores dos demais.

Depois da primeira rodada, todos passam a possuir o menor valor inicialmente proposto.

No nosso exemplo:

min⁡(40,20,30,10)=10

Assim:

P1=P2=P3=P4=10

O algoritmo fictício ainda utiliza uma condição de estabilidade: o valor precisa permanecer inalterado por duas rodadas consecutivas antes de ser considerado decidido.

Importante: essa regra serve para demonstrar a execução e testar a sincronização. Ela não constitui, isoladamente, uma garantia formal de consenso distribuído.

## Passo a passo para executar um experimento

Agora vamos executar um teste com quatro processos no Mininet.

O objetivo é observar:

A inicialização dos processos.
A comunicação entre os participantes.
O recebimento das mensagens.
A sincronização das rodadas.
A convergência dos valores.
A decisão final.

### Preparação do ambiente

Primeiro, precisamos ter o Mininet instalado e verificar se o python está disponível.

Em um terminal Linux, execute:

bash
sudo mn --version
python3 --version


A estrutura do projeto deverá estar organizada como mostrado na sessão Visão Geral.

Os quatro arquivos devem estar no mesmo diretório.

### Iniciar a topologia

No terminal Linux, entre no diretório do projeto:
bash

cd mininet/experimento

Execute:
bash

sudo python3 topologia.py

O Mininet deverá criar os quatro hosts.

Você verá o terminal de comandos:

ext
mininet>

Antes de iniciar os processos, teste a conectividade:
bash

mininet> pingall

O resultado esperado é que todos os hosts consigam se comunicar.

Por exemplo:
text

*** Ping: testing ping reachability
h1 -> h2 h3 h4
h2 -> h1 h3 h4
h3 -> h1 h2 h4
h4 -> h1 h2 h3

*** Results: 0% dropped

Se houver perda de pacotes, precisamos resolver o problema de conectividade antes de executar o algoritmo.

### Iniciar os quatro processos distribuídos


Agora precisa executar cada processo em um host diferente.

No terminal do Mininet, execute:


bash

mininet> h1 python3 processo.py P1 > /tmp/P1.log 2>&1 &

mininet> h2 python3 processo.py P2 > /tmp/P2.log 2>&1 &

mininet> h3 python3 processo.py P3 > /tmp/P3.log 2>&1 &

mininet> h4 python3 processo.py P4 > /tmp/P4.log 2>&1 &

Cada comando inicia um processo independente em segundo plano.

Os arquivos de log permitem acompanhar individualmente a execução de cada participante.

Importante: como nosso processo.py possui uma espera inicial de apenas um segundo, inicie os quatro processos rapidamente. Essa espera é uma simplificação para o primeiro teste, não uma barreira de inicialização garantida. Em uma versão mais robusta, devemos separar a inicialização dos servidores do início das rodadas, para garantir que todos estejam prontos antes da primeira transmissão.

### Acompanhar a execução

Podemos consultar os logs diretamente pelo terminal do Mininet.

Para P1:
bash

mininet> h1 cat /tmp/P1.log

Para P2:
bash

mininet> h2 cat /tmp/P2.log

Para P3:
bash

mininet> h3 cat /tmp/P3.log

Para P4:
bash

mininet> h4 cat /tmp/P4.log

Também podemos acompanhar a execução continuamente:
bash

mininet> h1 tail -f /tmp/P1.log

Isso permite observar as mensagens à medida que são registradas.

Observação: o conteúdo documenta a implementação atual, incluindo suas simplificações e limitações.




