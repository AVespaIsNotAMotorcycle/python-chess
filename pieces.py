names = [
  'None',
  'King',
  'Queen',
  'Bishop',
  'Knight',
  'Rook',
  'Pawn',
]
def piecename(number):
  if number > 6: return 'Black ' + names[number - 6]
  return 'White ' + names[number]

symbols = [
  ' ',
  'K',
  'Q',
  'B',
  'N',
  'R',
  'P',
]
def piecesymbol(number):
  if number > 6: return symbols[number - 6].lower()
  return symbols[number]

moves = [
  [],
  [ # King
    (-1, 1), (0, 1), (1, 1),
    (-1, 0),         (1, 0),
    (-1,-1), (0, -1),(1,-1),
  ],
  [ # Queen
    ('x','x'), ('x', '-x'), (0, 'x'), ('x', 0),
  ],
  [ # Bishop
    ('x', 'x'), ('x', '-x'),
  ],
  [ # Knight
    (-3, 2), (-2, 3), (2, 3), (3, 2),
    (-3,-2), (-2,-3), (2,-3), (3,-2),
  ],
  [ # Rook
    (0,'x'), ('x',0),
  ],
  [ # Pawn
  ],
]
def pawnmoves(number, location):
  if number > 6: return [(0, -1)]
  return [(0, 1)]

def piecemoves(number, location = -1):
  if number == 6 or number == 12: return pawnmoves(number, location)
  moveset = []
  if number > 6: moveset = moves[number - 6]
  else: moveset = moves[number]
  moves_to_remove = []
  for move in moveset:
    x_is_variable = move[0] == 'x' or move[0] == '-x'
    y_is_variable = move[1] == 'x' or move[1] == '-x'
    if x_is_variable or y_is_variable:
      sign_x = ((move[0] == 'x') * 2 - 1) * x_is_variable
      sign_y = ((move[1] == 'x') * 2 - 1) * y_is_variable
      for i in range(1, 9):
        constant_move_positive = (i * sign_x, i * sign_y)
        constant_move_negative = (i * -sign_x, i * -sign_y)
        moveset.append(constant_move_positive)
        moveset.append(constant_move_negative)
      moves_to_remove.append(move)
  for move in moves_to_remove:
    moveset.remove(move)
  return moveset

print(piecename(12), piecemoves(12))
'''
for i in range(13):
  print(piecename(i), piecemoves(i))
'''
