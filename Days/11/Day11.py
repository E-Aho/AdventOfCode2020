from collections import Counter
from copy import deepcopy

empty = "L"
occupied = "#"
floor = "."

def get_input(location: str):
    arr = []
    with open(location, "r") as file:
        for line in file.readlines():
            arr.append(list(line.strip()))
    return arr

def get_adjacent_seats(seat_map: list, x:int, y: int):
    adj = []
    x_min, x_max= 0, len(seat_map[0])
    y_min, y_max= 0, len(seat_map)
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if i == j == 0:
                pass
            else:
                x_i, y_i = x+i, y+j
                if x_min <= x_i < x_max and y_min <= y_i < y_max:
                    adj.append((x_i, y_i))
    return adj

def apply_rules(seat_map: list):
    current_seating = deepcopy(seat_map)
    next_seating = deepcopy(seat_map)

    x_range = range(len(seat_map[0]))
    y_range = range(len(seat_map))


    for y in y_range:
        for x in x_range:
            if (seat := current_seating[y][x]) == floor:
                pass
            else:
                adjacent_seats = get_adjacent_seats(current_seating, x, y)
                adjacent_states = [current_seating[y_i][x_i] for x_i, y_i in adjacent_seats]

                if seat == empty and occupied not in adjacent_states:
                    next_seating[y][x] = occupied
                elif seat == occupied and Counter(adjacent_states)[occupied] >= 4:
                    next_seating[y][x] = empty

    return next_seating

def find_adjacent_visible_seats(seat_map: list, x: int, y: int):
    directions = [(x_dir, y_dir) for x_dir in [-1, 0, 1] for y_dir in [-1, 0, 1] if not x_dir == y_dir == 0]

    adj = []
    x_min, x_max = 0, len(seat_map[0])
    y_min, y_max = 0, len(seat_map)
    for d in directions:
        dist = 0
        while True:
            dist += 1
            x_i, y_i = x + dist * d[0], y + dist * d[1]
            if not (x_min <= x_i < x_max and y_min <= y_i < y_max):
                break
            else:
                if seat_map[y_i][x_i] != floor:
                    adj.append((x_i, y_i))
                    break
    return adj



def display_seating(seat_map):
    map_vis = ""
    for row in seat_map:
        map_vis += "".join(row) + "\n"
    print(map_vis)
    return map_vis

def part_1(seat_map:list):
    map_history = [seat_map]
    map_history.append(apply_rules(seat_map))

    while True:
        if map_history[-1] == map_history[-2]:
            return map_history[-1]
        else:
            next_map = apply_rules(map_history[-1])
            map_history.append(next_map)


def apply_second_rule(seat_map: list):
    current_seating = deepcopy(seat_map)
    next_seating = deepcopy(seat_map)

    x_range = range(len(seat_map[0]))
    y_range = range(len(seat_map))

    visible_dict = {}

    for y in y_range:
        for x in x_range:
            if (seat := current_seating[y][x]) == floor:
                pass
            else:
                if not (x, y) in visible_dict.keys():
                    visible_dict[(x, y)] = find_adjacent_visible_seats(current_seating, x, y)
                adjacent_seats = visible_dict[(x, y)]
                adjacent_states = [current_seating[y_i][x_i] for x_i, y_i in adjacent_seats]
                if seat == empty and occupied not in adjacent_states:
                    next_seating[y][x] = occupied
                elif seat == occupied and Counter(adjacent_states)[occupied] >= 5:
                    next_seating[y][x] = empty

    return next_seating


def part_2(seat_map: list):
    map_history = [seat_map]
    map_history.append(apply_second_rule(seat_map))

    while True:
        if map_history[-1] == map_history[-2]:
            return map_history[-1]
        else:
            next_map = apply_second_rule(map_history[-1])
            map_history.append(next_map)

if __name__ == "__main__":

    seat_map = get_input("input.txt")
    final_map = part_2(seat_map)
    map_str = display_seating(final_map)

    print(f"number of occupied seats: {Counter(map_str)[occupied]}")
