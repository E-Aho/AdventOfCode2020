from collections import defaultdict
from itertools import combinations
from math import prod


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
        self.n = lines[0]
        self.s = lines[-1]
        self.e = ''.join([line[0] for line in lines])
        self.w = ''.join([line[-1] for line in lines])
        self.position = None

    def get_all_edges(self):
        return [self.n, self.s, self.e, self.w]

    def __repr__(self):
        return f"Tile: {self.index}\n n={self.n}, s={self.s}, \n e={self.e}, w={self.w}"

def find_adjacencies(tile_set: list):
    adjacency_dict = defaultdict(int)
    print(tile_set)
    for tile_a, tile_b in combinations(tile_set, 2):
        edges_a, edges_b = tile_a.get_all_edges(), tile_b.get_all_edges()
        for a in edges_a:
            for b in edges_b:
                if a == b or a == b[::-1]:
                    adjacency_dict[tile_a.index] += 1
                    adjacency_dict[tile_b.index] += 1
    return adjacency_dict


def get_corners(adjacency_dict: dict):
    corners = []
    for tile_id, adjacencies in adjacency_dict.items():
        if adjacencies == 2:
            corners.append(tile_id)
    return corners



if __name__ == "__main__":
    tiles = get_parsed_input("input.txt")
    print(len(tiles))
    print([x for x in tiles if x.index == 2473])
    adj_dict = find_adjacencies(tiles)
    print(len(adj_dict))
    print(adj_dict)

    print(prod(get_corners(adj_dict)))

