from copy import deepcopy, copy
from math import prod


def get_input(location: str):
    with open(location, "r") as file:
        return [line.strip() for line in file.readlines()]


def parse_input(input_list: list):
    rules = {}
    tickets = []

    empty_rows = []
    for i in range(len(input_list)):
        if input_list[i] == "":
            empty_rows.append(i)

    rules_raw = input_list[:empty_rows[0]]
    my_ticket_raw = input_list[empty_rows[0]+2: empty_rows[1]]
    nearby_tickets_raw = input_list[empty_rows[1]+2:]

    for s in rules_raw:
        name, rest = s.split(": ")
        ranges = [[int(x) for x in _.split("-")] for _ in rest.split(" or ")]
        full_set = set(range(ranges[0][0], ranges[0][1]+1)).union(set(range(ranges[1][0], ranges[1][1]+1)))
        rules[name] = full_set

    my_ticket = [int(x) for x in my_ticket_raw[0].split(",")]

    for t in nearby_tickets_raw:
        ticket = [int(x) for x in t.split(",")]
        tickets.append(ticket)

    return rules, my_ticket, tickets


def get_valid_tickets(rules, tickets):
    invalid_sum = 0
    valid_tickets = []
    total_rules = {x for _set in rules.values() for x in _set}

    for ticket in tickets:
        valid = True
        for value in ticket:
            if value not in total_rules:
                invalid_sum += value
                valid = False
        if valid:
            valid_tickets.append(ticket)

    return valid_tickets

def find_fields(rules, tickets):
    '''

    :param rules: Dict that maps field names (str) to rules (set of ints which fit)
    :param tickets: List of ints for values
    :return: Dict where each field name maps to it's index

    Each ticket must have a single instance of each field
    All fields of a given index must match one field

    '''

    # First wide parse

    unknown_fields = {field for field in rules.keys()}
    known_fields = {}
    unknown_indexes = {index for index in range(len(tickets[0]))}
    known_indexes = {}
    p_index = {}
    p_field = {field: set() for field in rules.keys()}

    def did_find_field(field_name: str, index: int):
        print(f"Found field!: {field_name}: {index}")
        known_fields[field_name] = index
        known_indexes[index] = field_name
        unknown_fields.remove(field_name)
        unknown_indexes.remove(index)

        for i, p in p_index.items():
            if field_name in p:
                p.remove(field_name)

        for f, p in p_field.items():
            if index in p:
                p.remove(index)

    # Populate possibility maps
    for index in unknown_indexes:
        values_at_index = set()
        p_index[index] = set()
        for ticket in tickets:
            values_at_index.add(ticket[index])

        for field in unknown_fields:
            rule = rules[field]
            if values_at_index.issubset(set(rule)):
                p_index[index].add(field)
                p_field[field].add(index)

    # Go through possibility maps to see if we can find truths
    while len(unknown_fields) > 0:
        for index in copy(unknown_indexes):
            if len(p_index[index]) == 1:
                did_find_field(next(iter(p_index[index])), index)
        for field in copy(unknown_fields):
            if len(p_field[field]) == 1:
                did_find_field(field, next(iter(p_field[field])))

    return known_fields


def do_part_2(field_map: dict, ticket: list):
    wanted_indexes = []
    for name, index in field_map.items():
        if name[:9] == "departure":
            wanted_indexes.append(index)

    return prod([ticket[i] for i in wanted_indexes])

if __name__ == "__main__":
    arr = get_input("input.txt")
    rules, my_ticket, tickets = parse_input(arr)
    valid_tickets = get_valid_tickets(rules=deepcopy(rules), tickets=tickets)
    field_map = find_fields(rules=rules, tickets=valid_tickets)
    result = do_part_2(field_map = field_map, ticket = my_ticket)
    print(result)
