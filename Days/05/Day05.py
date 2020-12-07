
def get_input(file_location: str):
    arr = []
    with open(file_location, "r") as file:
        for line in file.readlines():
            arr.append(Seat(str(line.strip())))
    return arr


class Seat:

    def __init__(self, seat_partition: str):
        self.string = seat_partition
        self.row = self.get_row(seat_partition[:7])
        self.col = self.get_col(seat_partition[-3:])
        self.id = int(self.get_id())


    def get_row(self, row_str: str):
        c = 0
        l = len(row_str)
        for i in range(l):
            if row_str[i].upper() == "B":
                c += 2 ** (l-1-i)
        return c

    def get_col(self, col_str: str):
        c = 0
        l = len(col_str)
        for i in range(l):
            if col_str[i].upper() == "R":
                c += 2 ** (l-1-i)
        return c

    def get_id(self):
        return self.row * 8 + self.col

    def __str__(self):
        return (f"Row: {self.row}, Col: {self.col}, id: {self.id}")

def part_1(arr_input: list):
    max = 0
    for seat in arr_input:
        if seat.id > max:
            max = seat.id
    return max


def part_2(arr_input: list):
    map = set([x.id for x in arr_input])
    for seat_id in map:
        if (seat_id+1 not in map and seat_id+2 in map):
            return seat_id+1



if __name__ == "__main__":
    input_list = get_input('input.txt')
    print(f"Max: {part_1(input_list)}")
    print(f"My seat: {part_2(input_list)}")
