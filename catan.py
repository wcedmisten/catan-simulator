import random
from enum import Enum
from colorama import Fore
from colorama import Style

import itertools

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

board_string = rf"""

                  / \         / \         / \
                /     \     /     \     /     \
              /         \ /         \ /         \
             |           |           *           |
             |    {tile(0, 0)}    |    {tile(0, 1)}    |    {tile(0, 2)}    |
             |    {dots(0, 0)}    |    {dots(0, 1)}    |    {dots(0, 2)}    |
            / \         / \         / \         / \
          /     \     /     \     /     \     /     \
        /         \ /         \ /         \ /         \
       |           |           |           |           |
       |    {tile(1, 0)}    |    {tile(1, 1)}    |    {tile(1, 2)}    |    {tile(1, 3)}    |
       |    {dots(1, 0)}    |    {dots(1, 1)}    |    {dots(1, 2)}    |    {dots(1, 3)}    |
      / \         / \         / \         / \         / \
    /     \     /     \     /     \     /     \     /     \
  /         \ /         \ /         \ /         \ /         \
 |           |           |           |           |           |
 |    {tile(2, 0)}    |    {tile(2, 1)}    |    {tile(2, 2)}    |    {tile(2, 3)}    |    {tile(2, 4)}    |
 |    {dots(2, 0)}    |    {dots(2, 1)}    |    {dots(2, 2)}    |    {dots(2, 3)}    |    {dots(2, 4)}    |
  \         / \         / \         / \         / \         /
    \     /     \     /     \     /     \     /     \     / 
      \ /         \ /         \ /         \ /         \ /
       |           |           |           |           |
       |    {tile(3, 0)}    |    {tile(3, 1)}    |    {tile(3, 2)}    |    {tile(3, 3)}    |
       |    {dots(3, 0)}    |    {dots(3, 1)}    |    {dots(3, 2)}    |    {dots(3, 3)}    |
        \         / \         / \         / \         /
          \     /     \     /     \     /     \     /
            \ /         \ /         \ /         \ /
             |           |           |           |
             |    {tile(4, 0)}    |    {tile(4, 1)}    |    {tile(4, 2)}    |
             |    {dots(4, 0)}    |    {dots(4, 1)}    |    {dots(4, 2)}    |
              \         / \         / \         /
                \     /     \     /     \     /
                  \ /         \ /         \ /
"""

print(board_string)


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

# idx_from_coordinates = {

# }


# def board_column(row, idx):
#     col = [[2, 4, 6], [1, 3, 5, 7], [0, 2, 4, 6, 8], [1, 3, 5, 7], [2, 4, 6]][row][idx]
#     idx_from_coordinates[(row, col)] = idx
#     return [[2, 4, 6], [1, 3, 5, 7], [0, 2, 4, 6, 8], [1, 3, 5, 7], [2, 4, 6]][row][idx]

# # store all valid tile coordinates
# board_coordinate_set = set()
# for i in range(5):
#     for j in range(5):
#         try:
#          board_coordinate_set.add((i, board_column(i, j)))
#         except Exception:
#             pass

# # store pair of neighbors being compared to find the best space
# visited = set()


# def are_neigbors(r1, c1, r2, c2):
#     return (abs(r1 - r2) <= 1 and abs(c1 - c2) <= 1) or (r1 == r2 and abs(c1 - c2) <= 2)


# def find_neighbors(x, y):
#     neighbors = set()
#     for r,c in (board_coordinate_set - set({(y, x)})):
#         if are_neigbors(y, x, r, c):
#             neighbors.add((r, c))
#     return neighbors

# spot_scores = {}

# for r,c in board_coordinate_set:    
#     total_dots = 0
#     idx = idx_from_coordinates[(r, c)]
#     print(r, c, idx, num_dots[board[r][idx][1]])
#     neighbors = find_neighbors(c, r)
#     print(neighbors)
#     mutual_neighbors = set()
#     for n1, n2 in list(itertools.combinations(neighbors, 2)):
#         if are_neigbors(n1[0], n1[1], n2[0], n2[1]):
#             mutual_neighbors.add((n1, n2))

#     print(mutual_neighbors)
#     print("~~~~~~~~")

