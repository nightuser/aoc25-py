import sys
from collections.abc import Iterable

Bank = list[int]


def solve(banks: Iterable[Bank], total_batteries: int) -> int:
    result = 0
    for bank in banks:
        best = Bank()
        joltage = None
        for b in bank:
            best.append(b)
            if len(best) < total_batteries:
                continue
            found = False
            joltage = 0
            for i in range(total_batteries):
                if found:
                    best[i] = best[i+1]
                elif best[i] < best[i + 1]:
                    best[i] = best[i+1]
                    found = True
                joltage = 10 * joltage + best[i]
            best.pop()
        assert joltage is not None
        result += joltage
    return result


def main() -> None:
    fname = sys.argv[1]
    banks = list[Bank]()
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            bank = [int(c) for c in line]
            banks.append(bank)

    ans1 = solve(banks, 2)
    print(f"ans1 = {ans1}")
    ans2 = solve(banks, 12)
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
