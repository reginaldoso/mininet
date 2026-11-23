def executar_consenso(sincronizador, valor_inicial, max_rodadas=10):

    """
    Algoritmo fictício de consenso baseado no menor valor.

    Parâmetros:
        sincronizador: objeto responsável pela sincronização.
        valor_inicial: proposta inicial do processo.
        max_rodadas: número máximo de rodadas.

    Retorno:
        Valor decidido pelo processo.
    """

    valor_atual = valor_inicial

    rodadas_estaveis = 0

    for rodada in range(1, max_rodadas + 1):

        print("\n===================================")
        print(f" INICIANDO RODADA {rodada}")
        print("===================================")

        # 1. Executa a rodada e recebe as mensagens.
        mensagens, faltantes = sincronizador.executar_rodada(
            rodada=rodada,
            valor=valor_atual,
            timeout=5
        )

        # 2. Verifica se todos os processos responderam.
        if faltantes:

            print(
                f"[{sincronizador.process_id}] "
                "Não foi possível concluir a rodada."
            )

            raise RuntimeError(
                f"Mensagens ausentes na rodada {rodada}: {faltantes}"
            )

        # 3. Reúne o valor local e os valores recebidos.
        valores = list(mensagens.values())

        valores.append(valor_atual)

        print(
            f"[{sincronizador.process_id}] "
            f"Valores considerados: {valores}"
        )

        # 4. Seleciona o menor valor.
        novo_valor = min(valores)

        print(
            f"[{sincronizador.process_id}] "
            f"Valor anterior: {valor_atual}"
        )

        print(
            f"[{sincronizador.process_id}] "
            f"Novo valor: {novo_valor}"
        )

        # 5. Verifica se o valor permaneceu estável.
        if novo_valor == valor_atual:

            rodadas_estaveis += 1

        else:

            rodadas_estaveis = 0

        # Atualiza o valor local.
        valor_atual = novo_valor

        # 6. Verifica a condição de decisão.
        if rodadas_estaveis >= 2:

            print("\n===================================")
            print(f"[{sincronizador.process_id}] CONSENSO ALCANÇADO!")
            print(f"Valor decidido: {valor_atual}")
            print(f"Rodadas executadas: {rodada}")
            print("===================================")

            return valor_atual

    raise RuntimeError(
        f"[{sincronizador.process_id}] "
        "Consenso não alcançado dentro do limite de rodadas."
    )
