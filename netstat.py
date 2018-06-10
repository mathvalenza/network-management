import sys

PROC_TCP = "/proc/net/tcp"
PROC_UDP = "/proc/net/udp"
PROC = "/proc/net/"

STATE = {
        '01':'ESTABELECIDA',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'FECHADA',
        '08':'ESPERANDO FECHAR',
        '09':'LAST_ACK',
        '0A':'ESCUTANDO',
        '0B':'FECHANDO'
        }

VALID_PARAMS = ['tcp', 'udp', '-e', '-a']

ESTABLISHED_PARAM = '-e'
ALL_PARAM = '-a'

def main():
	try:
		protocol, status_param = get_command_line_params()
	except Exception as e:
		print(e.args[0])
		sys.exit()
	# protocol = "udp"
	content = parse_file(protocol)

	print("----------------------- SHOWING " + protocol.upper() + " INFORMATIONS --------------------------")
	print("Origin\tDestiny")

	for line in content:
		display = ""

		host_origin, port_origin = get_host_and_port(line[1])
		display += host_origin + ":" + port_origin + "\t"

		host_destiny, port_destiny = get_host_and_port(line[2])
		display += host_destiny + ":" + port_destiny + "\t"

		connection_status = get_status(line[3])

		display += connection_status

		if(status_param == ALL_PARAM):
			print(display)
		elif(status_param == ESTABLISHED_PARAM and connection_status == "ESTABELECIDA"):
			print(display)


def get_host_and_port(string):
    host, port = string.split(':')
    return get_ip(host), hex2decimal(port)

def get_ip(string):
    ip = [(hex2decimal(string[6:8])), (hex2decimal(string[4:6])),
    	(hex2decimal(string[2:4])), (hex2decimal(string[0:2]))]
    return '.'.join(ip)

def get_status(string):
	return STATE[string]

def parse_file(protocol):
	file = open(PROC + protocol, 'r')

	content = file.readlines()

	content.pop(0)

	return format_content(content)

def format_content(content):
	formated_content = []

	for line in content:
		formated_content.append(line.split())

	return formated_content

def hex2decimal(string):
    return str(int(string,16))

def get_command_line_params():
	param_array = []

	for param in sys.argv[1:]:
		if(param in VALID_PARAMS or (int(param) > 0 and (int(param) < 9999)): #TODO: testar com regex
			param_array.append(param)
		else:
			raise Exception("Parâmetro inválido."
				+ "Os parâmetros devem estar entre as opções [tcp, udp] [-e, -a] [<NUMERO_DA_PORTA>]\n")

	return param_array

main()