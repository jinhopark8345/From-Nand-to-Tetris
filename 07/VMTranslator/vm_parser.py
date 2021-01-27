""" Parser
parses each VM command into its lexical elements """

import re


class VMParser:
  def __init__(self, input_vm_file):
    self.lines = []
    print("input file name: {}".format(input_vm_file))
    f = open(input_vm_file, 'r')

    while True:
      line = f.readline()

      cur_line = line.strip()
      trimmed = re.sub(r'[\/]{2}.*', '', cur_line)

      if trimmed != '':
        trimmed = trimmed.split()
        self.lines.append(trimmed)

      if not line:
        break
    f.close()

  def get_commands(self):
    return self.lines
