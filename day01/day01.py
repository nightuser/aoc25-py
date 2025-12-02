import enum
import sys

START_POS = 50
DIAL = 100


class Dir(enum.StrEnum):
    LEFT = "L"
    RIGHT = "R"


def mirror(pos: int) -> int:
    if pos == 0:
        return 0
    return DIAL - pos


def main() -> None:
    input_fname = sys.argv[1]
    rotations = list[tuple[Dir, int]]()
    with open(input_fname) as fh:
        for line in fh:
            line = line.rstrip()
            dir = Dir(line[0])
            turns = int(line[1:])
            rotations.append((dir, turns))

    ans1 = 0
    ans2 = 0

    current = START_POS
    for dir, turns in rotations:
        match dir:
            case Dir.LEFT:
                mirrored = mirror(current)
                diff, mirrored = divmod(mirrored + turns, DIAL)
                current = mirror(mirrored)
            case Dir.RIGHT:
                diff, current = divmod(current + turns, DIAL)

        ans2 += diff

        if current == 0:
            ans1 += 1

    print(f"ans1 = {ans1}")
    print(f"ans2 = {ans2}")


if __name__ == "__main__":
    main()
