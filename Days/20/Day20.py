import re
import string
from collections import defaultdict
from itertools import combinations
from math import prod

NORTH = "N"
SOUTH = "S"
EAST = "E"
WEST = "W"

def get_parsed_input(input_location: str):

    with open(input_location, "r") as file:
        raw_tiles = file.read().split("\n\n")
        tiles = []
        for raw_tile in raw_tiles:
            lines = raw_tile.strip().split("\n")
            index = int(lines[0].split(" ")[1].replace(":", ""))
            lines = lines[1:]
            tiles.append( Tile(index, lines))
        return tiles


class Tile:
    def __init__(self, index, lines):
        self.index = index
        self.lines = lines
        self.n = None
        self.s = None
        self.e = None
        self.w = None

        self.set_edges()

    def get_edge(self, direction):
        edges = {NORTH: self.n, SOUTH: self.s, EAST: self.e, WEST: self.w}
        return edges[direction]

    def set_edges(self):
        self.n = self.lines[0]
        self.s = self.lines[-1]
        self.e = ''.join([line[0] for line in self.lines])
        self.w = ''.join([line[-1] for line in self.lines])

    def set_position(self, position: tuple):
        self.position = position

    def get_all_edges(self):
        return {NORTH: self.n,
                SOUTH: self.s,
                EAST: self.e,
                WEST: self.w}

    def rotate90(self):
        new_lines = []
        for i in range(len(self.lines[0])):
            new_row = ''.join(row[i] for row in self.lines)[::-1]
            new_lines.append(new_row)
        self.lines = new_lines
        self.set_edges()
        return self

    def flip(self):
        new_lines = []
        for line in self.lines:
            new_lines.append(line[::-1])
        self.lines = new_lines
        self.set_edges()
        return self

    def get_inner_tile(self):
        return [row[1:-1] for row in self.lines[1:-1]]

    def __repr__(self):
        return f"Tile: {self.index}\n n={self.n}, s={self.s}, \n e={self.e}, w={self.w}\n"

def rotations(tile: Tile):
    yield tile
    for _ in range(3):
        tile = tile.rotate90()
        yield tile

def arrangements(tile: Tile):
    yield from rotations(tile)
    yield from rotations(tile.flip())

def rotate_90(img):
    new_img = []
    for c in range(len(img[0])):
        new_row = "".join(row[c] for row in img)[::-1]
        new_img.append(new_row)
    return new_img

def img_rotations(img):
    yield img
    for _ in range(3):
        img = rotate_90(img)
        yield img

def img_permutations(img):
    yield from img_rotations(img)
    yield from img_rotations(img[::-1])


def find_adjacencies(tile_set: list):
    adjacency_dict = defaultdict(str)
    print(tile_set)
    for tile_a, tile_b in combinations(tile_set, 2):
        edges_a, edges_b = tile_a.get_all_edges(), tile_b.get_all_edges()
        for side_a, a in edges_a.items():
            for side_b, b in edges_b.items():
                if a == b or a == b[::-1]:
                    adjacency_dict[tile_a.index] += side_a
                    adjacency_dict[tile_b.index] += side_b
    return adjacency_dict


def get_corners(adjacency_dict: dict):
    corners = {}
    for tile_id, adjacencies in adjacency_dict.items():
        if len(adjacencies) == 2:
            corners[tile_id] = adjacencies
    return corners

def matching_tile(tile, tile_dict, side_a, side_b) -> Tile:
    edge_to_match = tile.get_edge(side_a)

    for other_id, other_tile in tile_dict.items():
        if tile is other_tile:
            continue
        for arrangement in arrangements(other_tile):
            if edge_to_match == arrangement.get_edge(side_b):
                del tile_dict[other_id]
                return arrangement

def get_matching_row(starting_tile, tiles, tiles_per_row):
    previous_tile = starting_tile
    yield previous_tile
    for _ in range(int(tiles_per_row - 1)):
        next_tile = matching_tile(previous_tile, tiles, EAST, WEST)
        previous_tile = next_tile
        yield previous_tile

def build_image(top_left_tile, tiles, image_dimension):
    first = top_left_tile
    image = []

    while True:
        raw_row = list(get_matching_row(first, tiles, image_dimension))
        image_row = []
        for tile in raw_row:
            image_row.append(tile.get_inner_tile())
        image.extend(map(''.join, zip(*image_row)))

        if not tiles:
            break

        first = matching_tile(first, tiles, SOUTH, NORTH)

    return image


def get_top_left(tile_set: dict, adjacency_dict: dict):
    corners = get_corners(adjacency_dict)

    top_left_id, matching_sides = corners.popitem()
    top_left = tile_set[top_left_id]

    if matching_sides in combinations([NORTH, EAST], 2):
        top_left.rotate90()
    elif matching_sides in combinations([NORTH, WEST], 2):
        top_left.rotate90().rotate90()
    elif matching_sides in combinations([WEST, SOUTH], 2):
        top_left.rotate90().rotate90().rotate90()

    return top_left


def part_2(tiles: list):
    image_dimension = len(tiles) ** 0.5
    tile_dict = {tile.index: tile for tile in tiles}
    adjacency_dict = find_adjacencies(tiles)

    top_left = get_top_left(tile_dict, adjacency_dict)
    del tile_dict[top_left.index]

    image = build_image(top_left, tile_dict, image_dimension)

    pattern = (
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   '
    )

    image_str = "\n".join(image)
    print(image_str)

    monster_cells = sum(row.count("#") for row in pattern)
    water_cells = sum(row.count("#") for row in image)
    n_monsters = count_monsters(image, pattern)

    print(f"N monsters: {n_monsters}")
    result = water_cells - (n_monsters * 15)
    print(f"Roughness: {result}")

def count_monsters(image, pattern):

    monster_width, monster_height = len(pattern[0]), len(pattern)
    image_size = len(image)
    deltas = []

    for r, row in enumerate(pattern):
        for c, cell in enumerate(row):
            if cell == "#":
                deltas.append((r, c))

    for arrangement in img_permutations(image):
        n = 0
        for r in range(image_size - monster_height):
            for c in range(image_size - monster_width):
                if all(arrangement[r + dr][c + dc] == "#" for dr, dc in deltas):
                    n += 1

        if n != 0:
            return n


if __name__ == "__main__":
    tiles = get_parsed_input("input.txt")
    part_2(tiles)

