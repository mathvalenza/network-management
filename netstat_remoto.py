#!/usr/bin/python
# -*- coding: utf-8 -*-

from easysnmp import Session
import sys

HOST_NAME = '192.168.0.16' # demo.snmplabs.com
MAX_PORT_NUMBER = 65535 

STATE = { 'closed': '1',
          'listen': '2',
          'synSent': '3',
          'synReceived': '4',
          'established': '5',
          'finWait1': '6',
          'finWait2': '7',
          'closeWait': '8',
          'lastAck': '9',
          'closing': '10',
          'timeWait': '11',
          'deleteTCB': '12',
        }

VALID_PARAMS = ['tcp', 'udp']

def main():
	try:
		params = get_command_line_params()
	except Exception as e:
		print(e.args[0])
		sys.exit()

	protocol = 'tcp'
	min_port = 0
	max_port = MAX_PORT_NUMBER

	if (len(params) >= 1):
		protocol = params[0]
	if (len(params) >= 2):
		min_port = int(params[1])
	if (len(params) >= 3):
		max_port = int(params[2])

	session = connect()
	get_system_desc(session)

	if (protocol == 'tcp'):
		tcp_info = get_tcp(session, min_port, max_port)
	elif (protocol == 'udp'):
		udp_info = get_udp(session, min_port, max_port)

def connect():
	# Create an SNMP session to be used for all our requests
	session = Session(hostname=HOST_NAME, community='public', version=2)

	# You may retrieve an individual OID using an SNMP GET
	location = session.get('sysLocation.0')

	return session

def get_system_desc(session):
	print ('---------------------- ABOUT THE SYSTEM -----------------------')
	system_items = session.walk('system')

	for item in system_items:
	    print ('{oid}.{oid_index} {snmp_type} = {value}'.format(
	        oid=item.oid,
	        oid_index=item.oid_index,
	        snmp_type=item.snmp_type,
	        value=item.value
	    ))

	print ('---------------------------------------------------------------')

def get_tcp(session, min_port, max_port):
	# Perform an SNMP walk
	tcp_items = session.walk('tcp')

	established_oids_indexes = []
	items = {}
	initial_item = { 
					"status": "established",
		            "local_addr": "",
		            "local_port": "",
		            "remote_addr": "",
		            "remote_port": "",
					}

	for tcp_item in tcp_items:
		if (tcp_item.oid == "tcpConnState" and tcp_item.value == STATE['established']):

			items[tcp_item.oid_index] = initial_item
	
		if (tcp_item.oid_index in items.keys()):
			if (tcp_item.oid == 'tcpConnLocalAddress'):
				items[tcp_item.oid_index]['local_addr'] = tcp_item.value
			elif (tcp_item.oid == 'tcpConnLocalPort'):
				items[tcp_item.oid_index]['local_port'] = tcp_item.value
			elif (tcp_item.oid == 'tcpConnRemAddress'):
				items[tcp_item.oid_index]['remote_addr'] = tcp_item.value
			elif (tcp_item.oid == 'tcpConnRemPort'):
				items[tcp_item.oid_index]['remote_port'] = tcp_item.value

	print ('-------------------------  TCP INFO  --------------------------')
	print "STATUS".ljust(15),"ENDEREÇO LOCAL".ljust(15),"PORTA LOCAL".ljust(15),"ENDEREÇO REMOTO".ljust(15), "PORTA REMOTA".ljust(15)
	for key in items:
		if (int(items[key]["local_port"]) >= min_port and int(items[key]["local_port"]) <= max_port):
			print ('{status}\t{local_addr}\t{local_port}\t{remote_addr}\t{remote_port}'.format(
		        status = items[key]["status"].ljust(15),
		        local_addr = items[key]["local_addr"].ljust(15),
		        local_port = items[key]["local_port"].ljust(15),
		        remote_addr = items[key]["remote_addr"].ljust(15),
		        remote_port = items[key]["remote_port"].ljust(15),
		    ))
	print ('---------------------------------------------------------------')

def get_udp(session, min_port, max_port):
	# Perform an SNMP walk
	udp_items = session.walk('udp')

	items = {}

	initial_item = { 
		            "local_addr": "",
		            "local_port": ""
					}

	for udp_item in udp_items:
		if (udp_item.oid == 'udpLocalAddress' and udp_item.value != '0.0.0.0'):
			items[udp_item.oid_index] = initial_item

		if (udp_item.oid_index in items.keys()):
			if (udp_item.oid == 'udpLocalAddress'):
				items[udp_item.oid_index]['local_addr'] = udp_item.value
			elif (udp_item.oid == 'udpLocalPort'):
				items[udp_item.oid_index]['local_port'] = udp_item.value

		if (udp_item.oid == 'udpInErrors'):
			udpInErrors = udp_item.value
		elif (udp_item.oid == 'udpOutDatagrams'):
			udpOutDatagrams = udp_item.value


	print ('-------------------------  UDP INFO  --------------------------')
	print "ENDEREÇO LOCAL".ljust(15),"PORTA LOCAL"

	for key in items:
		if (int(items[key]["local_port"]) >= min_port and int(items[key]["local_port"]) <= max_port):
			print items[key]["local_addr"].ljust(15), items[key]["local_port"].ljust(15)
	print ('---------------------------------------------------------------')

	print "udpInErrors: ", udpInErrors
	print "udpOutDatagrams: ", udpOutDatagrams

def get_command_line_params():
	param_array = []

	for param in sys.argv[1:]:
		if(param in VALID_PARAMS):
			param_array.append(param)
		elif(int(param) > 0 and int(param) < MAX_PORT_NUMBER):
			param_array.append(param)
		else:
			raise Exception("Parâmetro inválido."
				+ "Os parâmetros devem estar entre as opções [tcp, udp] <NUMERO_DA_PORTA_MINIMO> <NUMERO_DA_PORTA_MAXIMO> \n")

	return param_array

main()