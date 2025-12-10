import dataclasses
import itertools
import sys


@dataclasses.dataclass(order=True)
class Point:
    x: int
    y: int


def area(u: Point, v: Point) -> int:
    return (abs(u.x - v.x) + 1) * (abs(u.y - v.y) + 1)


def bound(value: int, min_value: int, max_value: int) -> int:
    if value < min_value:
        return min_value
    if value > max_value:
        return max_value
    return value


def main() -> None:
    fname = sys.argv[1]
    points = list[Point]()
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            x, y = map(int, line.split(","))
            points.append(Point(x, y))
    pairs = list(itertools.combinations(points, 2))
    ans1 = max(map(lambda p: area(p[0], p[1]), pairs))
    print(f"ans1 = {ans1}")

    ans2 = 0
    for u, v in pairs:
        candidate = area(u, v)
        if candidate <= ans2:
            continue
        xmin, xmax = sorted([u.x, v.x])
        ymin, ymax = sorted([u.y, v.y])
        prev_point = Point(
            bound(points[-1].x, xmin, xmax), bound(points[-1].y, ymin, ymax)
        )
        sa = 0
        for w in points:
            new_x = bound(w.x, xmin, xmax)
            new_y = bound(w.y, ymin, ymax)
            new_point = Point(new_x, new_y)
            if new_point == prev_point:
                continue
            sa += (prev_point.y + new_point.y) * (prev_point.x - new_point.x)
            prev_point = new_point
        if sa == 0 or sa != 2 * abs(u.x - v.x) * abs(u.y - v.y):
            continue
        ans2 = candidate
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
