from copy import deepcopy


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

    print(invalid_sum)
    return valid_tickets

def find_fields(rules, tickets):
    known_fields = {}
    unknown_indexes = set(range(len(tickets[0])))

    # parse wide first
    index_map = {}
    index_poss = {index: set() for index in unknown_indexes}
    field_map = {field: set() for field in rules.keys()}
    unknown_fields = {k: v for k, v in rules.items()}
    for index in range(len(tickets[0])):
        index_map[index] = set()
        for ticket in tickets:
            index_map[index].add(ticket[index])
        for field_name, field_set in unknown_fields.items():
            if index_map[index].issubset(field_set):
                field_map[field_name].add(index)
                dd = index_poss[index]
                index_poss[index].add(field_name)


    for field_name, possibilities in index_poss.items():
        if len(possibilities) == 1:
            print(f"Found: {possibilities}")
            print(f"Unknown fields: {unknown_fields}")
            found_field = str(next(iter(possibilities)))
            known_fields[field_name] = found_field
            del unknown_fields[found_field]


    while len(unknown_indexes) > 0:
        for ticket in tickets:
            unknown_fields = {k: v for k, v in rules.items() if k not in known_fields.keys()}
            field_possibilities = {k: [] for k in unknown_fields.keys()}
            index_possibilities = {}

            print(unknown_indexes)

            # Check if each field only has one possibility
            for index in unknown_indexes:
                value = ticket[index]
                possibilities = [field for field in unknown_fields.keys() if value in unknown_fields[field]]
                if len(possibilities) == 1:
                    found_field = possibilities[0]
                    print(f"Found field {field}")
                    known_fields[found_field] = index
                    del unknown_fields[found_field]
                    unknown_indexes.remove(index)
                else:
                    for field in possibilities:
                        field_possibilities[field].append(index)
                    index_possibilities[index] = len(possibilities)

            # Check if any of the fields only have one possibility
            for field, field_possibilities in field_possibilities.items():
                if len(field_possibilities) == 1:
                    print(f"Found field: {field}")
                    index = field_possibilities[0]
                    known_fields[field] = index
                    del unknown_fields[field]
                    unknown_indexes.remove(index)

    return known_fields


if __name__ == "__main__":
    arr = get_input("test_input.txt")
    rules, my_ticket, tickets = parse_input(arr)
    # print(rules)
    valid_tickets = get_valid_tickets(rules=deepcopy(rules), tickets=tickets)
    # print(valid_tickets)
    field_map = find_fields(rules=rules, tickets=valid_tickets)
    print(field_map)
