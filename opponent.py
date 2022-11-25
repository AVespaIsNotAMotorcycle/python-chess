from utils import coordtoal
import random

'''
Default Opponent class
Returns a random move
Other opponents may be smarter
'''
class Opponent:

  def __init__(self, team):
    self.team = team

  # makemove(board, board.pieces)
  # returns [s, d, p] where
  # s is tuple [x, y] representing the coords of a piece
  # d is tuple [x, y] representing the coords of a destination
  # p is Piece located at s
  def makemove(self, board, pieces):
    # Prune enemy pieces
    ownedpieces = []
    for piece in pieces:
      if piece.getteam() == self.team:
        ownedpieces.append(piece)

    # Pick owned piece at random
    piece = ownedpieces[random.randrange(0, len(ownedpieces))]

    # Try moves at random
    s = piece.getcoords()
    moves = piece.getmoves()
    while len(moves) > 0:
      move = moves[random.randrange(0, len(moves))]
      d_x = move[0]
      d_y = move[1]
      # If a move may be of variable distance,
      # convert it into a finite set of moves
      # with constant distances
      if d_x == 'x' or d_y == 'x':
        deltarange = range(9)
        for delta in deltarange:
          if d_x == 'x' and d_y == 'x':
            moves.append((delta, delta))
          if d_x == 'x':
            moves.append((delta, d_y))
          if d_y == 'y':
           moves.append((d_x, delta))
        # Remove the variable distance move and try again
        moves.remove(move)
        continue
      # Check that the move is valid
      d = (s[0] + d_x, s[1] + d_y)
      if board.moveisvalid(s, d, board.fetchpiece(s)[1]):
        print('Moving ' + piece.getname() + ' from ' + str(s) + ' ' + str(d))
        return coordtoal(s) + ' ' + coordtoal(d)
      moves.remove(move)
    # None are valid, start again
    return self.makemove(board, pieces)

  def promotepiece(self, board):
    possible_promos = [
      'Queen',
      'Rook',
      'Bishop',
      'Knight'
    ]
    return possible_promos[random.randrange(0,len(possible_promos))]
