from math import cos, sin, pi


def get_input(input_location: str):
    with open(input_location, "r") as file:
        lines = [line.strip() for line in file.readlines()]
        return [(line[0], int(line[1:])) for line in lines]


def to_radians(degrees: int):
    return (pi * degrees) / 180


class Vector:
    def __init__(self, coords: tuple = (0, 0)):
        self.x = coords[0]
        self.y = coords[1]

    def distance_from(self, other_pos):
        return abs(self.x + other_pos.x) + abs(self.y + other_pos.y)

    def rotate(self, direction, val):

        angle = to_radians(val)
        if direction == "R":
            angle *= -1
        cos_angle = int(cos(angle))
        sin_angle = int(sin(angle))

        x_i = self.x * cos_angle - self.y * sin_angle
        y_i = self.x * sin_angle + self.y * cos_angle

        self.x = x_i
        self.y = y_i

    def __mul__(self, other):
        if isinstance(other, int):
            x = self.x * other
            y = self.y * other
            return Vector((x, y))
        else:
            raise Exception("Only multiplying by ints is supported for __mul__ here")

    def __rmul__(self, other):
        self.__mul__(other)

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y))

    def __repr__(self):
        return (self.x, self.y)

    def __str__(self):
        return f"x: {self.x}, y: {self.y}"


NORTH = Vector((0, 1))
SOUTH = Vector((0, -1))
EAST = Vector((1, 0))
WEST = Vector((-1, 0))

class Ship:

    def __init__(self):
        self.position = Vector((0,0))
        self.direction = Vector((1, 0))
        self.waypoint = Vector((10, 1))
        self.x = self.position.x
        self.y = self.position.y

    def move_forward(self, value):
        movement_vector = self.direction * value
        self.position += movement_vector

    def rotate(self, direction, value):
        self.direction.rotate(direction, value)

    def move(self, direction, value):
        movement_vector = (direction * value)
        self.position += movement_vector

    def move_waypoint(self, direction, value):
        movement_vector = direction * value
        self.waypoint += movement_vector

    def waypoint_forward(self, value):
        movement_vector = self.waypoint * value
        self.position += movement_vector

    def waypoint_rotate(self, direction, value):
        self.waypoint.rotate(direction, value)

    def apply_action(self, action):
        print(action)
        do_action = {
            "N": lambda v: self.move(NORTH, v),
            "S": lambda v: self.move(SOUTH, v),
            "E": lambda v: self.move(EAST, v),
            "W": lambda v: self.move(WEST, v),
            "L": lambda v: self.direction.rotate("L", v),
            "R": lambda v: self.direction.rotate("R", v),
            "F": lambda v: self.move_forward(v)
        }

        action_type = action[0]
        value = action[1]

        do_action[action_type](value)

    def apply_action_to_waypoint(self, action):
        print(action)
        do_action = {
            "N": lambda v: self.move_waypoint(NORTH, v),
            "S": lambda v: self.move_waypoint(SOUTH, v),
            "E": lambda v: self.move_waypoint(EAST, v),
            "W": lambda v: self.move_waypoint(WEST, v),
            "L": lambda v: self.waypoint_rotate("L", v),
            "R": lambda v: self.waypoint_rotate("R", v),
            "F": lambda v: self.waypoint_forward(v)
        }

        action_type = action[0]
        value = action[1]

        do_action[action_type](value)

def part_1(input_list: list):

    ship = Ship()
    for action in input_list:
        print(f"Position: {ship.position}")
        ship.apply_action(action)
    return ship.position.distance_from(Vector((0, 0)))

def part_2(input_list: list):

    ship = Ship()
    for action in input_list:
        print(f"Position: {ship.position}")
        ship.apply_action_to_waypoint(action)
    return ship.position.distance_from(Vector((0,0)))


if __name__ == "__main__":

    final_dist = part_1(get_input("input.txt"))
    print(final_dist)

    second_dist = part_2(get_input("input.txt"))
    print(second_dist)

