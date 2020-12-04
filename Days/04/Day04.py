import re
from copy import deepcopy

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
optional_fields = ["cid"]
all_fields = required_fields + optional_fields

def get_input(file_location: str):
    arr = []
    with open(file_location, "r") as file:
        passport = {}
        for line in file.readlines():
            if line.strip() == "":
                arr.append(deepcopy(Passport(passport)))
                passport = {}
            else:
                for field in line.rstrip().split(" "):
                    field_name, input_data = field.split(":")
                    if field_name in all_fields:
                        passport[field_name] = input_data
        if passport is not {}:
            arr.append(Passport(passport))
    return arr


def part_1(parsed_input: list):
    valid_count = 0
    for passport in parsed_input:
        if passport.validate_soft():
            valid_count += 1
    return valid_count


def part_2(parsed_input: list):
    valid_count = 0
    for passport in parsed_input:
        if passport.validate():
            valid_count += 1
    return valid_count

class Passport:

    required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    optional_fields = ["cid"]

    def __init__(self, v: dict):
        self.byr = v.get("byr", None)
        self.iyr = v.get("iyr", None)
        self.eyr = v.get("eyr", None)
        self.hgt = v.get("hgt", None)
        self.hcl = v.get("hcl", None)
        self.ecl = v.get("ecl", None)
        self.pid = v.get("pid", None)
        self.cid = v.get("cid", None)

    def validate_soft(self):
        if all([self.__dict__[field] is not None for field in required_fields]):
            return True
        return False

    def validate(self):
        return (
                self.validate_byr() and
                self.validate_iyr() and
                self.validate_eyr() and
                self.validate_hgt() and
                self.validate_hcl() and
                self.validate_ecl() and
                self.validate_pid()
        )

    def validate_pid(self):
        try:
            if len(self.pid) == 9:
                int(self.pid)
                return True
            return False
        except:
            return False

    def validate_byr(self):
        try:
            if 1920 <= int(self.byr) <= 2002:
                return True
            return False
        except:
            return False

    def validate_iyr(self):
        try:
            if 2010 <= int(self.iyr) <= 2020:
                return True
            return False
        except:
            return False

    def validate_eyr(self):
        try:
            if 2020 <= int(self.eyr) <= 2030:
                return True
            return False
        except:
            return False

    def validate_hgt(self):
        try:
            val = int(self.hgt[:-2])
            unit = self.hgt[-2:]
            if unit == "cm":
                if 150 <= val <= 193:
                    return True
            elif unit == "in":
                if 59 <= val <= 76:
                    return True
            return False
        except:
            return False

    def validate_hcl(self):
        hex_regex = "^#(?:[0-9a-fA-F]{3}){1,2}$"
        try:
            if re.search(hex_regex, self.hcl):
                return True
            return False
        except:
            return False

    def validate_ecl(self):
        accepted_colours = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        try:
            if self.ecl in accepted_colours:
                return True
            return False
        except:
            return False

if __name__ == "__main__":
    parsed_input = get_input("input.txt")
    print(f"part 1: {part_1(parsed_input)}")
    print(f"part 2: {part_2(parsed_input)}")
