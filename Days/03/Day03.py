
def get_input(file_location: str):
    arr = []
    with open(file_location, "r") as file:
        for line in file.readlines():
            arr.append(line)
        #     split_line = line.split(" ")
        #     int_0 = int(split_line[0].split("-")[0])
        #     int_1 = int(split_line[0].split("-")[1])
        #     letter = split_line[1][:-1]
        #     password = split_line[2].strip()
        #     arr.append(
        #         {"int_0": int_0,
        #          "int_1": int_1,
        #          "letter": letter,
        #          "pw": password}
        #     )
    return arr


def part_1(parsed_input: list):
    return None


def part_2(parsed_input: list):
    return None


if __name__ == "__main__":
    parsed_input = get_input("input.txt")
    print(f"part 1: {part_1(parsed_input)}")
    print(f"part 2: {part_2(parsed_input)}")
