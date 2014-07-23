module Exemplo(I1, I2, I3, O)

input I1, I2;
input I3;
output O;

wire W_1;

and AND_1(W_1, I1, I2);
and AND_2(O, I3, W_1);

endmodule