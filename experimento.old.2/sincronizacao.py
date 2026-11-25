import json
import socket
import threading
import time

from socketserver import ThreadingTCPServer, StreamRequestHandler


class RoundSynchronizer:

    def __init__(self, process_id, host, port, peers):

        self.process_id = process_id
        self.host = host
        self.port = port

        # Dicionário com os endereços dos demais processos.
        # Exemplo: {"P2": ("10.0.0.2", 5000)}
        self.peers = peers

        # Armazena mensagens separadas por rodada.
        self.mensagens = {}

        # Controla o acesso concorrente às mensagens.
        self.condition = threading.Condition()

        # Configura o servidor TCP de recebimento.
        synchronizer = self

        class RequestHandler(StreamRequestHandler):

            def handle(self):

                try:
                    linha = self.rfile.readline()

                    if not linha:
                        return

                    mensagem = json.loads(linha.decode("utf-8"))

                    synchronizer.receber_mensagem(mensagem)

                except (json.JSONDecodeError, UnicodeDecodeError):
                    print("Mensagem inválida recebida.")

        class Server(ThreadingTCPServer):

            allow_reuse_address = True
            daemon_threads = True

        self.server = Server(
            (self.host, self.port),
            RequestHandler
        )

        self.thread_servidor = threading.Thread(
            target=self.server.serve_forever,
            daemon=True
        )

    def iniciar(self):

        self.thread_servidor.start()

        print(
            f"[{self.process_id}] Servidor iniciado "
            f"em {self.host}:{self.port}"
        )

    def receber_mensagem(self, mensagem):

        origem = mensagem.get("origem")
        rodada = mensagem.get("rodada")
        valor = mensagem.get("valor")

        if origem not in self.peers:
            return

        if not isinstance(rodada, int) or rodada < 1:
            return

        with self.condition:

            if rodada not in self.mensagens:
                self.mensagens[rodada] = {}

            # Evita contabilizar mensagens duplicadas.
            if origem not in self.mensagens[rodada]:

                self.mensagens[rodada][origem] = valor

                print(
                    f"[{self.process_id}] Recebeu mensagem "
                    f"de {origem} na rodada {rodada}: {valor}"
                )

            self.condition.notify_all()

    def enviar_mensagem(self, destino, endereco, rodada, valor):

        mensagem = {
            "origem": self.process_id,
            "rodada": rodada,
            "valor": valor
        }

        dados = (
            json.dumps(mensagem) + "\n"
        ).encode("utf-8")

        try:

            with socket.create_connection(
                endereco,
                timeout=2
            ) as conexao:

                conexao.sendall(dados)

            return True

        except OSError:

            print(
                f"[{self.process_id}] Falha ao enviar "
                f"mensagem para {destino}"
            )

            return False

    def executar_rodada(self, rodada, valor, timeout=5):

        print(
            f"\n[{self.process_id}] "
            f"Iniciando rodada {rodada}"
        )

        # 1. Envia o valor para todos os outros processos.

        for destino, endereco in self.peers.items():

            self.enviar_mensagem(
                destino,
                endereco,
                rodada,
                valor
            )

        # 2. Aguarda as mensagens dos demais processos.

        prazo = time.monotonic() + timeout

        with self.condition:

            while True:

                recebidas = self.mensagens.get(
                    rodada, {}
                )

                faltantes = (
                    set(self.peers.keys())
                    - set(recebidas.keys())
                )

                if not faltantes:
                    break

                restante = prazo - time.monotonic()

                if restante <= 0:
                    break

                self.condition.wait(restante)

            # Copia as mensagens recebidas.
            recebidas = dict(
                self.mensagens.get(rodada, {})
            )

        faltantes = (
            set(self.peers.keys())
            - set(recebidas.keys())
        )

        print(
            f"[{self.process_id}] "
            f"Rodada {rodada} concluída."
        )

        if faltantes:

            print(
                f"[{self.process_id}] "
                f"Processos sem resposta: {faltantes}"
            )

        return recebidas, faltantes

    def encerrar(self):

        self.server.shutdown()
        self.server.server_close()
