import sys, os
from vm_parser import VMParser
from vm_codewriter import CodeWriter

if __name__ == '__main__':
  vm_file = sys.argv[1]
  asm_file = os.path.splitext(vm_file)[0] + '.asm'
  lines = VMParser(sys.argv[1]).get_commands()
  CodeWriter(asm_file, lines)
