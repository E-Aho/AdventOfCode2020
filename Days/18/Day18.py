from copy import copy
from math import prod

OPERATORS = ["+", "*"]

def parse_brackets(input_array: list):
    """Parses substrings and creates sub lists for bracket pairs"""
    open_index = None
    bracket_depth = 0
    output_list = []
    for i in range(len(input_array)):
        c = input_array[i]
        if (c in OPERATORS or c.isdigit()) and bracket_depth == 0:
            output_list.append(c)
        elif c[0] == "(":
            if bracket_depth == 0:
                open_index = i
            bracket_depth += c.count("(")
        elif c[-1] == ")":
            bracket_depth -= c.count(")")
            if bracket_depth == 0 and open_index is not None:
                sub_arr = input_array[open_index: i+1]
                sub_arr[0] = sub_arr[0].replace("(", "", 1)
                sub_arr[-1] = sub_arr[-1].replace(")", "", 1)
                output_list.append(parse_brackets(sub_arr))
    return output_list

def get_input(input_location: str):
    lines = []
    with open(input_location, "r") as file:
        for line in file.readlines():
            split_line = line.rstrip().split(" ")
            lines.append(parse_brackets(split_line))
    return lines

def apply_operation(x: int, operator: str, y: int):
    print(x, operator, y)
    op_map = {
        "+": lambda x,y: x+y,
        "*": lambda x,y: x*y
    }
    return op_map[operator](x, y)

def evaluate_expression(expression: list):
    running_sum = 0
    last_operation = None
    for i in range(len(expression)):
        c = expression[i]
        if isinstance(c, list):
            if last_operation is None:
                running_sum = evaluate_expression(c)
            else:
                running_sum = apply_operation(running_sum, last_operation, y=evaluate_expression(c))
        elif c.isdigit():
            if last_operation is None:
                running_sum = int(c)
            else:
                running_sum = apply_operation(running_sum, last_operation, y=int(c))
        elif c in OPERATORS:
            last_operation = c
    return running_sum

def evaluate_expression_with_precedence(expression: list):
    # Do all brackets
    exp = copy(expression)
    for i in range(len(exp)):
        if isinstance(exp[i], list):
            exp[i] = evaluate_expression_with_precedence(exp[i])

    # Do all sums
    running_sum = None
    product_list = []
    last_operator = None
    for i in range(len(exp)):
        c = exp[i]
        if isinstance(c, int) or c.isdigit():
            if running_sum is None:
                running_sum = int(c)
            elif last_operator == "+":
                running_sum += int(c)
            elif last_operator == "*":
                product_list.append(running_sum)
                running_sum = int(c)
        else:
            last_operator = c
    if running_sum is not None:
        product_list.append(running_sum)

    return prod(product_list)


def part_1(input_arr: list):
    vals = []
    for i in range(len(input_arr)):
        print(f"Doing index: i: {input_arr[i]}")
        v = evaluate_expression(input_arr[i])
        vals.append(v)
    print(sum(vals))

def part_2(input_arr: list):
    vals = []
    for i in range(len(input_arr)):
        print(f"Doing index: i: {input_arr[i]}")
        v = evaluate_expression_with_precedence(input_arr[i])
        print(f"Got: {v}")
        vals.append(v)
    print(sum(vals))


if __name__ == "__main__":
    input_arr = get_input("input.txt")
    part_2(input_arr)
