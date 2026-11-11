# aqui centralizamos apenas configurações globais (faixas de IP, portas padrão, caminhos de log)


# Faixa de IPs para distribuição automática (ex: 10.0.0.1, 10.0.0.2...)
REDE_BASE_IP = "10.0.0."
IP_INICIAL_HOST = 1

# Porta inicial para atribuição sequencial
PORTA_INICIAL = 5000

# Diretório padrão para salvar os logs de cada nó
DIR_LOGS = "./logs"