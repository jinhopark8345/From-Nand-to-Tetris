""" CodeWriter
writes the assembly code that implements the parsed command"""

from vm_parser import VMParser
from pathlib import Path


class CodeWriter:
    """"""

    def __init__(
        self, input_file, output_file, lines, num_call, operation="a", debug=False
    ):

        self.debug = debug
        self.input_file = input_file
        print(f"current input file name: {self.input_file}")
        self.output_file = output_file
        self.debug_lines = list()
        self.lines = lines
        self.if_count = 0
        self.line_count = 0
        self.return_count = num_call
        self.command_type = set(
            ["push", "pop", "label", "if-goto", "goto", "call", "return", "function"]
        )
        self.labels = set()
        self.assem_lines = []

        self.f = open(self.output_file, operation)
        # self.ram = Ram()
        self.init_code_writer()

        self.f.close()

    def get_debug_lines(self):
        return self.debug_lines

    def write_line(self, line):
        if self.debug is True:
            print("\t\t<current line: {}>".format(line))

        command_type = line[0]
        if command_type in self.command_type:
            if command_type in ("push", "pop"):
                self.write_push_pop(line)
            elif command_type == "label":
                self.save_label(line)
            elif command_type in ("if-goto", "goto"):
                self.write_goto(line)
            elif command_type == "function":
                self.write_function(line)
            elif command_type == "call":
                self.write_call(line)
            elif command_type == "return":
                # self.write_return(line)
                self.write_return(line)
            else:
                print(f"undefined command type {command_type}")
        else:  # arithmetic command
            self.write_arithmetic(command_type)

    def init_code_writer(self):

        self.assem_lines.append("@256")
        self.assem_lines.append("D=A")
        self.assem_lines.append("@0")
        self.assem_lines.append("M=D")

        for line in self.lines:
            last_ass_line_num = len(self.assem_lines)
            self.write_line(line)
            cur_ass_line_num = len(self.assem_lines)

            if self.debug:
                self.debug_lines.append(line)
                self.debug_lines.extend(
                    self.assem_lines[last_ass_line_num:cur_ass_line_num]
                )

        for ass_line in self.assem_lines:
            self.f.writelines(ass_line + "\n")

    def get_assem_pop(self):
        assem_pop = ["@SP", "M=M-1", "A=M", "D=M"]
        return assem_pop

    def save_label(self, line):
        self.assem_lines.append(f"({line[1]})")

    def write_function(self, line):
        func_name = line[1]
        nargs = int(line[2])
        # (f)
        self.assem_lines.append("({})".format(func_name))

        # repeat k times: push 0
        for _ in range(nargs):
            self.write_push_pop(["push", "constant", 0])

    def write_return(self, _):
        assem_pop = ["@SP", "M=M-1", "A=M", "D=M"]

        # FRAME = LCL, *(@13) = FRAME
        self.assem_lines.append("@LCL")
        self.assem_lines.append("D=M")
        self.assem_lines.append("@13")
        self.assem_lines.append("M=D")

        # RET = *(FRAME-5), *(@14) = RET
        self.assem_lines.append("@5")
        self.assem_lines.append("D=D-A")
        self.assem_lines.append("A=D")
        self.assem_lines.append("D=M")
        self.assem_lines.append("@14")
        self.assem_lines.append("M=D")

        # *ARG = pop()
        self.assem_lines.extend(assem_pop)
        self.assem_lines.append("@ARG")
        self.assem_lines.append("A=M")
        self.assem_lines.append("M=D")  # *(@2) = pop()

        # SP = ARG+1
        self.assem_lines.append("@ARG")
        self.assem_lines.append("D=M+1")  # D = ARG+1
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=D")  # SP = D(=ARG+1)

        # THAT = *(FRAME-1)
        self.assem_lines.append("@13")
        self.assem_lines.append("D=M-1")  # D = FRAME-1
        self.assem_lines.append("A=D")  # A = FRAME-1
        self.assem_lines.append("D=M")  # D = *(FRAME-1)
        self.assem_lines.append("@THAT")
        self.assem_lines.append("M=D")  # THAT = *(FRAME-1)

        # THIS = *(FRAME-2)
        self.assem_lines.append("@13")
        self.assem_lines.append("D=M")  # D = FRAME
        self.assem_lines.append("@2")
        self.assem_lines.append("D=D-A")  # D = FRAME-2
        self.assem_lines.append("A=D")  # A = FRAME-2
        self.assem_lines.append("D=M")  # D = *(FRAME-2)
        self.assem_lines.append("@THIS")
        self.assem_lines.append("M=D")  # THIS = *(FRAME-2)

        # ARG = *(FRAME-3)
        self.assem_lines.append("@13")
        self.assem_lines.append("D=M")  # D = FRAME
        self.assem_lines.append("@3")
        self.assem_lines.append("D=D-A")  # D = FRAME-3
        self.assem_lines.append("A=D")  # A = FRAME-3
        self.assem_lines.append("D=M")  # D = *(FRAME-3)
        self.assem_lines.append("@ARG")
        self.assem_lines.append("M=D")  # ARG = *(FRAME-3)

        # LCL = *(FRAME-4)
        self.assem_lines.append("@13")
        self.assem_lines.append("D=M")  # D = FRAME
        self.assem_lines.append("@4")
        self.assem_lines.append("D=D-A")  # D = FRAME-4
        self.assem_lines.append("A=D")  # A = FRAME-4
        self.assem_lines.append("D=M")  # D = *(FRAME-4)
        self.assem_lines.append("@LCL")
        self.assem_lines.append("M=D")  # LCL = *(FRAME-4)

        # goto RET
        self.assem_lines.append("@14")
        self.assem_lines.append("A=M")
        self.assem_lines.append("0;JMP")

    def write_call(self, line):

        assem_push = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        # assem_pop = ['@SP', 'M=M-1', 'A=M', 'D=M']
        func = line[1]
        nargs = int(line[2])

        self.assem_lines.append("@{}$RETURN_ADDRESS{}".format(func, self.return_count))

        self.assem_lines.append("D=A")  # not sure if this is right
        self.assem_lines.extend(assem_push)

        # push LCL, ARG, THIS, THAT
        for i in range(1, 5):
            self.assem_lines.append("@{}".format(i))
            self.assem_lines.append("D=M")
            self.assem_lines.extend(assem_push)

        # reposition ARG, ARG = SP-n-5
        self.assem_lines.append("@SP")
        self.assem_lines.append("D=M")  # D = SP
        self.assem_lines.append("@{}".format(nargs + 5))
        self.assem_lines.append("D=D-A")  # D = SP - n - 5
        self.assem_lines.append("@ARG")
        self.assem_lines.append("M=D")  # ARG = SP - n - 5

        # reposition LCL, LCL = SP
        self.assem_lines.append("@SP")
        self.assem_lines.append("D=M")
        self.assem_lines.append("@LCL")
        self.assem_lines.append("M=D")  # LCL = SP

        # goto f, add vm function code
        self.assem_lines.append("@{}".format(func))
        self.assem_lines.append("0;JMP")

        # (return-address)
        self.assem_lines.append("({}$RETURN_ADDRESS{})".format(func, self.return_count))
        self.return_count += 1

    def write_goto(self, line):

        assem_pop = ["@SP", "M=M-1", "A=M", "D=M"]
        if line[0] == "goto":
            self.assem_lines.append(f"@{line[1]}")
            self.assem_lines.append("0;JMP")
        else:
            self.assem_lines.extend(assem_pop)
            self.assem_lines.append(f"@{line[1]}")
            # self.assem_lines.append('D;JGT') # troll
            self.assem_lines.append("D;JNE")  # fixed

    def write_arithmetic_neg(self):
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M-1")
        self.assem_lines.append("A=M")
        self.assem_lines.append("M=-M")

        # move sp pointer to the next one
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M+1")

    def write_arithmetic_not(self):
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M-1")
        self.assem_lines.append("A=M")
        self.assem_lines.append("M=!M")

        # move sp pointer to the next one
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M+1")

    def write_arithmetic_add(self):
        assem_pop = ["@SP", "M=M-1", "A=M", "D=M"]
        self.assem_lines.extend(assem_pop)
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M-1")
        self.assem_lines.append("A=M")

        self.assem_lines.append("M=M+D")

        # move sp pointer to the next one
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M+1")

    def write_arithmetic_sub(self):
        assem_pop = ["@SP", "M=M-1", "A=M", "D=M"]
        self.assem_lines.extend(assem_pop)
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M-1")
        self.assem_lines.append("A=M")

        self.assem_lines.append("M=M-D")

        # move sp pointer to the next one
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M+1")

    def write_arithmetic_and(self):
        self.assem_lines.extend(self.get_assem_pop())
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M-1")
        self.assem_lines.append("A=M")
        self.assem_lines.append("M=D&M")
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M+1")

    def write_arithmetic_or(self):
        self.assem_lines.extend(self.get_assem_pop())
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M-1")
        self.assem_lines.append("A=M")
        self.assem_lines.append("M=D|M")
        self.assem_lines.append("@SP")
        self.assem_lines.append("M=M+1")

    def write_arithmetic(self, command):
        assem_pop = ["@SP", "M=M-1", "A=M", "D=M"]

        if command == "neg":
            self.write_arithmetic_neg()

        elif command == "not":
            self.write_arithmetic_not()

        elif command == "add":
            self.write_arithmetic_add()

        elif command == "sub":
            self.write_arithmetic_sub()

        elif command == "and":
            self.write_arithmetic_and()

        elif command == "or":
            self.write_arithmetic_or()

        # eg, gt, lt
        elif command in ["eq", "gt", "lt"]:

            # pop twice and subtract two val and save at D
            self.assem_lines.extend(assem_pop)
            self.assem_lines.append("@SP")
            self.assem_lines.append("M=M-1")
            self.assem_lines.append("A=M")
            self.assem_lines.append("D=D-M")

            # 1 has to be a varaible
            self.assem_lines.append("@if_true{}".format(self.if_count))
            if command == "eq":
                self.assem_lines.append("D;JEQ")
            elif command == "gt":
                self.assem_lines.append("D;JLT")
            else:  # command == 'lt'
                self.assem_lines.append("D;JGT")
            self.assem_lines.append("@if_false{}".format(self.if_count))
            self.assem_lines.append("0;JMP")

            self.assem_lines.append("(if_true{})".format(self.if_count))
            self.assem_lines.append("@SP")
            self.assem_lines.append("A=M")
            self.assem_lines.append("M=-1")  # true
            self.assem_lines.append("@SP")
            self.assem_lines.append("M=M+1")
            self.assem_lines.append("@if_end{}".format(self.if_count))
            self.assem_lines.append("0;JMP")

            self.assem_lines.append("(if_false{})".format(self.if_count))
            self.assem_lines.append("@SP")
            self.assem_lines.append("A=M")
            self.assem_lines.append("M=0")  # false
            self.assem_lines.append("@SP")
            self.assem_lines.append("M=M+1")

            self.assem_lines.append("(if_end{})".format(self.if_count))

            self.if_count += 1
        else:
            print("undefined arithmetic input")

    def write_push_pop(self, line):
        command = line[0]
        seg = line[1]
        idx = int(line[2])

        assem_push = ["@SP", "A=M", "M=D", "@SP", "M=M+1"]
        assem_pop = ["@SP", "M=M-1", "A=M", "D=M"]
        assem_save_at13 = ["@13", "M=D"]
        assem_save_at14 = ["@14", "M=D"]

        assem_lines = []
        if command == "push":
            if seg == "constant":
                self.assem_lines.append("@{}".format(idx))
                self.assem_lines.append("D=A")
                self.assem_lines.extend(assem_push)

            elif seg in ["static", "temp", "pointer"]:
                if seg == "static":
                    # self.assem_lines.append('@{}'.format(16 + idx)) # wrong
                    temp_str = "@{}.{}".format(self.input_file, idx)
                    print("temp_str :", temp_str)
                    self.assem_lines.append("@{}.{}".format(self.input_file, idx))
                elif seg == "temp":
                    self.assem_lines.append("@{}".format(5 + idx))
                elif seg == "pointer":
                    self.assem_lines.append("@{}".format(3 + idx))
                else:
                    print("undefined segment input")

                self.assem_lines.append("D=M")
                self.assem_lines.extend(assem_push)
            else:
                if seg == "local":
                    self.assem_lines.append("@LCL")
                elif seg == "argument":
                    self.assem_lines.append("@ARG")
                elif seg == "this":
                    self.assem_lines.append("@THIS")
                elif seg == "that":
                    self.assem_lines.append("@THAT")
                else:
                    print("undefined segment input")

                self.assem_lines.append("D=M")
                self.assem_lines.append("@{}".format(idx))
                self.assem_lines.append("A=A+D")
                self.assem_lines.append("D=M")
                self.assem_lines.extend(assem_push)
        else:  # pop
            if seg in ["static", "temp", "pointer"]:
                self.assem_lines.extend(assem_pop)
                if seg == "static":
                    # self.assem_lines.append('@{}'.format(16 + idx))
                    self.assem_lines.append("@{}.{}".format(self.input_file, idx))
                elif seg == "temp":
                    self.assem_lines.append("@{}".format(5 + idx))
                elif seg == "pointer":
                    self.assem_lines.append("@{}".format(3 + idx))
                self.assem_lines.append("M=D")
            elif seg in ["local", "argument", "this", "that"]:
                self.assem_lines.extend(assem_pop)
                self.assem_lines.extend(assem_save_at13)

                if seg == "local":
                    self.assem_lines.append("@LCL")
                elif seg == "argument":
                    self.assem_lines.append("@ARG")
                elif seg == "this":
                    self.assem_lines.append("@THIS")
                elif seg == "that":
                    self.assem_lines.append("@THAT")

                self.assem_lines.append("D=M")
                self.assem_lines.append("@{}".format(idx))
                self.assem_lines.append("D=D+A")
                self.assem_lines.extend(assem_save_at14)

                self.assem_lines.append("@13")
                self.assem_lines.append("D=M")
                self.assem_lines.append("@14")
                self.assem_lines.append("A=M")
                self.assem_lines.append("M=D")

        for ass_line in assem_lines:
            self.f.writelines(ass_line + "\n")
