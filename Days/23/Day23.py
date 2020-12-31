from collections import deque
from copy import copy


def get_input(input_location:str):
    with open(input_location, "r") as file:
        return tuple(map(int, file.read().strip()))

def perform_move(cups: deque):
    min_cup, max_cup = min(cups), max(cups)
    current = cups[0]
    cups.rotate(-1)
    picked_up = [cups.popleft() for _ in range(3)]

    destination = current - 1
    while destination in picked_up or destination < min_cup:
        if destination < min_cup:
            destination = max_cup
        else:
            destination -= 1

    position = cups.index(destination) + 1
    cups.rotate(-position)
    cups.extendleft(picked_up[::-1])
    cups.rotate(position)
    return cups

def play_game(cups: deque, moves: int):
    for _ in range(moves):
        cups = perform_move(cups)
    return cups

def part_1(cups: tuple, n_moves: int):
    final_cups = play_game(deque(cups), n_moves)

    final_cups.rotate(1)
    position = final_cups.index(1)
    final_cups.rotate(-position)
    final_cups.popleft()

    print(f"Part 1: {''.join(map(str, final_cups))}")

def make_linked_list(initial_cups: tuple, total_cups: int = 0):
    initial_size = max(initial_cups) + 1
    next_cup = [0] * initial_size

    for prev, cur in zip(initial_cups, initial_cups[1:]):
        next_cup[prev] = cur

    if total_cups <= initial_size:
        next_cup[initial_cups[-1]] = initial_cups[0]
    else:
        next_cup += list(range(initial_size + 1, total_cups + 2))
        next_cup[total_cups] = cups[0]
        next_cup[initial_cups[-1]] = initial_size
    return next_cup


def play_big_game(initial_cups: tuple, number_of_cups: int, number_of_turns: int):
    next_cup_map = make_linked_list(initial_cups, number_of_cups)
    max_cup = len(next_cup_map) - 1
    current = initial_cups[0]

    for _ in range(number_of_turns):
        first = next_cup_map[current]
        middle = next_cup_map[first]
        last = next_cup_map[middle]
        picked_cups = [first, middle, last]

        next_cup_map[current] = next_cup_map[last]
        destination = max_cup if current == 1 else current - 1
        while destination in picked_cups:
            destination = max_cup if destination == 1 else destination -1

        next_cup_map[last] = next_cup_map[destination]
        next_cup_map[destination] = first

        current = next_cup_map[current]

    return next_cup_map

def part_2(start_cups: tuple):
    final_cup_map = play_big_game(start_cups, number_of_cups=1000000, number_of_turns=10000000)
    print(f"Part 2: {final_cup_map[1] * final_cup_map[final_cup_map[1]]}")


if __name__ == "__main__":
    cups = get_input("input.txt")
    print(cups)
    part_1(copy(cups), 100)
    part_2(cups)


