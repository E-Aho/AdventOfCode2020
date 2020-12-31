from math import ceil, sqrt


def get_input(input_location: str):
    with open(input_location, "r") as file:
        return tuple(map(int, file.readlines()))

def baby_step_giant_step(base, n, p):

    N = ceil(sqrt(p))
    table = {pow(base, i, p): i for i in range(N)}
    c = pow(base, N * (p-2), p)

    for i in range(N):
        y = (n * pow(c, i, p)) % p
        if y in table:
            return i * N + table[y]

    return None

if __name__ == "__main__":
    A, B = get_input("input.txt")
    a = baby_step_giant_step(7, A, 20201227)
    key = pow(B, a, 20201227)
    print(f"Part 1: {key}")
    print("YAY YOU DID IT")
