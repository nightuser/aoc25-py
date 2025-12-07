import collections
import sys


def main() -> None:
    fname = sys.argv[1]
    beams = collections.defaultdict[int, int](int)
    next_beams = collections.defaultdict[int, int](int)
    ans1 = 0
    with open(fname) as fh:
        start_line = fh.readline().rstrip()
        start_pos = start_line.index("S")
        beams[start_pos] = 1
        for line in fh:
            line = line.rstrip()
            while beams:
                beam_pos, timelines = beams.popitem()
                if line[beam_pos] == "^":
                    ans1 += 1
                    next_beams[beam_pos - 1] += timelines
                    next_beams[beam_pos + 1] += timelines
                else:
                    next_beams[beam_pos] += timelines
            beams, next_beams = next_beams, beams
    ans2 = sum(beams.values())
    print(f"ans1 = {ans1}")
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
