import functools
import itertools
import sys
from collections.abc import Iterable

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp  # type: ignore


def powerset[T](iterable: Iterable[T]) -> Iterable[tuple[T, ...]]:
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )


def main() -> None:
    fname = sys.argv[1]
    ans1 = 0
    ans2 = 0
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            target_raw, *buttons_raw, joltage_raw = line.split()

            target_parts = target_raw.strip("[]")
            total_indicators = len(target_parts)
            target = np.zeros(total_indicators)
            target_binary = 0
            mask = 1
            for ix, c in enumerate(target_parts):
                if c == "#":
                    target[ix] = 1
                    target_binary |= mask
                mask *= 2

            total_buttons = len(buttons_raw)
            buttons = np.zeros((total_indicators, total_buttons))
            buttons_binary = list[int]()
            for button_id, button_raw in enumerate(buttons_raw):
                button_binary = 0
                for pos_raw in button_raw.strip("()").split(","):
                    pos = int(pos_raw)
                    buttons[pos][button_id] = 1
                    button_binary |= 1 << pos
                buttons_binary.append(button_binary)

            joltage_parts = joltage_raw.strip("{}").split(",")
            assert len(joltage_parts) == total_indicators
            joltage = np.zeros(total_indicators)
            for ix, value in enumerate(joltage_parts):
                joltage[ix] = int(value)

            total_presses1 = None
            # can also write an ILP
            for subset in powerset(buttons_binary):
                result = functools.reduce(lambda x, y: x ^ y, subset, 0)
                if result == target_binary:
                    total_presses1 = len(subset)
                    break
            assert total_presses1 is not None
            ans1 += total_presses1

            c = np.ones(total_buttons)
            presses2 = milp(
                c=c,
                constraints=LinearConstraint(buttons, lb=joltage, ub=joltage),  # type: ignore
                bounds=Bounds(lb=0),
                integrality=c,
            )
            total_presses2 = int(presses2.fun)  # type: ignore
            ans2 += total_presses2

    print(f"ans1 = {ans1}")
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
