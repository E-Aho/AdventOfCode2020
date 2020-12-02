import collections


def get_input(file_location: str):
    arr = []
    with open(file_location, "r") as file:
        for line in file.readlines():
            split_line = line.split(" ")
            int_0 = int(split_line[0].split("-")[0])
            int_1 = int(split_line[0].split("-")[1])
            letter = split_line[1][:-1]
            password = split_line[2].strip()
            arr.append(
                {"int_0": int_0,
                 "int_1": int_1,
                 "letter": letter,
                 "pw": password}
            )
    return arr


def part_1(input_list: list):
    count = 0
    for i in input_list:
        count_letters = collections.Counter(i["pw"])
        target = count_letters[i["letter"]]
        if i["int_0"] <= target <= i["int_1"]:
            count += 1
    return count


def part_2(input_list: list):
    count = 0
    for i in input_list:
        first = (i["pw"][i["int_0"]-1] == i["letter"])
        second = (i["pw"][i["int_1"]-1] == i["letter"])
        if (first and not second) or (second and not first):
            count += 1
    return count


if __name__ == "__main__":
    parsed_input = get_input("input.txt")
    print(f"part 1: {part_1(parsed_input)}")
    print(f"part 2: {part_2(parsed_input)}")
