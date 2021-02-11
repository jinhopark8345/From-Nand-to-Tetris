import sys, os
from vm_parser import VMParser
from vm_codewriter import CodeWriter
from pathlib import Path


def translate(input_path):
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

    f_name = str(p_path)[len(str(pp_path)) + 1:]  # f_name is wrong
    file_name = str(p_path)[len(str(pp_path)) + 1:] + '.asm'
    asm_file_path = str(p_path) + '/' + file_name
    print(f'asm_file path: {asm_file_path}')

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

    p_path = str(Path(input_path).parent)
    asm_file_name = p_path.split(sep='/')[-1] + '.asm'
    asm_file_path = p_path + '/' + asm_file_name

    vm_lines = VMParser(input_path).get_commands()
    file = open(asm_file_path, "w")
    file.close()
    temp_name = os.path.splitext(input_path)[0].split(sep='/')[-1]
    CodeWriter(temp_name, asm_file_path, vm_lines, operation='a')

  else:
    print("Not a file or dir")




if __name__ == '__main__':

  # asm_file = os.path.splitext(vm_file)[0] + '.asm'
  # lines = VMParser(sys.argv[1]).get_commands()

  # single file test
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/SimpleFunction/SimpleFunction.vm'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.vm'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/Sys.vm'

  # dir test
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest'
  # input_path = '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/SimpleFunction'

  # input_path = sys.argv[1]
  # translate(input_path)

  input_path = sys.argv[1]
  translate(input_path)
