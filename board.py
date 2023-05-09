def index_to_coords(index):
  y = int(index / 8 - 0.1) + 1
  x = index - ((y - 1) * 8)
  return (x, y)

def coords_to_index(coords):
  x = coords[0]
  y = (coords[1] - 1) * 8
  return x + y

def int_to_char(int): return chr(int + 96)

def char_to_int(char): return ord(char) - 96

def alg_to_coords(alg): return (char_to_int(alg[0]), int(alg[1]))

def coords_to_alg(coords): return int_to_char(coords[0]) + str(coords[1])
