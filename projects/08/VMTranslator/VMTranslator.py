import sys, os
from vm_parser import VMParser
from vm_codewriter import CodeWriter
from pathlib import Path

def translate_dir(input_path, debug_flag=False):
    # make vm_files list
    vm_files = list()
    for subdir, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(".vm"):

                file_path = input_path + '/' + str(file)
                if file == 'Sys.vm':
                    vm_files.insert(0, file_path)
                else:
                    vm_files.append(file_path)

    p_path = str(Path(vm_files[0]).parent)
    asm_file_name = p_path.split(sep='/')[-1] + '.asm'
    asm_file_path = p_path + '/' + asm_file_name
    print(f'asm_file path: {asm_file_path}')

    if os.path.exists(asm_file_path):
        os.remove(asm_file_path)

    # append assembly code file by file
    debug_lines = []
    call_cnt = 0

    for idx, vm_file in enumerate(vm_files):
        vm_lines = []
        if idx == 0:
            vm_lines.append(['call', 'Sys.init', 0])

        vm_lines.extend(VMParser(vm_file).get_commands())
        temp_name = os.path.splitext(vm_file)[0].split(sep='/')[-1]
        cw = CodeWriter(
            temp_name, asm_file_path, vm_lines, num_call=call_cnt, operation='a', debug=debug_flag
        )
        num_calls = len(list(filter(lambda line: line[0] == 'call', vm_lines)))
        call_cnt += num_calls

        debug_lines.extend(cw.get_debug_lines())

    if debug_flag == True:
        label_cnt = 0
        for idx, debug_line in enumerate(debug_lines):
            if type(debug_line) == list:
                print('\t\t<vm: {}>'.format(' '.join(debug_line)))
                label_cnt += 1
            else:
                if debug_line.startswith('('):
                    print('lcnt: {}\t{}'.format(idx - label_cnt, debug_line))
                    label_cnt += 1
                else:
                    print('lcnt: {}\t{}'.format(idx - label_cnt, debug_line))




def translate_file(input_path, debug_flag=False):
    p_path = str(Path(input_path).parent)
    asm_file_name = p_path.split(sep='/')[-1] + '.asm'
    asm_file_path = p_path + '/' + asm_file_name

    vm_lines = list()
    vm_lines.extend(VMParser(input_path).get_commands())

    is_sys = False
    for vm_line in vm_lines:
        if vm_line[0] == 'function' and vm_line[1] == "Sys.init":
            is_sys = True
            break
    if is_sys:
        vm_lines.insert(0, ['call', 'Sys.init', 0])

    # file = open(asm_file_path, "w")
    # file.close()
    if os.path.exists(asm_file_path):
        os.remove(asm_file_path)

    temp_name = os.path.splitext(input_path)[0].split(sep='/')[-1]
    CodeWriter(temp_name, asm_file_path, vm_lines, num_call=0, operation='a', debug=debug_flag)




def translate(input_path, debug_flag=False):

    if os.path.isdir(input_path):
        print("\tinput is a dir")
        translate_dir(input_path, debug_flag)

    elif os.path.isfile(input_path):
        print("\tinput is a file")
        translate_file(input_path, debug_flag)

    else:
        print("Not a file or dir")




if __name__ == '__main__':

    input_path = sys.argv[1]
    translate(input_path, debug_flag=False)
