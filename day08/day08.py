import dataclasses
import functools
import itertools
import sys


@dataclasses.dataclass
class Point:
    x: int
    y: int
    z: int


def dist(u: Point, v: Point) -> int:
    return (u.x - v.x) ** 2 + (u.y - v.y) ** 2 + (u.z - v.z) ** 2


class DSU:
    def __init__(self, total: int):
        self._total = total
        self._parent = list(range(total))
        self._size = [1] * total

    def find_set(self, index: int) -> int:
        parent = self._parent[index]
        if parent == index:
            return index
        representative = self.find_set(parent)
        self._parent[index] = representative
        return representative

    def union(self, index1: int, index2: int):
        representative1 = self.find_set(index1)
        representative2 = self.find_set(index2)
        if representative1 == representative2:
            return
        if self._size[representative1] < self._size[representative2]:
            representative1, representative2 = representative2, representative1
        self._parent[representative2] = representative1
        self._size[representative1] += self._size[representative2]

    def sizes(self) -> list[int]:
        result = list[int]()
        for i, size in enumerate(self._size):
            if self.find_set(i) == i:
                result.append(size)
        return result


def main() -> None:
    fname = sys.argv[1]
    points = list[Point]()
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            x, y, z = map(int, line.split(","))
            points.append(Point(x, y, z))
    edges = list[tuple[int, int, int]]()
    for (i, u), (j, v) in itertools.combinations(enumerate(points), 2):
        edges.append((i, j, dist(u, v)))
    edges.sort(key=lambda e: e[2])

    dsu1 = DSU(len(points))
    limit1 = 10 if fname == "ex.txt" else 1000
    ans1 = None
    ans2 = None
    for step, (i, j, _) in enumerate(edges, start=1):
        if dsu1.find_set(i) == dsu1.find_set(j):
            continue
        dsu1.union(i, j)
        if step == limit1:
            sizes1 = dsu1.sizes()
            sizes1.sort(reverse=True)
            ans1 = functools.reduce(lambda x, y: x * y, sizes1[:3], 1)
        ans2 = points[i].x * points[j].x
    print(f"ans1 = {ans1}")
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
