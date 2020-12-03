
def get_input(file_location: str):
    arr = []
    with open(file_location, "r") as file:
        for line in file.readlines():
            arr.append(list(line.strip()))
    print(arr[0])
    return arr


def part_1(parsed_input: list, x: int = 1, y:int = 3):
    count = 0
    for i in range(int(len(parsed_input)/x)):
        if parsed_input[x*i][(y*i % len(parsed_input[i]))] == "#":
            count += 1
    return count


def part_2(parsed_input: list):
    a = part_1(parsed_input, x=1, y=1)
    b = part_1(parsed_input, x=1, y=3)
    c = part_1(parsed_input, x=1, y=5)
    d = part_1(parsed_input, x=1, y=7)
    e = part_1(parsed_input, x=2, y=1)

    return a * b * c * d * e


if __name__ == "__main__":
    parsed_input = get_input("input.txt")
    print(f"part 1: {part_1(parsed_input)}")
    print(f"part 2: {part_2(parsed_input)}")
