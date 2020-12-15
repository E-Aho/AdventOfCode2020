from copy import deepcopy
from itertools import combinations


def get_input(location: str):
    with open(location, "r") as file:
        return [line.strip() for line in file.readlines()]


len_mask = 36

def get_all_combinations(l: list):
    array = []
    for i in range(len(l)+1):
        [array.append(subset) for subset in combinations(l, i)]
    return array

class Mask:
    def __init__(self, mask_array: list):
        self.zeros = []
        self.ones = []
        self.floaters = []
        for i in range(len_mask):
            if mask_array[i] == "1":
                self.ones.append(i)
            elif mask_array[i] == "0":
                self.zeros.append(i)
            else:
                self.floaters.append(i)
        self.__zeros = deepcopy(self.zeros)
        self.__ones = deepcopy(self.ones)

    def reset(self):
        self.zeros = [_ for _ in self.__zeros]
        self.ones = [_ for _ in self.__ones]

    def apply_floaters(self, new_ones: list):
        new_zeros = [i for i in self.floaters if i not in new_ones]
        self.zeros += new_zeros
        self.ones += new_ones
        return self

    def __str__(self):
        out_map = {}
        for i in self.zeros:
            out_map[i] = "0"
        for j in self.ones:
            out_map[j] = "1"

        out_str = ""
        for i in range(len_mask):
            out_str += out_map.get(i, "X")
        return out_str


class Value:
    def __init__(self, value: int = 0):
        self.value = list(bin(value)[2:].zfill(len_mask))

    def apply_mask(self, mask: Mask):
        for i in mask.zeros:
            self.value[i] = "0"
        for j in mask.ones:
            self.value[j] = "1"
        return self

    def apply_float_mask(self, mask: Mask):
        for i in mask.ones:
            self.value[i] = "1"
        return self

    def apply_floating_values(self, zeros, ones):
        for i in zeros:
            self.value[i] = "0"
        for j in ones:
            self.value[j] = "1"
        return self

    def __int__(self):
        return int(''.join(self.value), 2)


class Emulator:
    def __init__(self):
        self.memory = {}

    def apply_action(self, action: tuple):
        (mask, pos, val) = action
        val = Value(val)
        self.memory[pos] = val.apply_mask(mask)

    def get_total(self):
        total = 0
        for v in self.memory.values():
            total += int(v)
        return total

    def apply_floating_action(self, action: tuple):
        mask, pos, val = action[0], Value(action[1]), action[2]
        pos = pos.apply_float_mask(mask)

        ones_combinations = get_all_combinations(mask.floaters)
        for ones in ones_combinations:
            p = deepcopy(pos)
            zeroes = [i for i in mask.floaters if i not in ones]
            p.apply_floating_values(zeroes, ones)
            self.memory[int(p)] = val




def parse_input(input_list: list):
    mask = None
    action_list = []
    for line in input_list:

        cmd, _, val = line.split(" ")
        if cmd == "mask":
            mask = Mask(val)
        else:
            position = int(''.join(cmd.split("[")[1][:-1]))
            action_list.append((mask, position, int(val)))

    return action_list

def part_1(action_list: list):
    emulator = Emulator()
    for action in action_list:
        emulator.apply_action(action=action)
    return emulator.get_total()

def part_2(action_list: list):
    emulator = Emulator()
    for action in action_list:
        emulator.apply_floating_action(action=action)
    return emulator.get_total()


if __name__ == "__main__":

    action_list = parse_input(get_input("input.txt"))
    print(part_1(action_list))
    print(part_2(action_list))

