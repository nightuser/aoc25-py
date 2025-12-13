import collections
import enum
import sys


class ParserPhase(enum.Enum):
    PARSE_TILE = enum.auto()
    PARSE_TILE_SHAPE = enum.auto()
    PARSE_REGION = enum.auto()


CompressedTileShape = list[int]
Rotations = list[CompressedTileShape]
Tiles = list[tuple[Rotations, int]]
Regions = list[tuple[int, int, tuple[int, ...], int]]
State = tuple[int, int, tuple[int, ...], tuple[int, ...], int, int]


def parse_bin(row: list[int]) -> int:
    result = 0
    for b in row:
        result = 2 * result + b
    return result


def parse_input() -> tuple[Tiles, Regions]:
    fname = sys.argv[1]
    tile = list[list[int]]()
    tiles = Tiles()
    regions = Regions()
    with open(fname) as fh:
        phase = ParserPhase.PARSE_TILE
        line = fh.readline().rstrip()
        while fh:
            match phase:
                case ParserPhase.PARSE_TILE:
                    if "x" in line:
                        phase = ParserPhase.PARSE_REGION
                        continue
                    current_id = int(line[:-1])
                    assert current_id == len(tiles)
                    phase = ParserPhase.PARSE_TILE_SHAPE
                case ParserPhase.PARSE_TILE_SHAPE:
                    if not line:
                        phase = ParserPhase.PARSE_TILE
                        rotations = Rotations()
                        weight = 0
                        for row in tile:
                            weight += sum(row)
                        for _ in range(4):
                            rotation = [parse_bin(row) for row in tile]
                            rotations.append(rotation)
                            tile_height = len(tile)
                            tile_width = len(tile[0])
                            new_tile = [
                                [0 for _ in range(tile_height)]
                                for _ in range(tile_width)
                            ]
                            for x in range(tile_height):
                                for y in range(tile_width):
                                    new_tile[tile_height - 1 - x][y] = tile[y][x]
                            tile = new_tile
                        tiles.append((rotations, weight))
                        tile = []
                    else:
                        tile.append([int(c == "#") for c in line])
                case ParserPhase.PARSE_REGION:
                    if not line:
                        break
                    dims, cnts_raw = line.split(": ")
                    width, height = map(int, dims.split("x"))
                    cnts = tuple(int(x) for x in cnts_raw.split(" "))
                    total_weight = 0
                    for cnt, (_, weight) in zip(cnts, tiles):
                        total_weight += cnt * weight
                    regions.append((width, height, cnts, total_weight))
            line = fh.readline().rstrip()
    return tiles, regions


def main() -> None:
    tiles, regions = parse_input()
    ans1 = 0
    for width, height, cnts, total_weight in regions:
        queue = collections.deque[State]()
        visited = set[State]()

        initial_state = (0, 0, cnts, (0, 0, 0), total_weight, 0)
        queue.append(initial_state)
        visited.add(initial_state)

        def enqueue(new_state: State):
            nonlocal queue, visited
            if new_state in visited:
                return
            new_x, _, _, _, new_needed_weight, new_profile_weight = new_state
            available_weight = (width - new_x) * height - new_profile_weight
            if available_weight < new_needed_weight:
                return
            queue.append(new_state)
            visited.add(new_state)

        can_fit = False
        while queue:
            x, y, current_cnts, profile, needed_weight, profile_weight = queue.pop()
            if needed_weight == 0:
                can_fit = True
                break
            if y == height - 2:
                if x < width - 3:
                    enqueue(
                        (
                            x + 1,
                            0,
                            current_cnts,
                            profile[1:] + (0,),
                            needed_weight,
                            profile_weight - profile[0].bit_count(),
                        )
                    )
                continue
            enqueue((x, y + 1, current_cnts, profile, needed_weight, profile_weight))
            for tile_id, (rotations, weight) in enumerate(tiles):
                if current_cnts[tile_id] == 0:
                    continue
                for rotation in rotations:
                    if any(
                        ((col_mask << y) & profile_mask) != 0
                        for col_mask, profile_mask in zip(rotation, profile)
                    ):
                        continue
                    new_cnts = tuple(
                        cnt - int(cnt_id == tile_id)
                        for cnt_id, cnt in enumerate(current_cnts)
                    )
                    new_profile = tuple(
                        (col_mask << y) | profile_mask
                        for col_mask, profile_mask in zip(rotation, profile)
                    )
                    enqueue(
                        (
                            x,
                            y + 1,
                            new_cnts,
                            new_profile,
                            needed_weight - weight,
                            profile_weight + weight,
                        )
                    )
        ans1 += can_fit
    print(f"ans1 = {ans1}")


if __name__ == "__main__":
    main()
