import random
from enum import Enum
from colorama import Fore
from colorama import Style

class R(Enum):
    ROCK = 'R',
    WOOD = 'F',
    WHEAT = 'W',
    SHEEP = 'S',
    BRICK = 'B',
    DESERT = 'D'

board = [[(R.ROCK, 9), (R.WOOD, 11), (R.SHEEP, 6)],
       [(R.WHEAT, 4), (R.WOOD, 3), (R.WHEAT, 2), (R.SHEEP, 5)],
      [(R.SHEEP, 11), (R.ROCK, 8), (R.DESERT, 0), (R.ROCK, 10), (R.WHEAT, 9)],
       [(R.BRICK, 10), (R.SHEEP, 5), (R.BRICK, 12), (R.WHEAT, 4)],
         [(R.WOOD, 6), (R.WOOD, 3), (R.ROCK, 8)]]

resources = {
    'stone': [3, 2, 1],
    'wood':  [8, 4, 9, 11],
    'wheat': [12, 11, 4, 5],
    'sheep': [10, 5, 6, 6],
    'brick': [10, 3, 8]
}

totals = {
    R.ROCK: 0,
    R.WOOD:  0,
    R.WHEAT: 0,
    R.SHEEP: 0,
    R.BRICK: 0,
}

item_prices = {
    'road': [
    {
        'resource': 'wood',
        'quanitity': 1
    },
    {
        'resource': 'brick',
        'quanitity': 1
    }],
    'settlement': [
        {
        'resource': 'wood',
        'quanitity': 1
    },
    {
        'resource': 'brick',
        'quanitity': 1
    },
    {
        'resource': 'wheat',
        'quanitity': 1
    },
    {
        'resource': 'sheep',
        'quanitity': 1
    }],
    'city': [{
        'resource': 'wheat',
        'quanitity': 2
    },
    {
        'resource': 'stone',
        'quanitity': 3
    }],
    'development': [{
        'resource': 'wheat',
        'quanitity': 1
    },
    {
        'resource': 'sheep',
        'quanitity': 1
    },
    {
        'resource': 'rock',
        'quanitity': 1
    }]
}

NUM_TURNS = 1

rolls = {}

for i in range(2, 13):
    rolls[i] = 0

for i in range(NUM_TURNS):
    roll = random.randint(1, 6) + random.randint(1, 6)
    rolls[roll] += 1
    for resource, num in [item for sublist in board for item in sublist]:
        if roll == num:
            totals[resource] += 1

print("Average resource per turn:")
print([(resource, total / float(NUM_TURNS)) for resource, total in totals.items()])

print(rolls)

# 3 characters wide
def tile(row, column):
    return f"{board[row][column][0].name[0]}{board[row][column][1]:2}"

print(tile(0, 0))

board_string = rf"""

                  / \         / \         / \
                /     \     /     \     /     \
              /         \ /         \ /         \
             |           |           |           |
             |    {tile(0, 0)}    |    {tile(0, 1)}    |    {tile(0, 2)}    |
             |           |           |           |
            / \         / \         / \         / \
          /     \     /     \     /     \     /     \
        /         \ /         \ /         \ /         \
       |           |           |           |           |
       |    {tile(1, 0)}    |    {tile(1, 1)}    |    {tile(1, 2)}    |    {tile(1, 3)}    |
       |           |           |           |           |
      / \         / \         / \         / \         / \
    /     \     /     \     /     \     /     \     /     \
  /         \ /         \ /         \ /         \ /         \
 |           |           |           |           |           |
 |    {tile(2, 0)}    |    {tile(2, 1)}    |    {tile(2, 2)}    |    {tile(2, 3)}    |    {tile(2, 4)}    |
 |           |           |           |           |           |
  \         / \         / \         / \         / \         /
    \     /     \     /     \     /     \     /     \     / 
      \ /         \ /         \ /         \ /         \ /
       |           |           |           |           |
       |    {tile(3, 0)}    |    {tile(3, 1)}    |    {tile(3, 2)}    |    {tile(3, 3)}    |
       |           |           |           |           |
        \         / \         / \         / \         /
          \     /     \     /     \     /     \     /
            \ /         \ /         \ /         \ /
             |           |           |           |
             |    {tile(4, 0)}    |    {tile(4, 1)}    |    {tile(4, 2)}    |
             |           |           |           |
              \         / \         / \         /
                \     /     \     /     \     /
                  \ /         \ /         \ /
"""

print(board_string)

# def num_items(item, totals):
#     totals[item] / item_prices[item]

# num_items('road', totals)