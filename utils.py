def DEFAULT_SETTINGS():
  default_settings = {
    'observing': 'None',
    'opponent': 'None',
    'playercolor': 'None',
    'players': {
      'white': 'human',
      'black': 'human',
    },
    'maxturns': 200
  }
  return default_settings

def AI_LIST():
  ai_list = [
    'random',
    'boardstate_heuristic',
  ]
  return ai_list

# converts chessboard notation to coordinates
def altocoord(i):
  # check that i is str of len 2
  if len(i) != 2:
    return False
  # check that i[0] is a letter
  if i[0].isalpha() == False:
    return False
  # check that i[1] is a number
  if i[1].isdecimal() == False:
    return False
  return (ord(i[0]) - 96,int(i[1]))

# converts coordinates to chessboard notation
def coordtoal(i):
  x = chr(i[0] + 96)
  y = str(i[1])
  return x + y

def inboard(coords):
  if coords[0] < 0 or coords[0] > 7:
    return False
  if coords[1] < 0 or coords[1] > 7:
    return False
  return True

# s : (x,y) start position
# moves : list of moves
def interpretmoves(s,moves):
  interpretedmoves = []
  for mv in moves:
    # Variable distance moves
    if mv[0] == 'x' or mv[1] == 'x':
      for delta in range(1,9):
        newx = delta
        newy = delta
        if mv[0] == 'x' and mv[1] == 'x':
          interpretedmoves.append((newx, newy))
        elif mv[0] == 'x':
          interpretedmoves.append((newx, s[1] + mv[1]))
        else:
          interpretedmoves.append((s[0] + mv[0], newy))
        continue
    # Constant distance moves
    else:
      cd = (s[0] + mv[0], s[1] + mv[1])
      interpretedmoves.append(cd)
  return interpretedmoves
