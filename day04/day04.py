import dataclasses
import sys

Point = tuple[int, int]


@dataclasses.dataclass
class NeighborData:
    count: int
    mask: int


"""
For every index `i`, DIRS[i] == -DIRS[7-i].
"""
DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def main() -> None:
    fname = sys.argv[1]

    rolls = dict[Point, NeighborData]()

    with open(fname) as fh:
        for y, line in enumerate(fh):
            line = line.rstrip()
            for x, c in enumerate(line):
                if c == "@":
                    rolls[(x, y)] = NeighborData(0, 0)

    accessible_points = list[Point]()
    for point in rolls:
        x, y = point
        record = rolls[point]
        mask = 1
        for dx, dy in DIRS:
            if (x + dx, y + dy) in rolls:
                record.count += 1
                record.mask |= mask
            mask <<= 1
        if record.count < 4:
            accessible_points.append(point)
    ans1 = len(accessible_points)
    print(f"ans1 = {ans1}")

    ans2 = 0
    while accessible_points:
        point = accessible_points.pop()
        x, y = point
        ans2 += 1
        neighbors_mask = rolls.pop(point).mask

        for dir_id, (dx, dy) in enumerate(DIRS):
            if neighbors_mask == 0:
                break
            if neighbors_mask & 1 == 1:
                neighbor = (x + dx, y + dy)
                neighbor_record = rolls[neighbor]
                neighbor_record.count -= 1
                neighbor_record.mask &= ~(1 << (len(DIRS) - dir_id - 1))
                if neighbor_record.count == 3:
                    accessible_points.append(neighbor)
            neighbors_mask >>= 1
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
