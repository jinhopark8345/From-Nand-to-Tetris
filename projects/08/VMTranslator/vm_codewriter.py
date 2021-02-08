""" CodeWriter
writes the assembly code that implements the parsed command"""

# from ram import Ram

from vm_parser import VMParser


class CodeWriter:
  """

  """
  def __init__(self, output_file, lines):

    self.output_file = output_file
    self.lines = lines
    self.if_count = 0
    self.line_count = 0
    self.command_type = set(['push', 'pop', 'label', 'if-goto',
                         'goto', 'call', 'return', 'function'])
    self.labels = set()
    self.assem_lines = []

    self.f = open(self.output_file, 'w')
    # self.ram = Ram()

    self.init_code_writer()

    self.f.close()

  def init_code_writer(self):

    self.assem_lines.append('@256')
    self.assem_lines.append('D=A')
    self.assem_lines.append('@0')
    self.assem_lines.append('M=D')

    self.assem_lines.append('@300')
    self.assem_lines.append('D=A')
    self.assem_lines.append('@1')
    self.assem_lines.append('M=D')

    self.assem_lines.append('@400')
    self.assem_lines.append('D=A')
    self.assem_lines.append('@2')
    self.assem_lines.append('M=D')

    self.assem_lines.append('@3000')
    self.assem_lines.append('D=A')
    self.assem_lines.append('@3')
    self.assem_lines.append('M=D')

    self.assem_lines.append('@3010')
    self.assem_lines.append('D=A')
    self.assem_lines.append('@4')
    self.assem_lines.append('M=D')

    # for ass_line in self.assem_lines:
    #   self.f.writelines(ass_line + '\n')

    for line in self.lines:
      # if self.line_count == 31:
      #   break
      # self.line_count += 1

      print("current line: {}".format(line))
      # self.ram.process_line(line)

      command_type = line[0]
      if command_type in self.command_type:
        if command_type in ('push', 'pop'):
          self.write_push_pop(line)
        if command_type == 'label':
          self.save_label(line)
        if command_type in ('if-goto', 'goto'):
          self.write_goto(line)
      else:  # arithmetic command
        self.write_arithmetic(command_type)

    self.assem_lines.append('(INFINITE_LOOP)')
    self.assem_lines.append('@INFINITE_LOOP')
    self.assem_lines.append('0;JMP')

    for ass_line in self.assem_lines:
      self.f.writelines(ass_line + '\n')
      # self.vm_debugger()
  def save_label(self, line):
    self.assem_lines.append(f'({line[1]})')
  def write_goto(self, line):

    assem_pop = ['@SP', 'M=M-1', 'A=M', 'D=M']
    if line[0] == 'goto':
      self.assem_lines.append(f'@{line[1]}')
      self.assem_lines.append('0;JMP')
    else:
      self.assem_lines.extend(assem_pop)
      self.assem_lines.append(f'@{line[1]}')
      self.assem_lines.append('D;JGT')

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
      self.assem_lines.append('M=-1') # true
      self.assem_lines.append('@SP')
      self.assem_lines.append('M=M+1')
      self.assem_lines.append('@if_end{}'.format(self.if_count))
      self.assem_lines.append('0;JMP')

      self.assem_lines.append('(if_false{})'.format(self.if_count))
      self.assem_lines.append('@SP')
      self.assem_lines.append('A=M')
      self.assem_lines.append('M=0') # false
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
          self.assem_lines.append('@{}'.format(16 + idx))
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
          self.assem_lines.append('@{}'.format(16 + idx))
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

  vm_file = '/home/jinho/Dropbox/Projects/FromNandToTetris/projects/07/StackArithmetic/StackTest/StackTest.vm'
  output_file = '/home/jinho/Dropbox/Projects/FromNandToTetris/projects/07/StackArithmetic/StackTest/StackTest.asm'
  lines = VMParser(vm_file).get_commands()
  cw = CodeWriter(output_file, lines)
