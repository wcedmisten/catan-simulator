import random
from enum import Enum
from colorama import Fore
from colorama import Back
from colorama import Style

import os

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
          [None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None],
]

def is_adjacent_space(r1, c1, r2, c2):
    row_offset_map = {
        0: 2,
        1: 1,
        2: 0,
        3: 0,
        4: 1,
        5: 2
    }

    if abs(c1 - c2) <= 1 and r1 == r2:
        return True

    offset_c1 = c1 + row_offset_map[r1]
    offset_c2 = c2 + row_offset_map[r2]

    # print(offset_c1, offset_c2, r1, r2)

    if abs(r1 - r2) <= 1 and offset_c1 == offset_c2:
        return True

    return False

# print(is_adjacent_space(2, 0, 3, 0))
# print(is_adjacent_space(0, 1, 0, 2))
# print(is_adjacent_space(0, 0, 1, 1))
# print(is_adjacent_space(0, 0, 2, 1))
# print(is_adjacent_space(0, 1, 1, 2))
# print(is_adjacent_space(0, 2, 1, 3))

# roads are marked as between two spaces, e.g.
# row1, col1, row2, col2
# (0, 1, 0, 2)

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

def dots(row, column):
    return tile_colors[board[row][column][0]] + fmt_dots[num_dots[board[row][column][1]]] + Style.RESET_ALL


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

def can_place(row, col):
    for r, row1 in enumerate(spaces):
        for c, col1 in enumerate(row1):
            if spaces[r][c] and is_adjacent_space(r, c, row, col):
                return False
            
    return True

tile_colors = {
    R.ROCK: Fore.WHITE,
    R.SHEEP: Fore.GREEN,
    R.WOOD: Fore.BLUE,
    R.BRICK: Fore.RED,
    R.HAY: Fore.MAGENTA,
    R.DESERT: Fore.YELLOW
}

# 3 characters wide
def tile(row, column):
    resource = board[row][column][0]
    quantity = board[row][column][1]
    return tile_colors[resource] + f"{resource.name[0]}{quantity:2}" + Style.RESET_ALL
            
def board_string():
    return rf"""
    Legend: Player 1: {player_colors['1'] + '@' + Style.RESET_ALL}  {tile_colors[R.BRICK]}[B]rick{Style.RESET_ALL}
            Player 2: {player_colors['2'] + '@' + Style.RESET_ALL}  {tile_colors[R.SHEEP]}[S]heep{Style.RESET_ALL}
            Player 3: {player_colors['3'] + '@' + Style.RESET_ALL}  {tile_colors[R.WOOD]}[W]ood{Style.RESET_ALL}
            Player 4: {player_colors['4'] + '@' + Style.RESET_ALL}  {tile_colors[R.HAY]}[H]ay{Style.RESET_ALL}
                         {tile_colors[R.ROCK]}[R]ock{Style.RESET_ALL}
                         {tile_colors[R.DESERT]}[D]esert{Style.RESET_ALL}

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


player_order = ['1', '2', '3', '4', '4', '3', '2', '1']

print(board_string())
input("Waiting for user input...")

for player in player_order:
    best = sorted(score_map.items(), reverse=True)

    for key, val in best:
        # print(key, val)

        if len(val) == 0:
            score_map.pop(key, None)
            continue

        r, c = val.pop(0)
        if can_place(r, c):
            spaces[r][c] = player + "@"
            os.system('clear')
            print(f"Placing player: {player}")
            print(board_string())
            input("Waiting for user input...")
            break
        # else:
            # print("Could not place", r, c)

rolls = {}

player_resources = {
    '1': {
        R.WOOD: 0,
        R.SHEEP: 0,
        R.HAY: 0,
        R.ROCK: 0,
        R.BRICK: 0
    },
    '2': {
        R.WOOD: 0,
        R.SHEEP: 0,
        R.HAY: 0,
        R.ROCK: 0,
        R.BRICK: 0
    },
    '3': {
        R.WOOD: 0,
        R.SHEEP: 0,
        R.HAY: 0,
        R.ROCK: 0,
        R.BRICK: 0
    },
    '4': {
        R.WOOD: 0,
        R.SHEEP: 0,
        R.HAY: 0,
        R.ROCK: 0,
        R.BRICK: 0
    }
}


NUM_TURNS = 10000

for i in range(NUM_TURNS):
    roll = random.randint(1, 6) + random.randint(1, 6)

    for r, row in enumerate(spaces):
        for c, col in enumerate(row):
            if col:
                player = col[0]
                tiles = space_tile_lookup[r][c]
                for tile_row, tile_col in tiles:
                    resource = board[tile_row][tile_col][0]
                    if roll == board[tile_row][tile_col][1]:
                        player_resources[player][resource] += 1

print("Average resource per turn:")
for key, val in player_resources.items():
    print("player", key)
    total = 0
    for resource, qty in val.items():
        print(resource, qty / float(NUM_TURNS))
        total += qty / float(NUM_TURNS)
    print("Total: ", total)
    print()

# pprint.pprint(player_resources)