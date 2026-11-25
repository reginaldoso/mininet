import sys
import time

from sincronizacao import RoundSynchronizer
from consenso import executar_consenso


# ==========================================
# CONFIGURAÇÃO DOS PROCESSOS
# ==========================================

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


# ==========================================
# FUNÇÃO PRINCIPAL
# ==========================================

def main():

    if len(sys.argv) < 2:

        print("Uso: python3 processo.py <ID_PROCESSO>")

        sys.exit(1)

    process_id = sys.argv[1]

    if process_id not in PROCESSOS:

        print("Identificador de processo inválido.")

        sys.exit(1)

    # Obtém as informações do processo.
    configuracao = PROCESSOS[process_id]

    ip = configuracao["ip"]

    porta = configuracao["porta"]

    valor_inicial = configuracao["valor"]

    # Configura os demais processos.
    peers = {}

    for pid, dados in PROCESSOS.items():

        if pid != process_id:

            peers[pid] = (
                dados["ip"],
                dados["porta"]
            )

    print("\n===================================")
    print(f" INICIANDO PROCESSO {process_id}")
    print("===================================")

    print(f"IP: {ip}")
    print(f"Porta: {porta}")
    print(f"Valor inicial: {valor_inicial}")

    print(f"Processos conhecidos: {list(peers.keys())}")

    # ==========================================
    # INICIALIZA O SINCRONIZADOR
    # ==========================================

    sincronizador = RoundSynchronizer(
        process_id=process_id,
        host=ip,
        port=porta,
        peers=peers
    )

    sincronizador.iniciar()

    # Pequeno intervalo para inicialização dos servidores.
    time.sleep(1)

    try:

        # ==========================================
        # EXECUTA O ALGORITMO DE CONSENSO
        # ==========================================

        resultado = executar_consenso(
            sincronizador=sincronizador,
            valor_inicial=valor_inicial,
            max_rodadas=10
        )

        print("\n===================================")
        print(f" RESULTADO FINAL: {process_id}")
        print("===================================")

        print(f"Valor decidido: {resultado}")

    except RuntimeError as erro:

        print(f"\n[{process_id}] ERRO: {erro}")

    finally:

        sincronizador.encerrar()


# ==========================================
# PONTO DE ENTRADA
# ==========================================

if __name__ == "__main__":

    main()
