import random
from enum import Enum
from colorama import Fore
from colorama import Style

import pprint

import itertools

class R(Enum):
    ROCK = 'R',
    WOOD = 'F',
    HAY = 'W',
    SHEEP = 'S',
    BRICK = 'B',
    DESERT = 'D'

board = [[(R.ROCK, 9), (R.WOOD, 11), (R.SHEEP, 6)],
       [(R.HAY, 4), (R.WOOD, 3), (R.HAY, 2), (R.SHEEP, 5)],
      [(R.SHEEP, 11), (R.ROCK, 8), (R.DESERT, 0), (R.ROCK, 10), (R.HAY, 9)],
       [(R.BRICK, 10), (R.SHEEP, 5), (R.BRICK, 12), (R.HAY, 4)],
         [(R.WOOD, 6), (R.WOOD, 3), (R.ROCK, 8)]]


totals = {
    R.ROCK: 0,
    R.WOOD:  0,
    R.HAY: 0,
    R.SHEEP: 0,
    R.BRICK: 0,
}

item_prices = {
    'road': [
    {
        'resource': R.WOOD,
        'quanitity': 1
    },
    {
        'resource': R.BRICK,
        'quanitity': 1
    }],
    'settlement': [
        {
        'resource': R.WOOD,
        'quanitity': 1
    },
    {
        'resource': R.BRICK,
        'quanitity': 1
    },
    {
        'resource': R.HAY,
        'quanitity': 1
    },
    {
        'resource': R.SHEEP,
        'quanitity': 1
    }],
    'city': [{
        'resource': R.HAY,
        'quanitity': 2
    },
    {
        'resource': R.ROCK,
        'quanitity': 3
    }],
    'development': [{
        'resource': R.HAY,
        'quanitity': 1
    },
    {
        'resource': R.SHEEP,
        'quanitity': 1
    },
    {
        'resource': R.ROCK,
        'quanitity': 1
    }]
}

# NUM_TURNS = 1

# rolls = {}

# for i in range(2, 13):
#     rolls[i] = 0

# for i in range(NUM_TURNS):
#     roll = random.randint(1, 6) + random.randint(1, 6)
#     rolls[roll] += 1
#     for resource, num in [item for sublist in board for item in sublist]:
#         if roll == num:
#             totals[resource] += 1

# print("Average resource per turn:")
# print([(resource, total / float(NUM_TURNS)) for resource, total in totals.items()])

# print(rolls)

# 3 characters wide
def tile(row, column):
    return f"{board[row][column][0].name[0]}{board[row][column][1]:2}"

num_dots = {
    0: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 6,
    7: 0,
    8: 6,
    9: 4,
    10: 3,
    11: 2,
    12: 1
}

fmt_dots = {
  0: '   ',
  1: ' . ',
  2: '. .',
  3: '...',
  4: ': :',
  6: ':::'
}

def dots(row, column):
    return fmt_dots[num_dots[board[row][column][1]]]


"""
Coordinate system for hexagons:

first, third, and fifth rows count off by 2s

0:  2 4 6
1: 1 3 5 7
2:0 2 4 6 8
3: 1 3 5 7
4   2 4 6
  012345678
"""

spaces = [
    [None, None, None, None, None, None, None],
    [None, None, '1@', None, None, None, None, '4@', None],
    [None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, '2@', None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, '3@', None],
    [None, None, None, None, None, None, None],
]

# roads are marked as between two spaces, e.g.
# row1, col1, row2, col2
(0, 1, 0, 2)

player_colors = color = {
    '1': Fore.RED,
    '2': Fore.CYAN,
    '3': Fore.MAGENTA,
    '4': Fore.YELLOW,
}

def spce(r, c):
    if spaces[r][c] is None:
        return " "
    return player_colors[spaces[r][c][0]] + spaces[r][c][1] + Style.RESET_ALL

board_string = rf"""
                  /{spce(0,1)}\         /{spce(0,3)}\         /{spce(0,5)}\
                /     \     /     \     /     \
             {spce(0,0)}/         \{spce(0,2)}/         \{spce(0,4)}/         \{spce(0,6)}
             |           |           |           |
             |    {tile(0, 0)}    |    {tile(0, 1)}    |    {tile(0, 2)}    |
             |    {dots(0, 0)}    |    {dots(0, 1)}    |    {dots(0, 2)}    |
            /{spce(1,1)}\         /{spce(1,3)}\         /{spce(1,5)}\         /{spce(1,7)}\
          /     \     /     \     /     \     /     \
       {spce(1,0)}/         \{spce(1,2)}/         \{spce(1,4)}/         \{spce(1,6)}/         \{spce(1,8)}
       |           |           |           |           |
       |    {tile(1, 0)}    |    {tile(1, 1)}    |    {tile(1, 2)}    |    {tile(1, 3)}    |
       |    {dots(1, 0)}    |    {dots(1, 1)}    |    {dots(1, 2)}    |    {dots(1, 3)}    |
      /{spce(2,1)}\         /{spce(2,3)}\         /{spce(2,5)}\         /{spce(2,7)}\         /{spce(2,9)}\
    /     \     /     \     /     \     /     \     /     \
 {spce(2,0)}/         \{spce(2,2)}/         \{spce(2,4)}/         \{spce(2,6)}/         \{spce(2,8)}/         \{spce(2,10)}
 |           |           |           |           |           |
 |    {tile(2, 0)}    |    {tile(2, 1)}    |    {tile(2, 2)}    |    {tile(2, 3)}    |    {tile(2, 4)}    |
 |    {dots(2, 0)}    |    {dots(2, 1)}    |    {dots(2, 2)}    |    {dots(2, 3)}    |    {dots(2, 4)}    |
 {spce(3,0)}\         /{spce(3,2)}\         /{spce(3,4)}\         /{spce(3,6)}\         /{spce(3,8)}\         /{spce(3,10)}
    \     /     \     /     \     /     \     /     \     / 
      \{spce(3,1)}/         \{spce(3,3)}/         \{spce(3,5)}/         \{spce(3,7)}/         \{spce(3,9)}/
       |           |           |           |           |
       |    {tile(3, 0)}    |    {tile(3, 1)}    |    {tile(3, 2)}    |    {tile(3, 3)}    |
       |    {dots(3, 0)}    |    {dots(3, 1)}    |    {dots(3, 2)}    |    {dots(3, 3)}    |
       {spce(4,0)}\         /{spce(4,2)}\         /{spce(4,4)}\         /{spce(4,6)}\         /{spce(4,8)}
          \     /     \     /     \     /     \     /
            \{spce(4,1)}/         \{spce(4,3)}/         \{spce(4,5)}/         \{spce(4,7)}/
             |           |           |           |
             |    {tile(4, 0)}    |    {tile(4, 1)}    |    {tile(4, 2)}    |
             |    {dots(4, 0)}    |    {dots(4, 1)}    |    {dots(4, 2)}    |
             {spce(5,0)}\         /{spce(5,2)}\         /{spce(5,4)}\         /{spce(5,6)}
                \     /     \     /     \     /
                  \{spce(5,1)}/         \{spce(5,3)}/         \{spce(5,5)}/
"""

print(board_string)

space_tile_lookup = [
    [[(0,0)], [(0,0)], [(0,0),(0,1)], [(0,1)], [(0,1),(0,2)], [(0,2)], [(0,2)]],
    [[(1,0)], [(1,0),(0,0)], [(0,0),(1,0),(1,1)], [(0,0),(1,1),(0,1)], [(1,1),(0,1),(1,2)], [(0,1),(1,2),(0,2)], [(1,2),(0,2),(1,3)], [(0,2),(1,3)], [(1,3)]],
    [[(2,0)], [(2,0),(1,0)], [(1,0),(2,0),(2,1)], [(2,0),(2,1),(1,1)], [(2,1),(2,2),(1,1)], [(1,1),(1,2),(2,2)], [(2,2),(2,3),(1,2)], [(1,2),(1,3),(2,3)], [(2,3),(2,4),(1,3)], [(1,3),(2,4)], [(2,4)]],
    [[(2,0)], [(2,0),(3,0)], [(2,0),(3,0),(2,1)], [(3,0),(3,1),(2,1)], [(2,1),(2,2),(3,1)], [(3,1),(3,2),(2,2)], [(2,2),(2,3),(3,2)], [(3,2),(3,3),(2,3)], [(2,3),(2,4),(3,3)], [(2,4),(3,3)], [(2,4)]],
    [[(3,0)], [(3,0),(4,0)], [(3,0),(4,0),(3,1)], [(4,0),(4,1),(3,1)], [(3,1),(3,2),(4,1)], [(4,1),(4,2),(3,2)], [(3,2),(3,3),(4,2)], [(3,3),(4,2)], [(3,3)]],
    [[(4,0)], [(4,0)], [(4,0),(4,1)], [(4,1)], [(4,1),(4,2)], [(4,2)], [(4,2)]],
]

score_map = {

}

for r, row in enumerate(spaces):
    for c, col in enumerate(row):
        tiles = space_tile_lookup[r][c]
        total = 0
        for tile in tiles:
            r1, c1 = tile
            total += num_dots[board[r1][c1][1]]
        if total not in score_map:
            score_map[total] = []

        score_map[total].append((r, c))

# pprint.pprint(score_map)