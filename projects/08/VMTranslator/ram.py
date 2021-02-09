class Ram:
  """

  """
  def __init__(self,
               sp_addr=256,
               lcl_addr=300,
               arg_addr=400,
               this_addr=3000,
               that_addr=3010,
               temp_addr=5,
               gpr_addr=13,
               sv_addr=16):
    self.sp_addr = sp_addr
    self.lcl_addr = lcl_addr
    # self.lcl_addr = 1
    self.arg_addr = arg_addr
    self.this_addr = this_addr  # pointer segment
    self.that_addr = that_addr  # pointer segment
    self.temp_addr = temp_addr  # temporary segment : 5-12
    self.gpr_addr = gpr_addr  # general purpose registers: 13-15

    self.sv_addr = sv_addr  # static variables : 16-255
    # self.stack_addr = 256  # stack : 256-2047?

    self.arithmetic = [
        'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'
    ]
    self.ram = [None] * 4000

  def segment2addr(self, segment):
    if segment == 'pointer': return [self.this_addr, self.that_addr]
    elif segment == 'local': return self.lcl_addr
    elif segment == 'argument': return self.arg_addr
    elif segment == 'this': return self.this_addr
    elif segment == 'that': return self.that_addr
    elif segment == 'static': return self.sv_addr
    elif segment == 'temp': return self.temp_addr
    elif segment == 'constant': return self.sp_addr
    elif segment == 'sp': return self.sp_addr
    else:
      print('undefined segment: {}'.format(segment))
      return -5000

  def __getitem__(self, idx):
    return self.ram[idx]

  def __setitem__(self, idx, value):
    self.ram[idx] = value

  def get_segment_addr(self, segment, idx):
    if segment == 'pointer':
      # return self.segment2addr(segment)[idx]
      return self.ram[3 + idx]
    elif segment == 'constant':
      # idx doesn't matter, in this case idx will e the value itself
      return self.segment2addr(segment)
    else:
      temp = self.segment2addr(segment) + idx
      return temp

  def set_segment_addr(self, segment, addr):
    if segment == 'local': self.lcl_addr = addr
    elif segment == 'argument': self.arg_addr = addr
    elif segment == 'this': self.this_addr = addr
    elif segment == 'that': self.that_addr = addr
    elif segment == 'static': self.sv_addr = addr
    elif segment == 'temp': self.temp_addr = addr
    elif segment == 'sp': self.sp_addr = addr
    else:
      print('undefined segment: {}'.format(segment))

    # addr = self.segment2addr[segment] + idx

  def set_segment_value(self, segment, idx, value):
    segment_addr = self.get_segment_addr(segment, idx)
    self.ram[segment_addr] = value

  def get_segment_value(self, segment, idx):
    segment_addr = self.get_segment_addr(segment, idx)
    return self.ram[segment_addr]

  def rampush(self, segment, idx):
    if segment != 'constant':
      # push the value
      val = self.get_segment_value(segment, idx)
      self.set_segment_value('constant', idx,
                             val)  # push always add value to stack

    else:  # segment == 'constant'
      val = idx
      # set the value
      self.set_segment_value(segment, val, val)

    # move the pointer
    self.sp_addr += 1

  def rampop(self):
    self.sp_addr -= 1
    return self.ram[self.sp_addr]

  def process_line(self, line):
    # print("current line {}".format(line))
    command_type = line[0]
    if command_type in self.arithmetic:
      self._arithmetic(command_type)
    else:  # push or pop
      self._push_pop(line)

  def _arithmetic(self, command):
    if command == 'neg':
      neg_num = -self.rampop()
      self.rampush('constant', neg_num)
    elif command == 'not':
      not_num = not self.rampop()
      self.rampush('constant', not_num)
    else:

      num_y = self.rampop()
      num_x = self.rampop()

      if num_x is None or num_y is None:
        print('something is wrong with write_arithmetic')

      if command == 'add':
        self.rampush('constant', num_x + num_y)
      elif command == 'sub':
        self.rampush('constant', num_x - num_y)
      elif command == 'eq':
        temp = bool(num_x == num_y)  # currently False False return False
        self.rampush('constant', temp)
      elif command == 'gt':
        temp = bool(num_x > num_y)
        self.rampush('constant', temp)
      elif command == 'lt':
        temp = bool(num_x < num_y)
        self.rampush('constant', temp)
      elif command == 'and':
        temp = bool(num_x and num_y)
        self.rampush('constant', temp)
      elif command == 'or':
        temp = bool(num_x or num_y)
        self.rampush('constant', temp)

  def _push_pop(self, line):
    command_type = line[0]
    line[2] = int(line[2])
    if command_type == 'push':

      if line[1] == 'pointer':
        if line[2] == 0:
          self.rampush('constant', self.ram[3])
        if line[2] == 1:
          self.rampush('constant', self.ram[4])
      else:
        self.rampush(line[1], line[2])
    else:  # command_type == 'pop'
      pop_value = self.rampop()
      if line[1] == 'pointer':
        if line[2] == 0:
          self.set_segment_addr('this', pop_value)
          self.ram[3] = pop_value
        if line[2] == 1:
          self.set_segment_addr('that', pop_value)
          self.ram[4] = pop_value
      else:
        self.set_segment_value(line[1], line[2], pop_value)


if __name__ == '__main__':

  ram = Ram()

  ### push constant 10 ###
  ram.process_line(['push', 'constant', 10])
  ram.process_line(['push', 'constant', 123])
  ram.process_line(['push', 'constant', 5000])
  assert ram[256] == 10
  assert ram[257] == 123
  assert ram[258] == 5000

  ### pop local 1 ###
  ram.process_line(['pop', 'local', 1])
  ram.process_line(['pop', 'local', 2])
  assert ram[301] == 5000
  assert ram[302] == 123

  assert ram[256] == 10
  assert ram[257] == 123
  assert ram[258] == 5000

  ram.process_line(['push', 'constant', 4999])
  assert ram[256] == 10
  assert ram[257] == 4999
  assert ram[258] == 5000
  ram.process_line(['push', 'constant', 5001])
  assert ram[256] == 10
  assert ram[257] == 4999
  assert ram[258] == 5001  # 259

  ### pop this 6
  ram.process_line(['pop', 'this', 6])
  assert ram[3006] == 5001

  ### push this 6
  ram.process_line(['push', 'this', 6])
  assert ram[258] == 5001

  ### pop temp 0
  ram.process_line(['pop', 'temp', 0])
  assert ram[5] == 5001
  assert ram[256] == 10
  assert ram[257] == 4999
  assert ram[258] == 5001

  ### pop pointer 0
  ram.process_line(['pop', 'pointer', 0])
  assert ram.this_addr == 4999
  assert ram.get_segment_addr('this', 6) == 5005
  assert ram[3] == 4999
  assert ram[256] == 10
  assert ram[257] == 4999
  assert ram[258] == 5001

  ### push constant 77
  ram.process_line(['push', 'constant', 77])
  assert ram[256] == 10
  assert ram[257] == 77
  assert ram[258] == 5001
  assert ram.sp_addr == 258

  ### push constant 33
  ### pop pointer 0
  ### push pointer 0
  ram.process_line(['push', 'constant', 33])
  ram.process_line(['pop', 'pointer', 0])  # this_addr = 33
  assert ram.this_addr == 33
  ram.process_line(['push', 'pointer', 0])

  ram.process_line(['push', 'constant', 50])
  ram.process_line(['pop', 'this', 0])  # ram[this_addr] = 50
  print(ram.get_segment_value('this', 0))
  assert ram[33] == 50
  # print(ram.get_segment_value('pointer', 0))
  # print(ram.sp_addr)
  assert ram[256] == 10
  assert ram[257] == 77
  assert ram.sp_addr == 259

  ram.process_line((['add']))
  assert ram[257] == 110

  ram.process_line((['add']))
  assert ram[256] == 120

  ram.process_line(['push', 'constant', 1])
  ram.process_line(['push', 'constant', 2])
  ram.process_line(['push', 'constant', 3])
  ram.process_line(['push', 'constant', 4])
  ram.process_line(['push', 'constant', 5])
  ram.process_line(['push', 'constant', 6])
  assert ram[256] == 120
  assert ram[257] == 1
  assert ram[258] == 2
  assert ram[259] == 3
  assert ram[260] == 4
  assert ram[261] == 5
  assert ram[262] == 6

  ram.process_line((['sub']))
  # print(ram[259])
  # print(ram[260])
  # print(ram[261])
  assert ram[260] == 4
  assert ram[261] == -1  # sp_addr = 262
  assert ram[262] == 6

  ram.process_line((['eq']))
  assert ram[260] == False  # sp_addr = 261

  ram.process_line((['gt']))  # 2, 3  # sp_addr = 259
  assert ram[258] == False

  ram.process_line(['pop', 'pointer', 1])  # sp_addr = 258
  assert ram[3010] == False

  ram.process_line(['push', 'pointer', 0])  # sp_addr = 259
  assert ram[258] == False
  ram.process_line(['push', 'pointer', 1])  # sp_addr = 260
  assert ram[259] == False

  ram.process_line(['push', 'constant', 50])
  ram.process_line(['push', 'constant', 50])
  assert ram[ram.sp_addr - 1] == 50
  ram.process_line((['gt']))  # 2, 3  # sp_addr = 259
  assert ram[ram.sp_addr - 1] == False
  ram.process_line(['push', 'constant', 48])
  ram.process_line(['push', 'constant', 50])
  ram.process_line((['lt']))  # 2, 3  # sp_addr = 259
  assert ram[ram.sp_addr - 1] == True

  ram.process_line(['push', 'constant', 48])
  ram.process_line(['push', 'constant', 50])
  ram.process_line((['lt']))  # 2, 3  # sp_addr = 259
  assert ram[ram.sp_addr - 1] == True
  ram.process_line((['and']))  # 2, 3  # sp_addr = 259
  assert ram[ram.sp_addr - 1] == True

  ram.process_line(['push', 'constant', 48])
  ram.process_line(['push', 'constant', 50])
  ram.process_line((['gt']))  # 2, 3  # sp_addr = 259
  ram.process_line((['or']))  # 2, 3  # sp_addr = 259
  assert ram[ram.sp_addr - 1] == True
