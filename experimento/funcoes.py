## escolhe valor mínimo dentre conjunto de valores

def minimo(valores):
    """
    Retorna o menor valor de um conjunto de valores.

    Parâmetro:
        valores: conjunto (set) de valores numéricos.

    Retorno:
        O menor elemento do conjunto.

    Exceção:
        ValueError: caso o conjunto esteja vazio.
    """

    if not valores:
        raise ValueError("Erro: o conjunto de valores está vazio.")

    menor = None

    for valor in valores:
        if menor is None or valor < menor:
            menor = valor

    return menor


## representa a execução da rodada

def executar_rodada(rodada_atual, mensagens_recebidas):
    print(f"Executando rodada {rodada_atual}")

    # Processa as mensagens recebidas
    # Executa as operações do algoritmo

    return rodada_atual + 1

