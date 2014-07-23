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

def init(extracted_data, wave_in_data):
	global inputs
	global outputs
	global port_data
	global wave_in

	outputs = extracted_data['outputs']
	inputs = extracted_data['inputs']
	port_data = extracted_data['ports']
	wave_in = wave_in_data

	timeline_length = len(wave_in[0][1])
	final_signal = [0]*timeline_length

	for output in outputs:
		output_port = search_port_by_output(output)
		for t in range(timeline_length):
			final_signal[t] = process_signal(t, output_port['id'])
		
	return final_signal

def search_port_by_id(port_id):
	for port in port_data:
		if port['id'] == port_id:			
			return port

	return False

def get_wave_signal_by_port_signal_id(t, input_id):
	for wavein_el in wave_in:
		if wavein_el[0] == input_id:
			return wavein_el[1][t]

def choose_port(type, signal_1, signal_2):
	return globals()['p' + type](signal_1, signal_2)

def search_port_by_output(output):
	for port in port_data:
		if port['output'] == output:
			return port
	return False


def process_signal(t, port_id):
	current_port_data = search_port_by_id(port_id)
	input_1 = current_port_data['inputs'][0]
	
	if input_1 in inputs:
		signal_1 = get_wave_signal_by_port_signal_id(t, input_1)
	else:
		searched_port_1 = search_port_by_output(input_1)
		signal_1 = process_signal(t, searched_port_1['id'])
	
	input_2 = current_port_data['inputs'][1]

	if input_2 in inputs:
		signal_2 = get_wave_signal_by_port_signal_id(t, input_2)
	else:	
		searched_port_2 = search_port_by_output(input_2)
		signal_2 = process_signal(t, searched_port_2['id'])

	return choose_port(current_port_data['type'], signal_1, signal_2)

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