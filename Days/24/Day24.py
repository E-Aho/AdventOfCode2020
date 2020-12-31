import operator
from collections import defaultdict

VECTOR_MAP = {
    "e": (1,0),
    "w": (-1,0),
    "ne": (0,-1),
    "nw": (-1,-1),
    "se": (1,1),
    "sw": (0,1)
}

def get_input(input_location: str):
    tile_list = []
    with open(input_location, "r") as file:
        for line in list(map(str.strip, file.readlines())):
            i = 0
            tile = []
            while i < len(line):
                if line[i] in VECTOR_MAP.keys():
                    tile.append(VECTOR_MAP[line[i]])
                    i += 1
                else:
                    tile.append(VECTOR_MAP[line[i:i+2]])
                    i += 2
            tile_list.append(tile)
    return tile_list

def vector_sum(a: tuple, b: tuple):
    return tuple(map(operator.add, a, b))

def get_coordinate(tile_vector: list):
    coordinate = (0,0)
    for v in tile_vector:
        coordinate = vector_sum(coordinate, v)
    return coordinate

def part_1(tiles_as_list: list):
    times_tiles_fliped = defaultdict(int)
    for tile in list(map(get_coordinate, tiles_as_list)):
        times_tiles_fliped[tile] += 1
    black_tiles = set(tile for tile, flipped in times_tiles_fliped.items() if flipped % 2 == 1)
    print(f"Part 1: {len(black_tiles)}")
    return black_tiles

def count_adjacent_black_tiles(coordinate: tuple, black_tiles: set):
    c = 0
    for direction in VECTOR_MAP.values():
        if vector_sum(coordinate, direction) in black_tiles:
            c += 1
    return c

def all_adjacent_tiles(black_tiles: set):
    return set(vector_sum(direction, tile) for direction in VECTOR_MAP.values() for tile in black_tiles)

def iterate(black_tiles: set):
    next_black_tiles = set()
    for tile in all_adjacent_tiles(black_tiles) - black_tiles:
        if count_adjacent_black_tiles(tile, black_tiles) == 2:
            next_black_tiles.add(tile)

    next_black_tiles = next_black_tiles.union(black_tiles)
    for tile in black_tiles:
        if count_adjacent_black_tiles(tile, black_tiles) not in (1,2):
            next_black_tiles.remove(tile)

    return next_black_tiles

def part_2(black_tiles: set):
    for _ in range(100):
        black_tiles = iterate(black_tiles)

    print(f"Part 2: {len(black_tiles)}")


if __name__ == "__main__":
    tiles_as_list = get_input("input.txt")
    black_tiles = part_1(tiles_as_list)
    part_2(black_tiles)
