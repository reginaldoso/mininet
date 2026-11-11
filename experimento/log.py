# Utilitário de formatação de logs

def log_formatado(origem, id_conexao, mensagem):
    """ Formata todas as saídas no padrão: [ORIGEM] ('IP', PORTA): Mensagem """
    print(f"[{origem}] {id_conexao}: {mensagem}", flush=True)