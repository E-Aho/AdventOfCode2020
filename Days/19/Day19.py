import re

def parse_input(input_location: str):
    lines = []
    with open(input_location, "r") as file:
        [lines.append(line.strip()) for line in file.readlines()]

    raw_rules = []
    raw_messages = []

    split_index = [i for i, line in enumerate(lines) if line == ""][0]
    raw_rules = lines[0: split_index]
    raw_messages = lines[split_index+1: len(lines)]

    rules = {}
    for raw_rule in raw_rules:
        i, r = format_rule(raw_rule)
        rules[i] = r
    return rules, raw_messages

def format_rule(raw_rule: str):
    index, r = raw_rule.split(":")
    print(index, r)
    if '"' in r:
        rule = r.split('"')[1]
    elif "|" in r:
        rule = list()
        sub_rules = r.split("|")
        for sub_rule in sub_rules:
            rule.append([int(r) for r in sub_rule.strip().split(" ")])
    else:
        rule = [[int(i) for i in r.strip().split(" ")]]

    return int(index), rule

def parse_rule(rule, rule_map: dict):
    rule = rule_map[rule]
    if isinstance(rule, str):
        return rule
    # Will be a list, either of lists(optional rules), of ints(rules), or strings(optional_parsed_strings)
    options = []
    if isinstance(rule[0], int):
        return "".join(parse_rule(r, rule_map) for r in rule)
    else:
        for option in rule:
            option = "".join(parse_rule(r, rule_map=rule_map) for r in option)
            options.append(option)

    return "(" + "|".join(options) + ")"


def update_rules(rules):
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

def get_matches(rule_map: dict, string: str, rule=0, index=0):
    # Will return indexes that match rule for str, or an empty list if no matches exist
    if index >= len(string):
        return []

    rule = rule_map[rule]
    if isinstance(rule, str):
        if string[index] == rule:
            return [index + 1]
        return []
    else:
        matches = []
        for option in rule:
            sub_matches = [index]
            for sub_rule in option:
                new_matches = []
                for i in sub_matches:
                    new_matches += get_matches(rules, string, sub_rule, i)
                sub_matches = new_matches
            matches += sub_matches
        return matches


def count_all_matches(messages, rules):
    valid_count = 0
    for message in messages:
        if len(message) in get_matches(rules, message):
            valid_count += 1
    return valid_count


if __name__ == "__main__":
    rules, messages = parse_input("input.txt")
    print(rules)
    count_valid = count_all_matches(messages, rules)
    print(f"Part 1:{count_valid}")

    update_rules(rules)
    second_valid_count = count_all_matches(messages, rules)
    print(f"Part 2: {second_valid_count}")


