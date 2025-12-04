import sys

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def main() -> None:
    fname = sys.argv[1]
    width = None
    height = 0
    inner_grid = list[list[bool]]()
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            if width is None:
                width = len(line)
            height += 1

            row = [False] + [c == "@" for c in line] + [False]
            inner_grid.append(row)

    assert width is not None
    empty_row = [False] * (width + 2)
    grid = [empty_row] + inner_grid + [empty_row]

    ans1 = 0
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            if not grid[y][x]:
                continue
            around = sum(grid[y + dy][x + dx] for dx, dy in DIRS)
            if around < 4:
                ans1 += 1
    print(f"ans1 = {ans1}")

    ans2 = 0
    while True:
        to_be_removed = list[tuple[int, int]]()
        for y in range(1, height + 1):
            for x in range(1, width + 1):
                if not grid[y][x]:
                    continue
                around = sum(grid[y + dy][x + dx] for dx, dy in DIRS)
                if around < 4:
                    to_be_removed.append((x, y))
        if not to_be_removed:
            break
        ans2 += len(to_be_removed)
        for x, y in to_be_removed:
            grid[y][x] = False
    print(f"ans1 = {ans2}")


if __name__ == "__main__":
    main()
