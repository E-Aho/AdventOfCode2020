from collections import defaultdict


def get_input(input_location: str):
    with open(input_location, "r") as file:
        return list([int(line.strip()) for line in file.readlines()])


def get_device_joltage(joltage_list: list):
    return max(joltage_list) + 3


def part_1(joltage_list: list):
    c_1 = 0
    c_3 = 0
    joltage_list.append(0)
    l = sorted(joltage_list)
    l.append(get_device_joltage(joltage_list))

    for i in range(len(joltage_list)):
        print(l[i], l[i + 1])
        if l[i + 1] - l[i] == 1:
            c_1 += 1
        elif l[i + 1] - l[i] == 3:
            c_3 += 1
    return c_1 * c_3


def part_2(joltage_list: list):
    joltage_list.append(0)
    joltage_list.append(get_device_joltage(joltage_list))
    paths = defaultdict(int)
    paths[0] = 1

    for adapter in sorted(joltage_list):
        for d_jolt in (range(1, 4)):
            next_adapter = adapter + d_jolt
            if next_adapter in joltage_list:
                paths[next_adapter] += paths[adapter]

    return paths[max(joltage_list)]


if __name__ == "__main__":
    jolts = get_input("input.txt")
    part_1_solution = part_1(jolts.copy())

    print(part_1_solution)

    print(part_2(jolts))
