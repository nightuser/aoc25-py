import sys
from collections.abc import Iterable

TOTAL_BATTERIES = 12


def argmax[T](xs: Iterable[T]) -> tuple[int, T]:
    return max(enumerate(xs), key=lambda ix: (ix[1], -ix[0]))


def main() -> None:
    fname = sys.argv[1]
    banks = list[tuple[int, ...]]()
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            bank = tuple(int(c) for c in line)
            banks.append(bank)

    ans1 = 0
    for bank in banks:
        bat1_index, bat1_value = argmax(bank[:-1])
        bat2_value = max(bank[bat1_index + 1 :])
        joltage = bat1_value * 10 + bat2_value
        ans1 += joltage

    ans2 = 0
    for bank in banks:
        batteries = list[int]()
        start_index = 0
        end_index = len(bank) + 1 - TOTAL_BATTERIES
        for _ in range(TOTAL_BATTERIES):
            bat_index, bat_value = argmax(bank[start_index:end_index])
            batteries.append(bat_value)
            start_index += bat_index + 1
            end_index += 1
        joltage = 0
        for bat_value in batteries:
            joltage = 10 * joltage + bat_value
        ans2 += joltage

    print(f"ans1 = {ans1}")
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
