import sys, os
from vm_parser import VMParser
from vm_codewriter import CodeWriter

if __name__ == '__main__':
  # vm_file = sys.argv[1]
  # asm_file = os.path.splitext(vm_file)[0] + '.asm'
  # lines = VMParser(sys.argv[1]).get_commands()

  vm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.vm'
  asm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.asm'

  # vm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm'
  # asm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.asm'


  lines = VMParser(vm_file).get_commands()

  # print(lines)
  # for line in lines:
    # print(line)
  CodeWriter(asm_file, lines)
