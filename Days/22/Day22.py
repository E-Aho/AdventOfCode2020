from collections import deque
from copy import copy


def get_input(input_location: str):
    with open(input_location, "r") as file:
        raw_d1, raw_d2 = file.read().split("\n\n")
        d1 = deque(int(line.strip()) for line in raw_d1.splitlines()[1:])
        d2 = deque(int(line.strip()) for line in raw_d2.splitlines()[1:])
    return d1, d2

def play_part_1(deck_1: deque, deck_2: deque):
    while deck_1 and deck_2:
        card_1, card_2 = deck_1.popleft(), deck_2.popleft()

        if card_1 > card_2:
            deck_1.extend((card_1, card_2))
        else:
            deck_2.extend((card_2, card_1))

    return deck_1 if deck_1 else deck_2

def play_recursive(deck_1: deque, deck_2: deque):
    seen_decks = set()

    while deck_1 and deck_2:
        id = tuple(deck_1), tuple(deck_2)
        if id in seen_decks:
            return True, deck_1
        seen_decks.add(id)

        card_1, card_2 = deck_1.popleft(), deck_2.popleft()
        if len(deck_1) >= card_1 and len(deck_2) >= card_2:
            sub_1, sub_2 = deque(tuple(deck_1)[:card_1]), deque(tuple(deck_2)[:card_2])
            you_did_win, _ = play_recursive(sub_1, sub_2)
        else:
            you_did_win = card_1 > card_2

        if you_did_win:
            deck_1.extend((card_1, card_2))
        else:
            deck_2.extend((card_2, card_1))

    return (True, deck_1) if deck_1 else (False, deck_2)

def get_score(deck: deque):
    tot = 0
    for i, v in enumerate(reversed(deck)):
        tot += v * (i + 1)
    return tot

if __name__ == "__main__":
    d1, d2 = get_input("input.txt")

    winning_deck = play_part_1(copy(d1), copy(d2))
    print(get_score(winning_deck))

    _, winning_deck_2 = play_recursive(copy(d1), copy(d2))
    print(get_score(winning_deck_2))
