from itertools import product

ACTIVE = "#"


def get_initial_state(input_location: str):
    active_set = set()
    with open(input_location, "r") as file:
        for y, row in enumerate(file.readlines()):
            for x, value in enumerate(row.strip()):
                if value == ACTIVE:
                    active_set.add((x, y))
    return active_set


class EnergyCube:
    def __init__(self, input_state: set, is_hypercube: bool = False):
        self.is_hypercube = is_hypercube
        if self.is_hypercube:
            self.active_cubes = set((x, y, 0, 0) for (x, y) in input_state)
        else:
            self.active_cubes = set((x, y, 0) for (x, y) in input_state)

    def get_inactive_cubes_adjacent_to_active(self):
        inactive_cubes = set()
        for coord in self.active_cubes:
            for cube in self.get_adjacent_cubes(coord):
                if cube not in self.active_cubes:
                    inactive_cubes.add(cube)
        return inactive_cubes

    def get_adjacent_cubes(self, coords: tuple):
        if not self.is_hypercube:
            x, y, z = coords
            for dx, dy, dz in product([-1, 0, 1], repeat=3):
                if (dx, dy, dz) != (0, 0, 0):
                    yield x + dx, y + dy, z + dz
        else:
            x, y, z, w = coords
            for dx, dy, dz, dw in product([-1, 0, 1], repeat=4):
                if (dx, dy, dz, dw) != (0, 0, 0, 0):
                    yield x + dx, y + dy, z + dz, w + dw

    def get_tot_active_adjacent(self, coord: tuple):
        return sum(s in self.active_cubes for s in self.get_adjacent_cubes(coord))

    def iterate(self, is_hypercube: bool = False):
        next_state = {}
        for coord in self.active_cubes:
            adj = self.get_tot_active_adjacent(coord)
            if adj not in (2, 3):
                next_state[coord] = False

        for coord in self.get_inactive_cubes_adjacent_to_active():
            adj = self.get_tot_active_adjacent(coord)
            if adj == 3:
                next_state[coord] = True

        for coord, is_active in next_state.items():
            if is_active:
                self.active_cubes.add(coord)
            else:
                self.active_cubes.remove(coord)

    def get_tot(self):
        return len(self.active_cubes)


def do_part_1(initial_state: set):
    # Only need to track which ones are adj to an active cube
    energy_cube = EnergyCube(initial_state)
    TURNS = 6
    t = 0
    while t <= TURNS:
        energy_cube.iterate()
        print(t + 1, energy_cube.get_tot())
        t += 1


def do_part_2(initial_state: set):
    energy_hypercube = EnergyCube(initial_state, is_hypercube=True)
    TURNS = 6
    t = 0
    while t < TURNS:
        energy_hypercube.iterate()
        print(t + 1, energy_hypercube.get_tot())
        t += 1


if __name__ == "__main__":
    initial_state = get_initial_state("test_input.txt")
    do_part_1(initial_state)
    do_part_2(initial_state)
