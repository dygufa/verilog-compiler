import re

def init(file_object):
	return check_syntax(file_object)


def check_syntax(file_object):
	file_lines = file_object.readlines();

	is_comment = False
	module_defined = False
	parameters = []
	extracted_data = {}
	k = 0
	error = False

	for line in file_lines:
		k += 1
		# Ignora todos os comentários
		if (line[:2] == '//' or line[:2] == '/*' or line[:2] == '*/' or is_comment or line.replace(' ', '') == '\n'):
			continue
		if (line[:2] == '/*'):
			is_comment = True
		if (line[:2] == '*/'):
			is_comment = False

		if (module_defined):
			if sanitize_line(line) == 'endmodule':
				break

			res_xput = is_xput(line)
			if res_xput['status']:
				if res_xput['type'] == 'input':
					if not 'inputs' in extracted_data:
						extracted_data['inputs'] = []
					extracted_data['inputs'] = extracted_data['inputs'] + res_xput['args']
				elif res_xput['type'] == 'output':
					if not 'outputs' in extracted_data:
						extracted_data['outputs'] = []
					extracted_data['outputs'] = extracted_data['outputs'] + res_xput['args']
			else:
				res_port = is_port(line) 
				if res_port['status']:
					if not 'ports' in extracted_data:
						extracted_data['ports'] = []
					current_port_data = [{'id': res_port['name'], 'type': res_port['type'], 'delay': res_port['delay'], 'output': res_port['output'], 'inputs': res_port['inputs']}]
					extracted_data['ports'] = extracted_data['ports'] + current_port_data
				else:
					res_datatype = is_datatype(line)
					if res_datatype['status']:
						if res_datatype['type'] == 'wire':
							if not 'wires' in extracted_data:
								extracted_data['wires'] = []
							extracted_data['wires'] = extracted_data['wires'] + res_datatype['args']
					else:
						error = True
						print('Erro na linha ' + str(k) + ', estrutura não reconhecida.')
						break

					
		else:
			if (is_module(line)):
				module_defined = True
			else:
				error = True
				print('Erro, o código verilog não foi iniciado com module')
				break

	if error:
		return False

	return extracted_data


def sanitize_line(line):
	return line.replace("\n", '')

def is_module(line):
	line = sanitize_line(line)
	match = re.match("^module\s(\w+)(\s?)\(((\s?)((\w+)\,)?)+(\w+)\)\;$", line)
	if match:
		match = re.match("^module\s(?P<module_name>\w+)(\s?)\((?P<module_args>.*)\)\;$", line)
		matches = match.groupdict() 
		module_args = matches['module_args'].replace(' ', '')
		params = module_args.split(',')
		return {'status': True, 'args': params}
	else:
		return {'status': False}


def is_xput(line):
	line = sanitize_line(line)
	match = re.match("^(input|output)\s((\s?)((\w+)\,)?)+(\w+)\;$", line)
	if match:
		match = re.match("^(?P<xput_type>input|output)\s(?P<xput_args>.*)(\s?)\;$", line)
		matches = match.groupdict()
		module_args = matches['xput_args'].replace(' ', '')
		params = module_args.split(',')
		return {'status': True, 'type': matches['xput_type'] , 'args': params}
	else: 
		return {'status': False}

def is_datatype(line):
	line = sanitize_line(line)
	match = re.match("^(wire)\s((\s?)((\w+)\,)?)+(\w+)\;$", line)
	if match:
		match = re.match("^(?P<datatype_type>wire|integer|reg)\s(?P<datatype_args>.*)(\s?)\;$", line)
		matches = match.groupdict()
		datatype_args = matches['datatype_args'].replace(' ', '')
		params = datatype_args.split(',')
		return {'status': True, 'type': matches['datatype_type'] , 'args': params}
	else: 
		return {'status': False}


def is_port(line):
	line = sanitize_line(line)
	match = re.match("^(and|or|buf|not|xor)\s(\#([1-9]+)\s)?(\w+)(\s?)\(((\s?)((\w+)\,)?)+(\w+)\)\;$", line)
	if match:
		match = re.match("^(?P<xport_type>and|or|buf|not|xor)\s(?P<xport_delay>\#([1-9]+)(\s))?(?P<xport_name>\w+)\((?P<xport_args>.*)\)(\s?)\;$", line)
		matches = match.groupdict()
		module_args = matches['xport_args'].replace(' ', '')
		params = module_args.split(',')
		output = params[0]
		inputs = params[1:]
		if matches['xport_delay'] == None:
			delay = 0
		else: 
			delay = int(matches['xport_delay'].replace('#', ''))
		return {'status': True, 'type': matches['xport_type'] , 'delay': delay, 'output': output, 'inputs': inputs, 'name': matches['xport_name']}
	else: 
		return {'status': False}