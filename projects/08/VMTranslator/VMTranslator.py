import sys, os
from vm_parser import VMParser
from vm_codewriter import CodeWriter

if __name__ == '__main__':
  # vm_file = sys.argv[1]
  # asm_file = os.path.splitext(vm_file)[0] + '.asm'
  # lines = VMParser(sys.argv[1]).get_commands()

  vm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement/Sys.vm'
  # vm_file2 = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement/Main.vm'
  asm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement/FibonacciElement.asm'

  # vm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/Sys.vm'
  # asm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/NestedCall.asm'
  # vm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm'
  # asm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.asm'
  # from pathlib import Path
  # temp = Path(asm_file).parent
  # print(str(temp))

  # vm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/Sys.vm'
  # vm_file2 = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/Class1.vm'
  # vm_file3 = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/Class2.vm'
  # asm_file = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/StaticsTest.asm'

# Returns a Pathlib object

  lines = VMParser(vm_file).get_commands()
  # lines.extend(VMParser(vm_file2).get_commands())
  # lines.extend(VMParser(vm_file3).get_commands())
  CodeWriter(asm_file, lines)

  # print(lines)
  # for line in lines:
    # print(line)

    # func_path = '{}/{}.vm'.format(str(Path(self.output_file).parent), (line[1].split(sep='.')[0]))
    # # print(func_path)
    # func_lines = VMParser(func_path).get_commands()
    # # print(func_lines)
    # for func_line in func_lines:
    #   self.write_line(func_line)
