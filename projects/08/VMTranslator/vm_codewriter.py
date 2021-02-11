""" CodeWriter
writes the assembly code that implements the parsed command"""

# from ram import Ram

from vm_parser import VMParser
from pathlib import Path


class CodeWriter:
  """

  """
  def __init__(self, input_file, output_file, lines, operation='w'):

    self.debug = False
    self.input_file = input_file
    print(f'current input file name: {self.input_file}')
    self.output_file = output_file
    self.lines = lines
    self.if_count = 0
    self.line_count = 0
    self.return_count = 0
    self.command_type = set([
        'push', 'pop', 'label', 'if-goto', 'goto', 'call', 'return', 'function'
    ])
    self.labels = set()
    self.assem_lines = []

    self.f = open(self.output_file, operation)
    # self.ram = Ram()

    self.init_code_writer()

    self.f.close()

  def write_line(self, line):
    if self.debug is True:
      print("\t\t<current line: {}>".format(line))

    command_type = line[0]
    if command_type in self.command_type:
      if command_type in ('push', 'pop'):
        self.write_push_pop(line)
      elif command_type == 'label':
        self.save_label(line)
      elif command_type in ('if-goto', 'goto'):
        self.write_goto(line)
      elif command_type == 'function':
        self.write_function(line)
      elif command_type == 'call':
        self.write_call(line)
      elif command_type == 'return':
        # self.write_return(line)
        self.write_return2(line)
      else:
        print(f"undefined command type {command_type}")
    else:  # arithmetic command
      self.write_arithmetic(command_type)

  def init_code_writer(self):

    # self.assem_lines.append('@261')
    # self.assem_lines.append('@256')
    # self.assem_lines.append('D=A')
    # self.assem_lines.append('@0')
    # self.assem_lines.append('M=D')

    # self.assem_lines.append('@300')
    # self.assem_lines.append('D=A')
    # self.assem_lines.append('@1')
    # self.assem_lines.append('M=D')

    # self.assem_lines.append('@400')
    # self.assem_lines.append('D=A')
    # self.assem_lines.append('@2')
    # self.assem_lines.append('M=D')
    # goto f, add vm function code

    # self.assem_lines.append('@3000')
    # self.assem_lines.append('D=A')
    # self.assem_lines.append('@3')
    # self.assem_lines.append('M=D')

    # self.assem_lines.append('@3010')
    # self.assem_lines.append('D=A')
    # self.assem_lines.append('@4')
    # self.assem_lines.append('M=D')

    # for ass_line in self.assem_lines:
    #   self.f.writelines(ass_line + '\n')

    for line in self.lines:
      # if self.line_count == 15:
      #   break
      # self.line_count += 1

      last_ass_line_num = len(self.assem_lines)
      label_cnt = len([line for line in self.assem_lines if line[0].startswith('(')])
      # print(f'label_cnt: {label_cnt}')
      self.write_line(line)
      cur_ass_line_num = len(self.assem_lines)

      if self.debug is True:
        for i in range(last_ass_line_num, cur_ass_line_num):
          print('lcnt: {}\t{}'.format(i - label_cnt, self.assem_lines[i]))
      # print('\n'.join(self.assem_lines[last_ass_line_num:cur_ass_line_num]))

    # self.assem_lines.append('(INFINITE_LOOP)')
    # self.assem_lines.append('@INFINITE_LOOP')
    # self.assem_lines.append('0;JMP')

    for ass_line in self.assem_lines:
      self.f.writelines(ass_line + '\n')
      # self.vm_debugger()
  def save_label(self, line):
    self.assem_lines.append(f'({line[1]})')

  def write_function(self, line):
    func_name = line[1]
    nargs = int(line[2])
    # (f)
    self.assem_lines.append('({})'.format(func_name))

    # repeat k times: push 0
    for _ in range(nargs):
      self.write_push_pop(['push', 'constant', 0])

  def write_return2(self, _):
    assem_pop = ['@SP', 'M=M-1', 'A=M', 'D=M']

    # FRAME = LCL, *(@13) = FRAME
    self.assem_lines.append('@LCL')
    self.assem_lines.append('D=M')
    self.assem_lines.append('@13')
    self.assem_lines.append('M=D')

    # RET = *(FRAME-5), *(@14) = RET
    self.assem_lines.append('@5')
    self.assem_lines.append('D=D-A')
    self.assem_lines.append('A=D')
    self.assem_lines.append('D=M')
    self.assem_lines.append('@14')
    self.assem_lines.append('M=D')

    # *ARG = pop()
    self.assem_lines.extend(assem_pop)
    self.assem_lines.append('@ARG')
    self.assem_lines.append('A=M')
    self.assem_lines.append('M=D')  # *(@2) = pop()

    # SP = ARG+1
    self.assem_lines.append('@ARG')
    self.assem_lines.append('D=M+1')  # D = ARG+1
    self.assem_lines.append('@SP')
    self.assem_lines.append('M=D')  # SP = D(=ARG+1)

    # THAT = *(FRAME-1)
    self.assem_lines.append('@13')
    self.assem_lines.append('D=M-1')  # D = FRAME-1
    self.assem_lines.append('A=D')  # A = FRAME-1
    self.assem_lines.append('D=M')  # D = *(FRAME-1)
    self.assem_lines.append('@THAT')
    self.assem_lines.append('M=D')  # THAT = *(FRAME-1)

    # THIS = *(FRAME-2)
    self.assem_lines.append('@13')
    self.assem_lines.append('D=M')  # D = FRAME
    self.assem_lines.append('@2')
    self.assem_lines.append('D=D-A')  # D = FRAME-2
    self.assem_lines.append('A=D')  # A = FRAME-2
    self.assem_lines.append('D=M')  # D = *(FRAME-2)
    self.assem_lines.append('@THIS')
    self.assem_lines.append('M=D')  # THIS = *(FRAME-2)

    # ARG = *(FRAME-3)
    self.assem_lines.append('@13')
    self.assem_lines.append('D=M')  # D = FRAME
    self.assem_lines.append('@3')
    self.assem_lines.append('D=D-A')  # D = FRAME-3
    self.assem_lines.append('A=D')  # A = FRAME-3
    self.assem_lines.append('D=M')  # D = *(FRAME-3)
    self.assem_lines.append('@ARG')
    self.assem_lines.append('M=D')  # ARG = *(FRAME-3)

    # LCL = *(FRAME-4)
    self.assem_lines.append('@13')
    self.assem_lines.append('D=M')  # D = FRAME
    self.assem_lines.append('@4')
    self.assem_lines.append('D=D-A')  # D = FRAME-4
    self.assem_lines.append('A=D')  # A = FRAME-4
    self.assem_lines.append('D=M')  # D = *(FRAME-4)
    self.assem_lines.append('@LCL')
    self.assem_lines.append('M=D')  # LCL = *(FRAME-4)

    # goto RET
    self.assem_lines.append('@14')
    self.assem_lines.append('A=M')
    self.assem_lines.append('0;JMP')

  def write_return(self, _):
    assem_pop = ['@SP', 'M=M-1', 'A=M', 'D=M']
    # FRAME = LCL, *(@13) = FRAME
    self.assem_lines.append('@LCL')
    self.assem_lines.append('D=M')
    self.assem_lines.append('@13')
    self.assem_lines.append('M=D')

    # RET = *(FRAME-5), *(@14) = RET
    self.assem_lines.append('@5')
    self.assem_lines.append('D=D-A')
    self.assem_lines.append('A=D')
    self.assem_lines.append('D=M')
    self.assem_lines.append('@14')
    self.assem_lines.append('M=D')

    # *ARG = pop()
    self.assem_lines.extend(assem_pop)
    self.assem_lines.append('@ARG')
    self.assem_lines.append('A=M')
    self.assem_lines.append('M=D')  # *(@2) = pop()

    # SP = ARG+1
    self.assem_lines.append('@ARG')
    self.assem_lines.append('D=M+1')  # D = ARG+1
    self.assem_lines.append('@SP')
    self.assem_lines.append('M=D')  # SP = D(=ARG+1)

    # THAT = *(FRAME-1)
    self.assem_lines.append('@13')
    self.assem_lines.append('M=M-1')  # M = FRAME-1, *(@13) = FRAME-1
    self.assem_lines.append('D=M')  # D = FRAME-1
    self.assem_lines.append('A=D')
    self.assem_lines.append('D=M')  # D = *(FRAME-1)
    self.assem_lines.append('@THAT')
    self.assem_lines.append('M=D')

    # THIS = *(FRAME-2)
    self.assem_lines.append('@13')
    self.assem_lines.append('M=M-1')  # M = FRAME-2, *(@13) = FRAME-2
    self.assem_lines.append('D=M')  # D = FRAME-2
    self.assem_lines.append('A=D')
    self.assem_lines.append('D=M')  # D = *(FRAME-2)
    self.assem_lines.append('@THIS')
    self.assem_lines.append('M=D')

    # ARG = *(FRAME-3)
    self.assem_lines.append('@13')
    self.assem_lines.append('M=M-1')  # M = FRAME-3, *(@13) = FRAME-3
    self.assem_lines.append('D=M')  # D = FRAME-3
    self.assem_lines.append('A=D')
    self.assem_lines.append('D=M')  # D = *(FRAME-3)
    self.assem_lines.append('@ARG')
    self.assem_lines.append('M=D')

    # LCL = *(FRAME-4)
    self.assem_lines.append('@13')
    self.assem_lines.append('M=M-1')  # M = FRAME-4, *(@14) = FRAME-4
    self.assem_lines.append('D=M')  # D = FRAME-4
    self.assem_lines.append('A=D')
    self.assem_lines.append('D=M')  # D = *(FRAME-4)
    self.assem_lines.append('@LCL')
    self.assem_lines.append('M=D')

    # goto RET
    self.assem_lines.append('@14')
    self.assem_lines.append('A=M')
    self.assem_lines.append('0;JMP')

  def write_call(self, line):

    assem_push = ['@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
    # assem_pop = ['@SP', 'M=M-1', 'A=M', 'D=M']
    func = line[1]
    nargs = int(line[2])

    self.assem_lines.append('@{}$RETURN_ADDRESS{}'.format(func, self.return_count))

    self.assem_lines.append('D=A')  # not sure if this is right
    self.assem_lines.extend(assem_push)

    # push LCL, ARG, THIS, THAT
    # for i in range(1, 5):
    #   self.assem_lines.append('@{}'.format(i))
    #   self.assem_lines.append('D=M')
    #   self.assem_lines.extend(assem_push)

    self.assem_lines.append('@LCL')
    self.assem_lines.append('D=M')
    self.assem_lines.extend(assem_push)

    self.assem_lines.append('@ARG')
    self.assem_lines.append('D=M')
    self.assem_lines.extend(assem_push)

    self.assem_lines.append('@THIS')
    self.assem_lines.append('D=M')
    self.assem_lines.extend(assem_push)

    self.assem_lines.append('@THAT')
    self.assem_lines.append('D=M')
    self.assem_lines.extend(assem_push)

    # reposition ARG, ARG = SP-n-5
    self.assem_lines.append('@SP')
    self.assem_lines.append('D=M')  # D = SP
    self.assem_lines.append('@{}'.format(nargs + 5))
    self.assem_lines.append('D=D-A')  # D = SP - n - 5
    self.assem_lines.append('@ARG')
    self.assem_lines.append('M=D')  # ARG = SP - n - 5

    # reposition LCL, LCL = SP
    self.assem_lines.append('@SP')
    self.assem_lines.append('D=M')
    self.assem_lines.append('@LCL')
    self.assem_lines.append('M=D')  # LCL = SP

    # goto f, add vm function code
    self.assem_lines.append('@{}'.format(func))
    self.assem_lines.append('0;JMP')

    # (return-address)
    self.assem_lines.append('({}$RETURN_ADDRESS{})'.format(func, self.return_count))
    self.return_count += 1

  def write_goto(self, line):

    assem_pop = ['@SP', 'M=M-1', 'A=M', 'D=M']
    if line[0] == 'goto':
      self.assem_lines.append(f'@{line[1]}')
      self.assem_lines.append('0;JMP')
    else:
      self.assem_lines.extend(assem_pop)
      self.assem_lines.append(f'@{line[1]}')
      # self.assem_lines.append('D;JGT') # troll
      self.assem_lines.append('D;JNE')  # fixed

  def write_arithmetic(self, command):
    assem_pop = ['@SP', 'M=M-1', 'A=M', 'D=M']

    # ned, not
    if command == 'neg':
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M-1')
      self.assem_lines.append('A=M')
      self.assem_lines.append('M=-M')

      # move sp pointer to the next one
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M+1')

    elif command == 'not':
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M-1')
      self.assem_lines.append('A=M')
      self.assem_lines.append('M=!M')

      # move sp pointer to the next one
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M+1')

    # add, sub
    elif command in ['add', 'sub']:
      self.assem_lines.extend(assem_pop)
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M-1')
      self.assem_lines.append('A=M')
      if command == 'add':
        self.assem_lines.append('M=M+D')
      else:  # command == 'sub'
        self.assem_lines.append('M=M-D')

      # move sp pointer to the next one
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M+1')

    # and, or
    elif command in ['and', 'or']:
      self.assem_lines.extend(assem_pop)
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M-1')
      self.assem_lines.append('A=M')

      if command == 'and':
        self.assem_lines.append('M=D&M')
      else:  # command == 'or'
        self.assem_lines.append('M=D|M')

      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M+1')

    # eg, gt, lt
    elif command in ['eq', 'gt', 'lt']:

      # pop twice and subtract two val and save at D
      self.assem_lines.extend(assem_pop)
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M-1')
      self.assem_lines.append('A=M')
      self.assem_lines.append('D=D-M')

      # 1 has to be a varaible
      self.assem_lines.append('@if_true{}'.format(self.if_count))
      if command == 'eq':
        self.assem_lines.append('D;JEQ')
      elif command == 'gt':
        self.assem_lines.append('D;JLT')
      else:  # command == 'lt'
        self.assem_lines.append('D;JGT')
      self.assem_lines.append('@if_false{}'.format(self.if_count))
      self.assem_lines.append('0;JMP')

      self.assem_lines.append('(if_true{})'.format(self.if_count))
      self.assem_lines.append('@SP')
      self.assem_lines.append('A=M')
      self.assem_lines.append('M=-1')  # true
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M+1')
      self.assem_lines.append('@if_end{}'.format(self.if_count))
      self.assem_lines.append('0;JMP')

      self.assem_lines.append('(if_false{})'.format(self.if_count))
      self.assem_lines.append('@SP')
      self.assem_lines.append('A=M')
      self.assem_lines.append('M=0')  # false
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M+1')

      self.assem_lines.append('(if_end{})'.format(self.if_count))

      self.if_count += 1
    else:
      print("undefined arithmetic input")

  def write_push_pop(self, line):
    command = line[0]
    seg = line[1]
    idx = int(line[2])

    assem_push = ['@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
    assem_pop = ['@SP', 'M=M-1', 'A=M', 'D=M']
    assem_save_at13 = ['@13', 'M=D']
    assem_save_at14 = ['@14', 'M=D']

    assem_lines = []
    if command == 'push':
      if seg == 'constant':
        self.assem_lines.append('@{}'.format(idx))
        self.assem_lines.append('D=A')
        self.assem_lines.extend(assem_push)

      elif seg in ['static', 'temp', 'pointer']:
        if seg == 'static':
          # self.assem_lines.append('@{}'.format(16 + idx)) # wrong
          temp_str = '@{}.{}'.format(self.input_file, idx)
          print("temp_str :",temp_str)
          self.assem_lines.append('@{}.{}'.format(self.input_file, idx))
        elif seg == 'temp':
          self.assem_lines.append('@{}'.format(5 + idx))
        elif seg == 'pointer':
          self.assem_lines.append('@{}'.format(3 + idx))
        else:
          print("undefined segment input")

        self.assem_lines.append('D=M')
        self.assem_lines.extend(assem_push)
      else:
        if seg == 'local':
          self.assem_lines.append('@LCL')
        elif seg == 'argument':
          self.assem_lines.append('@ARG')
        elif seg == 'this':
          self.assem_lines.append('@THIS')
        elif seg == 'that':
          self.assem_lines.append('@THAT')
        else:
          print("undefined segment input")

        self.assem_lines.append('D=M')
        self.assem_lines.append('@{}'.format(idx))
        self.assem_lines.append('A=A+D')
        self.assem_lines.append('D=M')
        self.assem_lines.extend(assem_push)
    else:  # pop
      if seg in ['static', 'temp', 'pointer']:
        self.assem_lines.extend(assem_pop)
        if seg == 'static':
          # self.assem_lines.append('@{}'.format(16 + idx))
          self.assem_lines.append('@{}.{}'.format(self.input_file, idx))
        elif seg == 'temp':
          self.assem_lines.append('@{}'.format(5 + idx))
        elif seg == 'pointer':
          self.assem_lines.append('@{}'.format(3 + idx))
        self.assem_lines.append('M=D')
      elif seg in ['local', 'argument', 'this', 'that']:
        self.assem_lines.extend(assem_pop)
        self.assem_lines.extend(assem_save_at13)

        if seg == 'local':
          self.assem_lines.append('@LCL')
        elif seg == 'argument':
          self.assem_lines.append('@ARG')
        elif seg == 'this':
          self.assem_lines.append('@THIS')
        elif seg == 'that':
          self.assem_lines.append('@THAT')

        self.assem_lines.append('D=M')
        self.assem_lines.append('@{}'.format(idx))
        self.assem_lines.append('D=D+A')
        self.assem_lines.extend(assem_save_at14)

        self.assem_lines.append('@13')
        self.assem_lines.append('D=M')
        self.assem_lines.append('@14')
        self.assem_lines.append('A=M')
        self.assem_lines.append('M=D')

    for ass_line in assem_lines:
      self.f.writelines(ass_line + '\n')

    # print(assem_lines)

  def test_basic_test(self):
    assert self.ram[256] == 472
    assert self.ram[257] == 510
    assert self.ram[258] == 36
    assert self.ram.sp_addr == 257

    assert self.ram[300] == 10

    assert self.ram[401] == 21
    assert self.ram[402] == 22
    assert self.ram[3006] == 36
    assert self.ram[3012] == 42
    assert self.ram[3015] == 45

  def test_pointer_test(self):

    assert self.ram[256] == 6084
    assert self.ram[257] == 46
    assert self.ram.sp_addr == 257

    assert self.ram[3] == 3030
    assert self.ram[4] == 3040

    assert self.ram[3030 + 2] == 32
    assert self.ram[3040 + 6] == 46

  def test_static_test(self):
    assert self.ram[256] == 1110
    assert self.ram[257] == 888
    assert self.ram[258] == 888
    assert self.ram.sp_addr == 257

    assert self.ram[17] == 111
    assert self.ram[19] == 333
    assert self.ram[24] == 888


if __name__ == '__main__':
  # vm_file = sys.argv[1]
  # asm_file = os.path.splitext(vm_file)[0] + '.asm'
  # lines = VMParser(sys.argv[1]).get_commands()

  import os
  from pathlib import Path

  # single file test
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/SimpleFunction/SimpleFunction.vm'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.vm'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/Sys.vm'

  # dir test
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement'
  input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/SimpleFunction'

  extension = ".vm"
  if os.path.isdir(input_path):
    print("\tinput is a dir")

    # make vm_files list
    vm_files = list()
    for subdir, dirs, files in os.walk(input_path):
      for file in files:
        if file.endswith(extension):

          file_path = input_path + '/' + str(file)
          if file == 'Sys.vm':
            vm_files.insert(0, file_path)
          else:
            vm_files.append(file_path)

    # set asm file path
    p_path = Path(vm_files[0]).parent
    pp_path = p_path.parent

    f_name = str(p_path)[len(str(pp_path)) + 1:] # f_name is wrong
    file_name = str(p_path)[len(str(pp_path)) + 1:] + '.asm'
    asm_file_path = str(p_path) + '/' + file_name
    print(f'asm_file path: {asm_file_path}')

    vm_lines = list()

    # empty the file first
    file = open(asm_file_path, "w")
    file.close()

    # append assembly code file by file
    for vm_file in vm_files:
      vm_lines = VMParser(vm_file).get_commands()
      temp_name = os.path.splitext(vm_file)[0].split(sep='/')[-1]
      CodeWriter(temp_name, asm_file_path, vm_lines, operation='a')

  elif os.path.isfile(input_path):
    print("\tinput is a file")
    vm_file = input_path
    p_path = Path(vm_file).parent
    pp_path = p_path.parent
    f_name = str(p_path)[len(str(pp_path)) + 1:] # f_name is wrong
    print("f_name ", f_name)

    file_name = str(p_path)[len(str(pp_path)) + 1:] + '.asm'
    asm_file_path = str(p_path) + '/' + file_name
    # print(asm_file_path)

    lines = VMParser(input_path).get_commands()
    # lines.extend(VMParser(vm_file2).get_commands())
    # for l in lines:
    #   print(l)
    # # lines.extend(VMParser(vm_file3).get_commands())
    temp_name = os.path.splitext(vm_file)[0].split(sep='/')[-1]
    CodeWriter(temp_name, asm_file_path, vm_lines, operation='a')


  else:
    print("Not a file or dir")
