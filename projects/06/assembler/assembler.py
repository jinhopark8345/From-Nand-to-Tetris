# import fileinput
# for line in fileinput.FileInput("file",inplace=1):
#     if line.rstrip():
#         print line

import sys
import re

# comp2bits
# dest2bits
# jump2bits
comp2bits = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'A+D': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'M+D': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}

dest2bits = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111',
}

jump2bits = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}

# *warning*: has integer value
symboltable = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
}

label2linenum = {}

linenum = 0
varnum = 16


def first_pass(line):
  """
  handle labels
  """

  global linenum

  if line.startswith('('):
    curlabel = line.strip(')(')
    symboltable[curlabel] = linenum
    # subtract 1 because it took one line from the code and this line is just for reference
    linenum -= 1
  linenum += 1


def second_pass(line):
  """
  handle symbols and variables
  """

  global varnum
  # print(line)
  if line.startswith('@'):
    var = line[1:]

    # print(var)
    # if var.isdigit():
    #   print("this is digit: " + var)
    if var not in symboltable and not var.isdigit():
      # print(var)
      symboltable[var] = varnum
      varnum += 1




def third_pass(line):
  # A instruction
  if line.startswith("@"):
    # get the number
    var = line[1:]

    if var.isdigit():
      curnum = int(var)
      # convert integer to binary
      curbinum = f'{curnum:015b}'
      # add 1 to the start of the string to indicate A instruction
      curbline = '0' + curbinum
    else:
      curnum = symboltable[var]
      curbinum = f'{curnum:015b}'
      # add 1 to the start of the string to indicate A instruction
      curbline = '0' + curbinum


    print(curbline)

  # C instruction
  else:
    # print(line,end="")

    headbin = '111'
    compbin = ''
    destbin = ''
    jumpbin = ''

    sepidx = line.find('=')
    sepidx2 = line.find(';')

    # case like D=M
    if sepidx != -1:
      dest = line[:sepidx].rstrip('\r\n')
      comp = line[sepidx + 1:].rstrip('\r\n')

      compbin = comp2bits[comp]
      destbin = dest2bits[dest]
      jumpbin = '000'
      curbline = headbin + compbin + destbin + jumpbin
      print(curbline)
      # print('before: {}, after: {}'.format(line, curbline))

    # case like 0;JMP
    if sepidx2 != -1:
      comp = line[:sepidx2].rstrip('\r\n')
      jump = line[sepidx2 + 1:].rstrip('\r\n')

      compbin = comp2bits[comp]
      destbin = '000'
      jumpbin = jump2bits[jump]
      curbline = headbin + compbin + destbin + jumpbin
      # print('before: {}, after: {}'.format(line, curbline))
      print(curbline)


def main():
  filelist = [
      "../add/Add.asm",  # 0
      '../max/MaxL.asm',  # 1
      '../pong/PongL.asm',  #2
      '../rect/RectL.asm',  #3
      '../max/Max.asm',  #4
      '../pong/Pong.asm',  #5
      '../rect/Rect.asm',  #6
  ]
  # sys.argv[1] = '../add/Add.asm'
  # with open(sys.argv[1], 'r') as file:

  print()

  # curfile = filelist[6]
  curfile = "/home/jinho/Projects/study/From-Nand-to-Tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.asm"

  with open(curfile, 'r') as file:

    for line in file:
      if not line.isspace() and not line.startswith('/'):
        idx = line.find('/')
        if idx != -1:
          line = line[:idx]
        line = line.rstrip('\r\n').strip()

        first_pass(line)

  with open(curfile, 'r') as file:
    for line in file:
      if not line.isspace() and not line.startswith('/'):
        idx = line.find('/')
        if idx != -1:
          line = line[:idx]
        line = line.rstrip('\r\n').strip()
        second_pass(line)

  with open(curfile, 'r') as file:
    for line in file:
      if not line.isspace() and not line.startswith('/') and not line.startswith('('):
        idx = line.find('/')
        if idx != -1:
          line = line[:idx]
        line = line.rstrip('\r\n').strip()
        # print(line)
        third_pass(line)

  # print(symboltable)


main()
