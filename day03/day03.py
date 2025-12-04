import dataclasses
import sys
from collections.abc import Sized

TOTAL_BATTERIES = 12


@dataclasses.dataclass
class Node:
    index: int
    value: int


def node_key(node: Node):
    return (node.value, -node.index)


def node_max(first: Node, second: Node):
    return max(first, second, key=node_key)


class SegmentTree(Sized):
    def __init__(self, bank: str):
        self._total_bats = len(bank)
        self._tree = [Node(0, 0) for _ in range(self._total_bats)]
        for bat_index, bat_value in enumerate(bank):
            self._tree.append(Node(bat_index, int(bat_value)))
        for node_index in range(self._total_bats - 1, 0, -1):
            self._tree[node_index] = node_max(
                self._tree[2 * node_index], self._tree[2 * node_index + 1]
            )

    def max(self, left: int, right: int) -> Node:
        left += self._total_bats
        right += self._total_bats
        result = Node(0, 0)
        while left < right:
            if left & 1 == 1:
                result = node_max(result, self._tree[left])
                left += 1
            if right & 1 == 1:
                right -= 1
                result = node_max(result, self._tree[right])
            left >>= 1
            right >>= 1
        return result

    def __len__(self) -> int:
        return self._total_bats


def main() -> None:
    fname = sys.argv[1]
    banks = list[SegmentTree]()
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            bank = SegmentTree(line)
            banks.append(bank)

    ans1 = 0
    for bank in banks:
        bat1 = bank.max(0, len(bank) - 1)
        bat2 = bank.max(bat1.index + 1, len(bank))
        joltage = bat1.value * 10 + bat2.value
        ans1 += joltage
    print(f"ans1 = {ans1}")

    ans2 = 0
    for bank in banks:
        joltage = 0
        start_index = 0
        end_index = len(bank) + 1 - TOTAL_BATTERIES
        for _ in range(TOTAL_BATTERIES):
            bat = bank.max(start_index, end_index)
            joltage = 10 * joltage + bat.value
            start_index = bat.index + 1
            end_index += 1
        ans2 += joltage
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
