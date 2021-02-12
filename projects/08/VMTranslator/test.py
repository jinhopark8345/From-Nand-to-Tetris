import subprocess


def run_test(home_path):
    test_list = [
        (
            home_path
            + "/Projects/FromNandToTetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.vm",
            home_path
            + "/Projects/FromNandToTetris/projects/08/ProgramFlow/BasicLoop/BasicLoop.tst",
        ),
        (
            home_path
            + "/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.vm",
            home_path
            + "/Projects/FromNandToTetris/projects/08/ProgramFlow/FibonacciSeries/FibonacciSeries.tst",
        ),
        (
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/SimpleFunction/SimpleFunction.vm",
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/SimpleFunction/SimpleFunction.tst",
        ),
        (
            "../FunctionCalls/NestedCall",
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/NestedCall.tst",
        ),
        (
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/Sys.vm",
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/NestedCall/NestedCall.tst",
        ),
        (
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement",
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/FibonacciElement/FibonacciElement.tst",
        ),
        (
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest",
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/StaticsTest.tst",
        ),
        (
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/",
            home_path
            + "/Projects/FromNandToTetris/projects/08/FunctionCalls/StaticsTest/StaticsTest.tst",
        ),
    ]

    cnt = 0
    # for i in range(0, 1):
    for i in range(len(test_list)):
        dirorfile = test_list[i][0]
        test_path = test_list[i][1]

        translator_path = (
            home_path
            + "/Projects/FromNandToTetris/projects/08/VMTranslator/VMTranslator.py"
        )

        cpu_emulator_path = (
            home_path + "/Projects/FromNandToTetris/tools/CPUEmulator.sh"
        )

        translate_result = subprocess.run(
            [
                "python3",
                translator_path,
                dirorfile,
            ],
            capture_output=True,
        )
        test_result = subprocess.run(
            [cpu_emulator_path, test_path],
            capture_output=True,
            text=True,
        )

        if (
            not test_result.stdout.strip()
            == "End of script - Comparison ended successfully"
        ):
            print("fail: {}".format(dirorfile))
            print(test_result.stderr)
            # print("test fail")
            # print("dirorfile: ", dirorfile)
            # print("test_path: ", test_path)
            print(
                "\n".join(
                    [
                        output_line.decode("ascii")
                        for output_line in translate_result.stdout.split(b"\n")
                    ]
                )
            )


        else:
            print("pass: {}".format(dirorfile))


if __name__ == "__main__":
    import os

    home_path = os.environ.get("HOME")
    run_test(home_path)
