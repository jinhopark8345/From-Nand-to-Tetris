@256
D=A
@0
M=D
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@13
M=D
@LCL
D=M
@0
D=D+A
@14
M=D
@13
D=M
@14
A=M
M=D
(LOOP_START)
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@13
M=D
@LCL
D=M
@0
D=D+A
@14
M=D
@13
D=M
@14
A=M
M=D
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@13
M=D
@ARG
D=M
@0
D=D+A
@14
M=D
@13
D=M
@14
A=M
M=D
@ARG
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@LOOP_START
D;JGT
@LCL
D=M
@0
A=A+D
D=M
@SP
A=M
M=D
@SP
M=M+1
(INFINITE_LOOP)
@INFINITE_LOOP
0;JMP
