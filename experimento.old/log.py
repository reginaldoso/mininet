def log_formatado(origem, id_conexao, mensagem):
    """
    Exibe o log no formato: [TIPO] ('IP', PORTA): Mensagem
    """
    print(f"[{origem}] {id_conexao}: {mensagem}", flush=True)