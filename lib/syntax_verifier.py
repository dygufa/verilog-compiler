import re

def init(file_object):
	check_syntax(file_object)


def check_syntax(file_object):
	file_lines = file_object.readlines();

	is_comment = False
	module_defined = False
	parameters = []
	extracted_data = {};

	for line in file_lines:
		# Ignora todos os comentários
		if (line[:1] == '//' or line[:1] == '/*' or line[:1] == '*/' or is_comment):
			continue
		if (line[:1] == '/*'):
			is_comment = True
		if (line[:1] == '*/'):
			is_comment = False

		if (module_defined):
			res_xput = is_xput(line)
			if (res_xput['status']):
				print('e exput')
			else:
				res_port = is_port(line) 
				if (res_port['status']):
					print('e port')
		else:
			if (is_module(line)):
				module_defined = True
			else:
				print('Erro, o código verilog não foi iniciado com module')
				break


def sanitize_line(line):
	return line.replace("\n", '')

def is_module(line):
	line = sanitize_line(line)
	match = re.match("^module\s(\w+)(\s?)\(((\s?)((\w+)\,)?)+(\w+)\)$", line)
	if match:
		match = re.match("^module\s(?P<module_name>\w+)(\s?)\((?P<module_args>.*)\)$", line)
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
	match = re.match("^(wire|integer|reg)\s((\s?)((?P<datatype_params>\w+)\,)?)+(?P<datatype_last_param>\w+)$", line)


def is_port(line):
	line = sanitize_line(line)
	match = re.match("^(and|or|buf|not|xor)\s(\w+)(\s?)\(((\s?)((\w+)\,)?)+(\w+)\)\;$", line)
	if match:
		match = re.match("^(?P<xport_type>and|or|buf|not|xor)\s(?P<xport_name>\w+)\((?P<xport_args>.*)\)(\s?)\;$", line)
		matches = match.groupdict()
		module_args = matches['xport_args'].replace(' ', '')
		params = module_args.split(',')
		return {'status': True, 'type': matches['xport_type'] , 'args': params, 'name': matches['xport_name']}
	else: 
		return {'status': False}