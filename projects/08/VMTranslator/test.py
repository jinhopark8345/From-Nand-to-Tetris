
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
          '/home/jinho/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/NestedCall.vm',
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
  ]

  import subprocess
  # output = subprocess.call(["cmd", "--thing", "foo", "--stuff", "bar", "-a", "b", "input", "output"])
  # list_files = subprocess.run(["ls", "-l"], stdout=subprocess.DEVNULL)
  # result = subprocess.run([sys.executable, "-c", "print('ocean')"])

  cnt = 0
  for dirorfile, test_path in test_list:
    if cnt == 6:
      break
    cnt += 1

    print("dirorfile: ",dirorfile)
    print("test_path: ",test_path)

    output_msg = ""

    output_msg =  subprocess.run(["python3", "/home/jinho/Projects/FromNandToTetris/projects/08/VMTranslator/VMTranslator.py", dirorfile], capture_output=True)

    print(output_msg)
    subprocess.run(["/home/jinho/Projects/FromNandToTetris/tools/CPUEmulator.sh", test_path], capture_output=True)
    print(output_msg)
    # print("dirorfile: ", dirorfile)
    # print("test_path: ", test_path)

run_test()
