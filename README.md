Verilog Output Weaver Generator
================

Verilog Output Weaver Generator allows you to generate the output wave from a digital circuit using a Verilog¹ file and the input states described on a "wave in" file. If you didn't get it: check the example below! :) 

¹ *In case you don't know: Verilog is a hardware description language that allow us to represent digital circuits.*

Try it:
```
python3 compiler.py [VERILOG FILE] [WAVE IN FILE]
```

## Example

If you have no clue about what I'm talking about, please let me give you an example:

#### 1. First we need a circuit (and a Verilog file that describe it)!

Let's use this one:

![Circuit](circuit.png)

and this is the respective Verilog description file (let's name it verilog.v):
```
module Exemplo(I1, I2, O1, O2);

input I1, I2;
output O1, O2;

and AND(O1, I1, I2);
or OR(O2, I1, I2);

endmodule
```

#### 2. Now we need to figure out some inputs for the circuit above:

Input waves:

![Wave in](wavein.png)

We can represent the waves above in a python file (let's name it wave_in.py):
```
wave_in_base = [
	['I1', [1, 0, 1]],
	['I2', [1, 0, 0]]
]
```

#### 3. It's done! We just need to run it:

```
python3 compiler.py verilog.v wave_in.py
```

and we will get:
```
{'O2': [1, 0, 1], 'O1': [1, 0, 0]}
```
