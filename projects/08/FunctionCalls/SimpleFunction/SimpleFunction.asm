@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@0
D=A
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
@LCL
D=M
@1
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
M=!M
@SP
M=M+1
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
@SP
M=M-1
A=M
M=M+D
@SP
M=M+1
@ARG
D=M
@1
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
M=M-D
@SP
M=M+1
@LCL
D=M
@13
M=D
@5
D=D-A
A=D
D=M
@14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@13
M=M-1
D=M
A=D
D=M
@THAT
M=D
@13
M=M-1
D=M
A=D
D=M
@THIS
M=D
@13
M=M-1
D=M
A=D
D=M
@ARG
M=D
@13
M=M-1
D=M
A=D
D=M
@LCL
M=D
@14
A=M
0;JMP
(INFINITE_LOOP)
@INFINITE_LOOP
0;JMP
