## Para personalizar os valores para os parâmetros customizados do experimento

Edite o arquivo config.yaml.
Para ler o arquivo, basta usar a biblioteca nativa PyYAML (pip install pyyaml ou sudo apt install python3-yaml).



## Para executar a topologia 

Usando integralmente as configurações do config.yaml (Sem passar nada):

sudo python3 custom_mesh_topo.py

Sobrescrevendo apenas um parâmetro específico pela linha de comando:(O script usará os valores do YAML para o resto, mas usará 2 hosts)

sudo python3 custom_mesh_topo.py -n 2

Apontando para outro arquivo de configuração YAML:

sudo python3 custom_mesh_topo.py --config outro_cenario.yaml
