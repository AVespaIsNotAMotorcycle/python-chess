def DEFAULT_SETTINGS():
  default_settings = {
    'observing': 'None',
    'opponent': 'None',
    'playercolor': 'None',
    'players': {
      'white': 'human',
      'black': 'human',
    }
  }
  return default_settings

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
