import sys

Point = tuple[int, int]

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def main() -> None:
    fname = sys.argv[1]

    rolls = set[Point]()

    with open(fname) as fh:
        for y, line in enumerate(fh):
            line = line.rstrip()
            for x, c in enumerate(line):
                if c == "@":
                    rolls.add((x, y))

    ans1 = 0
    for x, y in rolls:
        neighbors = [(x + dx, y + dy) for dx, dy in DIRS if (x + dx, y + dy) in rolls]
        if len(neighbors) < 4:
            ans1 += 1
    print(f"ans1 = {ans1}")

    ans2 = 0
    affected = rolls.copy()
    next_affected = set[Point]()
    while affected:
        while affected:
            p = affected.pop()
            if p not in rolls:
                continue
            x, y = p
            neighbors = [
                (x + dx, y + dy) for dx, dy in DIRS if (x + dx, y + dy) in rolls
            ]
            if len(neighbors) < 4:
                ans2 += 1
                next_affected.update(neighbors)
                rolls.remove(p)
        affected, next_affected = next_affected, affected
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
