def get_input(location: str):
    with open(location, "r") as file:
        return [line.strip() for line in file.readlines()]

class Mask:

    def __init__(self, mask_list: list):
        self.value = mask_list

    def apply_mask(self, other_mask):
        for i in range()


def parse_input(input_list: list):
