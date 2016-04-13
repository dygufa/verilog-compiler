#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def init(file_object):
	return check_syntax(file_object)

def array_in_array(array_1, array_2):
	not_found_elements = []
	for el_1 in array_1:
		if not el_1 in array_2:
			not_found_elements.append(el_1)

	not_found_elements_length = len(not_found_elements)
	returned_dict = {'status': not not_found_elements_length}
	if not_found_elements_length:
		returned_dict['not_found_elements'] = not_found_elements
	return returned_dict

def check_syntax(file_object):
	file_lines = file_object.readlines();

	is_comment = False
	module_defined = False
	parameters = []
	extracted_data = {}
	k = 0
	error = False
	module_args = []

	extracted_data['outputs'] = []
	extracted_data['inputs'] = []
	extracted_data['wires'] = []
	extracted_data['ports'] = []

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
				res_array_in_array = array_in_array(res_xput['args'], module_args)
				if not res_array_in_array['status']:
					error = True
					print(res_xput['type'].title() + '(s) não declarado(s) no module na linha ' + str(k) + ': ' + ', '.join(res_array_in_array['not_found_elements']))
					break;

				if res_xput['type'] == 'input':
					extracted_data['inputs'] = extracted_data['inputs'] + res_xput['args']
				elif res_xput['type'] == 'output':
					extracted_data['outputs'] = extracted_data['outputs'] + res_xput['args']
			else:
				res_port = is_port(line) 
				if res_port['status']:
					res_array_in_array = array_in_array([res_port['output']] + res_port['inputs'], extracted_data['inputs'] + extracted_data['outputs'] + extracted_data['wires'])
					if not res_array_in_array['status']:
						error = True
						print('Entrada(s) ou saída não encontrado(s) na porta na linha ' + str(k) + ': ' + ', '.join(res_array_in_array['not_found_elements']))
						break;

					current_port_data = [{'id': res_port['name'], 'type': res_port['type'], 'delay': res_port['delay'], 'output': res_port['output'], 'inputs': res_port['inputs']}]
					extracted_data['ports'] = extracted_data['ports'] + current_port_data
				else:
					res_datatype = is_datatype(line)
					if res_datatype['status']:
						if res_datatype['type'] == 'wire':
							extracted_data['wires'] = extracted_data['wires'] + res_datatype['args']
					else:
						error = True
						print('Erro na linha ' + str(k) + ', estrutura não reconhecida.')
						break

					
		else:
			res_module = is_module(line)
			if (res_module['status']):
				module_args = res_module['args']
				module_defined = True
			else:
				error = True
				print('Erro, o código verilog não foi iniciado com module corretamente')
				break

	if error:
		return False

	return extracted_data


def sanitize_line(line):
	return line.replace("\n", '')

def is_module(line):
	line = sanitize_line(line)
	match = re.match("(\s*)module\s(\w+)(\s?)\(((\s?)((\w+)\,)?)+(\w+)\)\;$", line)
	if match:
		match = re.match("(\s*)module\s(?P<module_name>\w+)(\s?)\((?P<module_args>.*)\)\;$", line)
		matches = match.groupdict() 
		module_args = matches['module_args'].replace(' ', '')
		params = module_args.split(',')
		return {'status': True, 'args': params}
	else:
		return {'status': False}


def is_xput(line):
	line = sanitize_line(line)
	match = re.match("(\s*)(input|output)\s((\s?)((\w+)\,)?)+(\w+)\;$", line)
	if match:
		match = re.match("(\s*)(?P<xput_type>input|output)\s(?P<xput_args>.*)(\s?)\;$", line)
		matches = match.groupdict()
		module_args = matches['xput_args'].replace(' ', '')
		params = module_args.split(',')
		return {'status': True, 'type': matches['xput_type'] , 'args': params}
	else: 
		return {'status': False}

def is_datatype(line):
	line = sanitize_line(line)
	match = re.match("(\s*)(wire)\s((\s?)((\w+)\,)?)+(\w+)\;$", line)
	if match:
		match = re.match("(\s*)(?P<datatype_type>wire|integer|reg)\s(?P<datatype_args>.*)(\s?)\;$", line)
		matches = match.groupdict()
		datatype_args = matches['datatype_args'].replace(' ', '')
		params = datatype_args.split(',')
		return {'status': True, 'type': matches['datatype_type'] , 'args': params}
	else: 
		return {'status': False}


def is_port(line):
	line = sanitize_line(line)
	match = re.match("(\s*)(and|or|buf|not|xor)\s(\#([1-9]+)\s)?(\w+)(\s?)\(((\s?)((\w+)\,)?)+(\w+)\)\;$", line)
	if match:
		match = re.match("(\s*)(?P<xport_type>and|or|buf|not|xor)\s(?P<xport_delay>\#([1-9]+)(\s))?(?P<xport_name>\w+)\((?P<xport_args>.*)\)(\s?)\;$", line)
		matches = match.groupdict()
		port_args = matches['xport_args'].replace(' ', '')
		params = port_args.split(',')
		if matches['xport_type'] != 'not' and len(params) <= 2:
			return {'status': False}
		output = params[0]
		inputs = params[1:]
		if matches['xport_delay'] == None:
			delay = 0
		else: 
			delay = int(matches['xport_delay'].replace('#', ''))
		return {'status': True, 'type': matches['xport_type'] , 'delay': delay, 'output': output, 'inputs': inputs, 'name': matches['xport_name']}
	else: 
		return {'status': False}