from board import alg_to_coords

print('Input a move:')
move = input()
alg1 = move[0:2]
alg2 = move[3:]
coords1 = alg_to_coords(alg1)
coords2 = alg_to_coords(alg2)
print(coords1, coords2)
