import bisect
import dataclasses
import sys


@dataclasses.dataclass
class Interval:
    lo: int
    hi: int


def main() -> None:
    fname = sys.argv[1]
    original_intervals = list[Interval]()
    queries = list[int]()
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            if not line:
                break
            lo, hi = map(int, line.split("-", maxsplit=1))
            original_intervals.append(Interval(lo, hi))
        for line in fh:
            line = line.rstrip()
            queries.append(int(line))

    original_intervals.sort(key=lambda interval: (interval.lo, -interval.hi))

    intervals = list[Interval]()
    current = dataclasses.replace(original_intervals[0])
    for interval in original_intervals[1:]:
        if interval.lo > current.hi:
            intervals.append(current)
            current = dataclasses.replace(interval)
        else:
            current.hi = max(current.hi, interval.hi)
    intervals.append(current)

    ans1 = 0
    for query in queries:
        index = bisect.bisect_right(intervals, query, key=lambda interval: interval.lo)
        if index == 0:
            continue
        if query <= intervals[index - 1].hi:
            ans1 += 1
    print(f"ans1 = {ans1}")

    ans2 = 0
    for interval in intervals:
        ans2 += interval.hi - interval.lo + 1
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
