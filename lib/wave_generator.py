def pand(s1, s2):
	return s1 and s2

def pnand(s1, s2):
	return not pand(s1, s2)

def por(s1, s2):
	return s1 or s2

def pnor(s1, s2):
	return not por(s1, s2)

def pxor(s1, s2):
	return s1 != s2

def pxnor(s1, s2):
	return not xor(s1, s2)

def pnot(s1):
	return not s1

inputs = []
outputs = []
port_data = []

def init(extracted_data, wave_in):
	outputs = extracted_data[0]
	inputs = extracted_data[1] 
	port_data = extracted_data[2]

	for output in outputs
		output_port = search_port_by_id(output);
		for t in range(len(wave_in)):
			signal = process_signal(t, output_port)
		


def search_port_by_id(port_id):
	for port in port_data:
		if port == port_id
			return port
	return False

def get_wave_signal_by_port_signal_id():
	return 1


def choose_port(type, signal_1, signal_2):
	if type == 'and':	
		return pand(signal_1, signal_2)
	elif type == 'nand':
		return pnand(signal_1, signal_2)


def search_port_by_output(output):
	for port in port_data:
		if port[3] == output:
			return port
	return False


def process_signal(t, port_id):
	current_port_data = search_port_by_id(port_id)

	if current_port_data[4] in inputs:
		return get_wave_signal_by_port_signal_id(current_port_data[4])
	else:
		signal_1 = process_signal(t, search_port_by_output(current_port_data[4]))
	
	if current_port_data[5] in inputs:
		return get_wave_signal_by_port_signal_id(current_port_data[5])
	else:	
		signal_2 = process_signal(t, search_port_by_output(current_port_data[5]))

	return choose_port(current_port_data[1], signal_1, signal_2)

'''
tipos:


 [[id do output], [input1, input2], [[id, tipo, atraso, saida, entrada1, entrada2], []]]

'''



'''
ler linha por linha definiçoes de porta com sinais de entrada, saida e atraso, salvar tudo em um array dentro de outro array contendo todas as portas


ex:

assign c AND #3(a,b)
assign d AND #4(e,f)

[[AND, 3, c, a, b.],[AND, 4, d, e, f]]
'''