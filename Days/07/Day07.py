def parse_input(file_location: str):
    with open(file_location, "r") as file:
        arr = []
        for line in file.readlines():
            outer, inner = line.strip().split(" bags contain ")
            if inner == "no other bags.":
                inner_arr = ()
            else:
                inner.replace(".", "")
                inner_arr = []
                for bag in inner.split(", "):
                    count = int(bag.split(" ")[0])
                    colour = bag.split(" ")[1] + " " + bag.split(" ")[2]
                    inner_arr.append((count, colour))
            arr.append((outer, inner_arr))
        return arr

def list_to_map(input_list: list):
    parsed_map = {}
    for outer_bag in input_list:
        contains = []
        for count, colour in outer_bag[1]:
            contains.append({"count": count, "colour": colour})
        parsed_map[outer_bag[0]] = contains
    return parsed_map

def get_inner_colours(input_map: dict, colour: str, all_colours = None):
    if all_colours is None:
        all_colours = []
    if colour in input_map and len(input_map[colour]) > 0:
        for inner_colour in input_map[colour]:
            all_colours.append(inner_colour["colour"])
            all_colours += [x for x in get_inner_colours(input_map=input_map, colour=inner_colour["colour"])]
    return all_colours


def part_1(input_map: dict):
    has_colour = 0
    for outer_colour, contains in input_map.items():
        holds_colours = get_inner_colours(input_map = input_map, colour=outer_colour)
        if "shiny gold" in holds_colours:
            has_colour += 1
    return has_colour


def get_number_of_inner_bags(input_map: dict, colour: str):
    contains_bags = 0
    if colour in input_map and len(input_map[colour]) > 0:
        for inner_colour in input_map[colour]:
            count = inner_colour["count"]
            bag_colour = inner_colour["colour"]
            contains_bags += count
            contains_bags += (count * get_number_of_inner_bags(input_map=input_map, colour=bag_colour))
    return contains_bags


if __name__ == "__main__":
    target = parse_input("test_input.txt")
    map = list_to_map(target)
    print(part_1(input_map=map))
    print(get_number_of_inner_bags(input_map=map, colour="shiny gold"))
