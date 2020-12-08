from copy import deepcopy


def get_input(file_location: str):
    with open(file_location, "r") as file:
        arr = []
        for line in file.readlines():
            arr.append(line.strip())
        return arr


class Action:
    def __init__(self, input_row: str):
        _ = input_row.strip().split(" ")
        self.cmd = _[0]
        self.arg = int(_[1])

    def __str__(self):
        return f"mem: {self.cmd}, arg: {self.arg}"

    def __repr__(self):
        return str(self)

    def flip_nop_jump(self):
        if self.cmd == "jmp":
            self.cmd = "nop"
        elif self.cmd == "nop":
            self.cmd = "jmp"


class GameConsole:
    def __init__(self, input_array):
        self.mem = [Action(x) for x in input_array]
        self.index = 0
        self.acc = 0
        self.performed_indexes = set()
        self.cont = True

    def do_nop(self):
        self.performed_indexes.add(self.index)
        self.index += 1
        if self.index in self.performed_indexes:
            self.cont = False

    def do_acc(self, arg: int):
        self.performed_indexes.add(self.index)
        self.acc += arg
        self.index += 1

    def do_jmp(self, arg: int):
        self.performed_indexes.add(self.index)
        self.index += arg
        if self.index in self.performed_indexes:
            self.cont = False

    def perform_cmd(self):
        action_lambda = {
            "jmp": lambda arg: self.do_jmp(arg),
            "nop": lambda arg: self.do_nop(),
            "acc": lambda arg: self.do_acc(arg)
        }
        a = self.mem[self.index]
        action_lambda[a.cmd](a.arg)

    def find_acc_before_first_dup(self):
        while True:
            if self.index in self.performed_indexes:
                return self.acc
            else:
                self.perform_cmd()

    def does_get_to_end(self):
        try:
            while self.cont:
                self.perform_cmd()
            return False
        except IndexError:
            return True

    def reset(self):
        self.acc = 0
        self.cont = True
        self.index = 0
        self.performed_indexes = set()

    def automate_fix(self):
        print(f"Fixing console")
        self.reset()
        # Check if already fixed
        if self.does_get_to_end():
            print("Console is already fixed!")
            return

        # go through, flip each jmp or nop and check if the console can finish
        while True:
            action = self.mem[self.index]
            if action.cmd in ["jmp", "nop"]:
                cache_index = deepcopy(self.index)
                action.flip_nop_jump()
                if self.does_get_to_end():
                    print("Fixed!")
                    self.reset()
                    return
                else:
                    # Change did not fix, revert and continue
                    self.index = cache_index
                    action.flip_nop_jump()
                    self.perform_cmd()
                    self.cont = True

            else:
                # Keep going until we find another jmp/nop cmd to flip
                self.perform_cmd()

    def perform_to_end(self):
        try:
            while True:
                self.perform_cmd()
        except IndexError:
            return


def do_part_1(console: GameConsole):

    print(f"Part 1: {console.find_acc_before_first_dup()}")
    console.reset()


def do_part_2(console: GameConsole):

    console.automate_fix()
    console.perform_to_end()

    print(f"Console has finished! Final acc: {console.acc}")


if __name__ == "__main__":
    in_arr = get_input("input.txt")
    console = GameConsole(in_arr)

    do_part_1(console)
    do_part_2(console)

