# network-management
Trabalho final da disciplina de Gerência de Redes, 2018/1

Simulação do comando netstat, com informações sobre o protocolo da camada de transporte, host e porta de origem, host e porta destino e status da conexão (no caso do TCP)

Execução: netstat.py [tcp, udp] [-e, -a] <NUMERO_DA_PORTA>

-e: established, conexão estabelecida
-a: all, conexões de todos os status

Caso não informado algum parâmetro, a saída retornará as informações sem filtros.

Dependências: python3.5.2+

Autor: Matheus Vinícius Valenza
