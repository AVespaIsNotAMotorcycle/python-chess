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
    for piece in pieces:
      if piece.getteam() == self.team:
        ownedpieces.append(piece)
    # Randomly order owned pieces
    piecequeue = []
    while len(ownedpieces) > 0:
      i = random.randrange(len(ownedpieces))
      p = ownedpieces[i]
      piecequeue.append(p)
      ownedpieces.pop(i)
    # Interpret piece moves
    while len(piecequeue) > 0:
      p = piecequeue[0]
      s = p.getcoords()
      moves = interpretmoves(s,p.getmoves())
      while len(moves) > 0:
        i = random.randrange(len(moves))
        mv = moves[i]
        if board.moveisvalid(s,mv,p):
          return coordtoal(s) + ' ' + coordtoal(mv)
        moves.pop(i)
      piecequeue.pop(0)
    return 'concede'

  def promotepiece(self, board):
    possible_promos = [
      'Queen',
      'Rook',
      'Bishop',
      'Knight'
    ]
    return possible_promos[random.randrange(0,len(possible_promos))]
