def get_input(input_location: str):
    with open(input_location, "r") as file:
        return list([int(line.strip()) for line in file.readlines()])

