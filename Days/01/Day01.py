def get_input(file_location):
    arr = []
    with open(file_location, "r") as file:
        for line in file.readlines():
            arr.append(int(line.strip()))
    return arr


def find_sum_to_2020(input_list: list):

    target = 2020

    for a in input_list:
        if (target - a) in input_arr:
            return (target - a) * a


def find_triple_sum_to_2020(input_list: list):

    target = 2020

    for a in input_list:
        input_list.remove(a)
        for b in input_list:
            if (target - (a+b)) in input_list:
                return a*b * (target - (a+b))


if __name__ == "__main__":
    input_arr = get_input("input_1.txt")
    print(f"Part 1: {find_sum_to_2020(input_arr)}")
    print(f"Part 2: {find_triple_sum_to_2020(input_arr)}")
