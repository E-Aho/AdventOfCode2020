def get_input(location: str):
    with open(location, "r") as file:
        line = file.readlines()[0]
        return [int(val) for val in line.strip().split(",")]

def play_game(starting_numbers: list):

    memory = {}
    i = 0
    last_number = None

    for i in range(len(starting_numbers)):
        curr_number = starting_numbers[i]
        print(f"i: {curr_number}, last={last_number}")
        if last_number is not None:
            memory[last_number] = i - 1
        last_number = curr_number

    for i in range(len(starting_numbers), 30000000):
        if last_number not in memory.keys():
            curr_number = 0
        else:
            curr_number = i - (memory[last_number]+1)
        memory[last_number] = i-1
        last_number = curr_number

    print(f"{i+1}: {curr_number}, last={last_number}")



if __name__ == "__main__":
    input_list = get_input("input.txt")
    play_game(input_list)

