@261
D=A
@0
M=D
(Sys.init)
@6
D=A
@SP
A=M
M=D
@SP
M=M+1
@8
D=A
@SP
A=M
M=D
@SP
M=M+1
@Class1.set$RETURN_ADDRESS0
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(Class1.set$RETURN_ADDRESS0)
@SP
M=M-1
A=M
D=M
@5
M=D
@23
D=A
@SP
A=M
M=D
@SP
M=M+1
@15
D=A
@SP
A=M
M=D
@SP
M=M+1
@Class2.set$RETURN_ADDRESS1
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@2
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(Class2.set$RETURN_ADDRESS1)
@SP
M=M-1
A=M
D=M
@5
M=D
@Class1.get$RETURN_ADDRESS2
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(Class1.get$RETURN_ADDRESS2)
@Class2.get$RETURN_ADDRESS3
D=A
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=M
@SP
A=M
M=D
@SP
M=M+1
@3
D=M
@SP
A=M
M=D
@SP
M=M+1
@4
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Class2.get
0;JMP
(Class2.get$RETURN_ADDRESS3)
(WHILE)
@WHILE
0;JMP
(Class1.set)
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
@16
M=D
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
@17
M=D
@0
D=A
@SP
A=M
M=D
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
(Class1.get)
@16
D=M
@SP
A=M
M=D
@SP
M=M+1
@17
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
(Class2.set)
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
@16
M=D
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
@17
M=D
@0
D=A
@SP
A=M
M=D
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
(Class2.get)
@16
D=M
@SP
A=M
M=D
@SP
M=M+1
@17
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
