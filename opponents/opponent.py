from utils import coordtoal, interpretmoves
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
  # returns s + ' ' + d where
  # s is a len 2 string representing the coords of a piece
  # d is a len 2 string representing the coords of a destination
  # both s and d are in algebraic notation
  def makemove(self, board, pieces):
    # Prune enemy pieces
    ownedpieces = []
    # print('---- owned pieces ----')
    for piece in pieces:
      if piece.getteam() == self.team:
        # print(piece.getname())
        ownedpieces.append(piece)
    while len(ownedpieces) > 0:
      pieceindex = random.randrange(0, len(ownedpieces))
      piece = ownedpieces[pieceindex]
      start = piece.getcoords()
      moves = interpretmoves(start, piece.getmoves())
      while len(moves) > 0:
        moveindex = random.randrange(0, len(moves))
        move = moves[moveindex]

        startstring = '(' + str(start[0]) + ', ' + str(start[1]) + ')'
        movestring = '(' + str(move[0]) + ', ' + str(move[1]) + ')'
        # print('trying to move ' + piece.getname() + ' from ' + startstring + ' to ' + movestring)
        if (board.moveisvalid(start, move, piece)):
          return coordtoal(start) + ' ' + coordtoal(move)
        moves.pop(moveindex)
      ownedpieces.pop(pieceindex)
    return 'concede'

  def promotepiece(self, board):
    possible_promos = [
      'Queen',
      'Rook',
      'Bishop',
      'Knight'
    ]
    return possible_promos[random.randrange(0,len(possible_promos))]
