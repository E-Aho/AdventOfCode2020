import math


def get_input(input_location: str):
    with open(input_location, "r") as file:
        return [line.strip() for line in file.readlines()]


def parse_input(input_arr: list):
    arrival_time = int(input_arr[0])
    bus_times = [int(x) if x != "x" else None for x in input_arr[1].split(",")]

    return arrival_time, bus_times


def is_int(x):
    return isinstance(x, int)


def part_1(start_time: int, time_list: list):
    valid_times = filter(is_int, time_list)

    min_time = math.inf
    bus_id = None
    for bus in valid_times:
        if start_time % bus == 0:
            curr_time = 0
        else:
            curr_time = (math.floor(start_time / bus) + 1) * bus - start_time
        if curr_time < min_time:
            min_time = curr_time
            bus_id = bus

    return min_time * bus_id

def part_2(time_list: list):
    t_list = [(key, bus) for key, bus in enumerate(time_list) if bus is not None]

    running_time = t_list[0][1]
    min_inc = 1

    for key, bus in t_list:
        remainder = (bus - key) % bus
        # TODO: There's a way to do this without looping
        while running_time % bus - remainder != 0:
            running_time += min_inc
        min_inc *= bus
    return running_time


if __name__ == "__main__":
    start_time, bus_list = parse_input(get_input("input.txt"))

    print(part_1(start_time, bus_list))
    print(part_2(bus_list))
