from collections import defaultdict


def get_input(input_location: str):
    with open(input_location, "r") as file:
        return [line.strip() for line in file.readlines()]

def parse_input(input_location: str):
    parsed_input = []
    for line in get_input(input_location):
        ingredient_str, allergens_str = line.split("(")
        ingredients = ingredient_str.strip().split(" ")
        allergens = allergens_str[9:-1].split(", ")
        parsed_input.append((ingredients, allergens))
    return(parsed_input)

def get_common_maps(input_list: list):
    ingredient_map = defaultdict(set)
    allergen_map = defaultdict(list)
    recipe_map = {}

    for recipe, (ingredients, allergens) in enumerate(input_list):
        [[ingredient_map[ingredient].add(allergen) for allergen in allergens] for ingredient in ingredients]
        [allergen_map[allergen].append(recipe) for allergen in allergens]
        recipe_map[recipe] = ingredients
    return dict(ingredient_map), dict(allergen_map), dict(recipe_map)


def get_non_allergens(potential_allergens: dict, recipes_with_allergen: dict, recipes: dict):
    non_allergens = []

    for ingredient, potential_allergens in potential_allergens.items():
        impossible_allergens = set()
        for allergen in potential_allergens:
            for recipe in recipes_with_allergen[allergen]:
                if ingredient not in recipes[recipe]:
                    impossible_allergens.add(allergen)
                    break

        potential_allergens -= impossible_allergens
        if not potential_allergens:
            non_allergens.append(ingredient)
    return non_allergens

def part_1(recipe_map, non_allergens):
    return sum(ingredient in recipe for recipe in recipe_map.values() for ingredient in non_allergens)

def get_dangerous_ingredients(potential_allergens: dict, recipes_with_allergen: dict, recipes: dict):
    non_allergens = get_non_allergens(potential_allergens, recipes_with_allergen, recipes)
    identified = {}

    for non_allergen in non_allergens:
        del potential_allergens[non_allergen]

    while potential_allergens:
        for ingredient, potential_allergen in potential_allergens.items():
            if len(potential_allergen) == 1:
                break
        # Identified that ingredient => allergen
        allergen = potential_allergen.pop()
        identified[allergen] = ingredient
        del potential_allergens[ingredient]

        for other_ingredient, possible_allergens in potential_allergens.items():
            if allergen in possible_allergens:
                possible_allergens.remove(allergen)

    return identified


def part_2(ingredient_map, allergen_map, recipe_map):
    dangerous_ingredient_map = get_dangerous_ingredients(ingredient_map, allergen_map, recipe_map)
    sorted_allergens = ','.join(map(dangerous_ingredient_map.get, sorted(dangerous_ingredient_map)))
    print(f"Part 2: \n{sorted_allergens}")

if __name__ == "__main__":
    input_list = parse_input("input.txt")

    ingredient_map, allergen_map, recipe_map = get_common_maps(input_list)

    non_allergens = get_non_allergens(ingredient_map, allergen_map, recipe_map)

    print(non_allergens)
    print(part_1(recipe_map=recipe_map, non_allergens=non_allergens))
    part_2(ingredient_map, allergen_map, recipe_map)

