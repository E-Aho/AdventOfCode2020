
def get_input(file_location: str):
    arr = []
    sub_arr = []
    with open(file_location, "r") as file:
        for line in file.readlines():
            if line == "\n":
                arr.append(sub_arr)
                sub_arr = []
            else:
                sub_arr.append(line.strip())
    return arr



def part_1(arr_input: list):
    total_yes = 0
    for group in arr_input:
        answered_yes = []
        for person in group:
            for c in list(person):
                if c not in answered_yes:
                    answered_yes.append(c)
        total_yes += len(answered_yes)
    return total_yes

def part_2(arr_input: list):
    total_all_yes = 0
    for group in arr_input:
        for c in group[0]:
            if all(c in person for person in group):
                total_all_yes += 1
    return total_all_yes

if __name__ == "__main__":
    input_list = get_input('input.txt')
    print(f"Total yes: {part_1(input_list)}")
    print(f"My seat: {part_2(input_list)}")
