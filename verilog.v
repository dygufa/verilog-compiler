module Exemplo(I1, I2, I3, O);

input I1, I2;
input I3;
output O;

wire W_1;
wire W_2;
wire W_3;

not NOT_1(W_3, I2);
and #2 AND_1(W_1, I1, W_3);
and AND_2(O, W_1, W_2);
and #4 AND_3(W_2, I1, I3);

endmodule
