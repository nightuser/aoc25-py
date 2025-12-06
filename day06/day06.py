import enum
import functools
import operator
import sys
from collections.abc import Iterable


class Operation(enum.StrEnum):
    PLUS = "+"
    MUL = "*"


def prod(iterable: Iterable[int], initial: int = 1) -> int:
    return functools.reduce(operator.mul, iterable, initial)


def main() -> None:
    fname = sys.argv[1]
    with open(fname) as fh:
        line = fh.readline().strip()
        problems = [[int(x)] for x in line.split()]
        operations = None
        for line in fh:
            line = line.strip()
            if line[0] == "*" or line[0] == "+":
                operations = [Operation(op) for op in line.split()]
            else:
                for x, problem in zip(line.split(), problems, strict=True):
                    problem.append(int(x))
    assert operations is not None
    ans1 = 0
    for operation, problem in zip(operations, problems):
        match operation:
            case Operation.PLUS:
                result = sum(problem)
            case Operation.MUL:
                result = prod(problem)
        ans1 += result
    print(f"ans1 = {ans1}")

    width = None
    height = 0
    lines = list[str]()
    with open(fname) as fh:
        for line in fh:
            height += 1
            line = line.rstrip("\n")
            if width is None:
                width = len(line)
            else:
                assert len(line) == width
            lines.append(line)

    transposed = [[" " for _ in range(height)] for _ in range(width)]
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            transposed[x][y] = c
    ans2 = 0
    result = 0
    current_op = None
    for line in transposed:
        line = "".join(line).strip()
        if not line:
            ans2 += result
            current_op = None
            result = 0
            continue
        if current_op is None:
            current_op = Operation(line[-1])
            result = int(line[:-1])
        else:
            x = int(line)
            match current_op:
                case Operation.PLUS:
                    result += x
                case Operation.MUL:
                    result *= x
    if current_op is not None:
        ans2 += result
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
