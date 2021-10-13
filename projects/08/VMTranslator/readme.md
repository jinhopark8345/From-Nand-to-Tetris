
* program flow
- .jack -> .vm (not implemented)
- .vm -> .asm
- .asm -> .hack

* How to use VMTranslator
e.g. BasicLoop.vm(hack virtual machine code) -> BasicLoop.asm(hack assembly code)

#+begin_src bash
python VMTranslator.py /home/jinho/Projects/study/From-Nand-to-Tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.vm
#+end_src
* how to use assembler

e.g. BasicLoop.asm(hack assembley code) -> BasicLoop.hack(only binary codes)

and this .hack file will be fed to hack CPU

** command example
 #+begin_src bash
# using provided assembler
/home/jinho/Projects/study/From-Nand-to-Tetris/tools/Assembler.sh /home/jinho/Projects/study/From-Nand-to-Tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.asm

# it just convert from assembly to .hack code, so no room for optimization
# using custom assembler / have to change input file manually & output will be streamed, won't be written to a file
python /home/jinho/Projects/study/From-Nand-to-Tetris/projects/06/assembler/assembler.py
 #+end_src

** file examples
#+begin_src bash
# BasicLoop.asm
    M=M+1
    @SP
    M=M-1
    A=M
    ...

# BasicLoop.hack
    0000000100000000
    1110110000010000
    0000000000000000
    1110001100001000
    ...
#+end_src
* how to use CPUEmulator
~.out~ will be generated in result.

#+begin_src bash
# in below case BasicLoop.out will be generated
/home/jinho/Projects/study/From-Nand-to-Tetris/tools/CPUEmulator.sh /home/jinho/Projects/study/From-Nand-to-Tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.tst
#+end_src
* etc
** .cmp
comes with the project for testing purpose

 e.g: /home/jinho/Projects/study/From-Nand-to-Tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.cmp
** .tst
comes with the project and used to run provided tools - testing script file

/home/jinho/Projects/study/From-Nand-to-Tetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.tst
/home/jinho/Projects/study/From-Nand-to-Tetris/projects/08/ProgramFlow/BasicLoop/BasicLoopVME.tst
