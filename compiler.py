#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, 'lib')

import syntax_verifier
import wave_generator
import os.path


if len(sys.argv) == 3:
	verilog_file_path = sys.argv[1]
	wavein_file_path = sys.argv[2]

	if os.path.isfile(verilog_file_path) and os.path.isfile(wavein_file_path):		
		wavein_file_object = open(wavein_file_path,'r')
		wavein_file = wavein_file_object.read();		
		exec(wavein_file)
		
		if not 'wave_in_base' in vars():
			print('Arquivo de wavein inválido!')
		else:
			verilog_file_object = open(verilog_file_path,'r')
			extracted_data = syntax_verifier.init(verilog_file_object)
			if (extracted_data != False):
				print(wave_generator.init(extracted_data, wave_in_base))
	else:
		print('Arquivo(s) inválido(s), por favor verifique o caminho dos arquivo(s) informado(s).')
else:
	print('Este programa deve ser chamado junto com dois parametros: o arquivo verilog e o arquivo de wavein. Exemplo: "python3 compiler.py /caminho/absoluto/verilog.v /caminho/absoluto/wavein.py".')