import sys

Point = tuple[int, int]

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def main() -> None:
    fname = sys.argv[1]

    rolls = dict[Point, int]()

    with open(fname) as fh:
        for y, line in enumerate(fh):
            line = line.rstrip()
            for x, c in enumerate(line):
                if c == "@":
                    rolls[(x, y)] = 0

    accessible_points = set[Point]()
    for point in rolls:
        x, y = point
        neighbors = [(x + dx, y + dy) for dx, dy in DIRS if (x + dx, y + dy) in rolls]
        rolls[point] = len(neighbors)
        if len(neighbors) < 4:
            accessible_points.add(point)
    ans1 = len(accessible_points)
    print(f"ans1 = {ans1}")

    ans2 = 0
    while accessible_points:
        point = accessible_points.pop()
        x, y = point
        ans2 += 1
        del rolls[point]
        neighbors = [(x + dx, y + dy) for dx, dy in DIRS if (x + dx, y + dy) in rolls]
        for neighbor in neighbors:
            rolls[neighbor] -= 1
            if rolls[neighbor] < 4:
                accessible_points.add(neighbor)
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
