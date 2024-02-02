import sys
from fixed_point_class import *
from floating_point_class import *


def solve(inputs: list[str]):
    if len(inputs) not in [3, 5]:
        print("3 or 5 arguments expected, but", len(inputs), "given", file=sys.stderr)
        return
    if inputs[0] != 'h' and inputs[0] != 'f':
        if inputs[0].count('.') != 1 or int(inputs[0].split('.')[0]) <= 0 or int(inputs[0].split('.')[1]) < 0 or int(inputs[0].split('.')[0]) + int(inputs[0].split('.')[1]) > 32:
            print("Incorrect first argument\nExpected h, f or A.B (where A, B are integers, A+B<=32, A>=1) in the first_argument", file=sys.stderr)
            return
    if len(inputs) == 3:
        inputs[2] = inputs[2].upper()
        if not check_for_valid_hex(inputs[2]):
            print(inputs[2], "is not valid hex input", file=sys.stderr)
            return
        if inputs[0] == 'h' or inputs[0] == 'f':
            code = hex2binary_code(inputs[2])
            rounding = int(inputs[1])
            print(FloatNum(code, rounding, inputs[0] == 'f'))
        else:
            assert inputs[0].count('.') == 1
            A, B = map(int, inputs[0].split('.'))
            rounding = int(inputs[1])
            print(FixedPointNum(A, B, hex2binary_code(inputs[2]), rounding))
    elif len(inputs) == 5:
        if inputs[3] not in "+-/*":
            print("Incorrect input: Operation should be +,-,* or /, but got " + inputs[3], file=sys.stderr)
            return
        if not check_for_valid_hex(inputs[2]):
            print(inputs[2], "is not valid hex input", file=sys.stderr)
            return
        if not check_for_valid_hex(inputs[4]):
            print(inputs[4], "is not valid hex input", file=sys.stderr)
            return
        inputs[2] = inputs[2].upper()
        inputs[4] = inputs[4].upper()
        if inputs[0] == 'h' or inputs[0] == 'f':
            rounding = int(inputs[1])
            num1 = FloatNum(hex2binary_code(inputs[2]), rounding, inputs[0] == 'f')
            num2 = FloatNum(hex2binary_code(inputs[4]), rounding, inputs[0] == 'f')
        else:
            assert str(inputs[0]).count('.') == 1
            A, B = map(int, inputs[0].split('.'))
            rounding = int(inputs[1])
            num1 = FixedPointNum(A, B, hex2binary_code(inputs[2]), rounding)
            num2 = FixedPointNum(A, B, hex2binary_code(inputs[4]), rounding)
        ans = None
        if inputs[3] == '+':
            ans = (num1 + num2)
        elif inputs[3] == '-':
            ans = (num1 - num2)
        elif inputs[3] == '*':
            ans = (num1 * num2)
        elif inputs[3] == '/':
            ans = (num1 / num2)
        if ans is not None:
            print(ans)


if __name__ == '__main__':
    solve(sys.argv[1:])


