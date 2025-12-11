import collections
import sys


def visit(neighbors: dict[str, list[str]], current: str, paths: dict[str, int]) -> int:
    if current in paths:
        return paths[current]
    result = 0
    for next in neighbors[current]:
        result += visit(neighbors, next, paths)
    paths[current] = result
    return result


def main() -> None:
    fname = sys.argv[1]
    neighbors = collections.defaultdict[str, list[str]](list)
    with open(fname) as fh:
        for line in fh:
            line = line.rstrip()
            source, targets_raw = line.split(": ")
            targets = targets_raw.split(" ")
            neighbors[source] = targets
    ans1 = visit(neighbors, "you", {"out": 1})
    print(f"ans1 = {ans1}")

    total_fft_dac = visit(neighbors, "fft", {"dac": 1})
    if total_fft_dac > 0:
        total_svr_fft = visit(neighbors, "svr", {"fft": 1})
        total_dac_out = visit(neighbors, "dac", {"out": 1})
        ans2 = total_svr_fft * total_fft_dac * total_dac_out
    else:
        total_svr_dac = visit(neighbors, "svr", {"dac": 1})
        total_dac_fft = visit(neighbors, "dac", {"fft": 1})
        total_fft_out = visit(neighbors, "fft", {"out": 1})
        ans2 = total_svr_dac * total_dac_fft * total_fft_out
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
