# network-management
Trabalho final da disciplina de Gerência de Redes, 2018/1

Simulação do comando netstat, com informações sobre o protocolo da camada de transporte, host e porta de origem, host e porta destino e status da conexão (no caso do TCP)

Execução: 

	netstat_local.py [tcp, udp] [-e, -a] <NUMERO_DA_PORTA>

		-e: established, conexão estabelecida
		-a: all, conexões de todos os status

	netstat_remoto.py [tcp, udp] <NUMERO_DA_PORTA_MINIMO> <NUMERO_DA_PORTA_MAXIMO>
		Para a versão remota, só são retornadas as informações com conexão estabelecida (para TCP)
		Caso não informado algum parâmetro, a saída retornará as informações do protocolo TCP, para todas as portas.

Dependências: python3.5.2+, easysnmp (pip install easysnmp)

Autor: Matheus Vinícius Valenza
