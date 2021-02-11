import sys


def run_test():
  test_list = [
      (
          '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.vm',
          '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.tst',
      ),
      (
          '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm',
          '/home/jinho/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.tst',
      ),
      (
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/SimpleFunction/SimpleFunction.vm',
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/SimpleFunction/SimpleFunction.tst',
      ),
      (
          '../FunctionCalls/NestedCall',
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/NestedCall.tst'
      ),
      (
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/Sys.vm',
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/NestedCall.tst',
      ),
      (
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement',
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement/FibonacciElement.tst',
      ),
      (
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest',
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/StaticsTest.tst',
      ),
      (
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/',
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/StaticsTest.tst',
      ),
  ]

  import subprocess

  cnt = 0
  # for i in range(0, 1):
  for i in range(len(test_list)):
    print()
    dirorfile = test_list[i][0]
    test_path = test_list[i][1]
    print("dirorfile: ", dirorfile)
    print("test_path: ", test_path)

    output = subprocess.run([
        "python3", "/home/jinho/Projects/FromNandToTetris/projects/08/VMTranslator/VMTranslator.py",
        dirorfile
    ],
                            capture_output=True)

    print('\n'.join([output_line.decode('ascii') for output_line in output.stdout.split(b'\n')]))

    subprocess.run(["/home/jinho/Projects/FromNandToTetris/tools/CPUEmulator.sh", test_path])


run_test()
