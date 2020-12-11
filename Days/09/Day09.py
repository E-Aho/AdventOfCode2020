from collections import defaultdict


def get_input(input_location: str):
    arr = []
    with open(input_location, "r") as file:
        return list([int(line.strip()) for line in file.readlines()])


def get_invalid_numbers(list_of_numbers: list, l: int):
    numbers_to_check = []
    running_sums = defaultdict(int)
    list_of_non_sums = []

    numbers_to_check.append(list_of_numbers.pop(0))

    while len(list_of_numbers) > 0:
        if len(numbers_to_check) < l:
            n = list_of_numbers.pop(0)
            for m in numbers_to_check:
                running_sums[m+n] += 1
            numbers_to_check.append(n)
        else:
            n = list_of_numbers.pop(0)
            if running_sums[n] <= 0:
                list_of_non_sums.append(n)

            m = numbers_to_check.pop(0)
            for k in numbers_to_check:
                running_sums[m+k] -= 1
                running_sums[n+k] += 1
            numbers_to_check.append(n)

    return list_of_non_sums


def get_contiguous_list(number_list: list, target: int):

    for i in range(len(number_list)):
        for j in range(i+1, len(number_list)):
            if s := sum(l := number_list[i:j]) == target:
                return l
            elif s > target:
                break


if __name__ == "__main__":
    number_list = get_input("input.txt")
    first_invalid_number = get_invalid_numbers(number_list.copy(), 25)[0]
    print(first_invalid_number)
    print(len(number_list))
    contiguous_list = get_contiguous_list(number_list=number_list, target=first_invalid_number)

    print(min(contiguous_list) + max(contiguous_list))

