from opponents.opponent import Opponent
from utils import coordtoal
from copy import deepcopy

class OppBoardStateHeuristic(Opponent):
  def __init__(self, team):
    self.team = team

  # takes a coordinate pair (x, y)
  # and returns the utility of occupying that tile
  @staticmethod
  def coordtoutil(x,y):
    x_u = x
    if x_u >= 5:
      x_u = 5 - (x_u - 4)
    y_u = y
    if y_u >= 5:
      y_u = 5 - (y_u - 4)
    return x_u * y_u

  # utility((pieces), matestatus) where
  # pieces is a list of extant pieces
  # and matestatus is a string of value
  # none || self_check || self_mate || opp_check || opp_mate
  # returns u, where u is an evaluation of the
  # utility of that gamestate
  def utility(self, gamestate):
    pieces = gamestate[0]
    matestatus = gamestate[1]
    u = 0
    if matestatus == 'self_check':
      return -1000
    if matestatus == 'self_mate':
      return -1000
    if matestatus == 'opp_check':
      return 1000
    if matestatus == 'opp_mate':
      return 2000
    for piece in gamestate:
      tile = piece.getcoords()
      tile_util = self.coordtoutil(tile[0], tile[1])
      tile_util = tile_util * piece.getpoints()
      team_mod = 1
      if piece.getteam() != self.team:
        team_mod = -1
      tile_util = tile_util * team_mod
      u += tile_util
    return u

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

    # List possiblemoves
    # Contains tuples of form (Piece, Move) where
    # Piece is a Piece and
    # Move is a tuple of form (x, y) representing
    # a possible destination
    possiblemoves = []
    for piece in ownedpieces:
      piecemoves = piece.getmoves()
      s = piece.getcoords()
      for move in piecemoves:
        # Handle moves of variable distance
        if move[0] == 'x' or move[1] == 'x':
          deltarange = range(1, 9)
          for delta in deltarange:
            if move[0] == 'x' and move[1] == 'x':
              d = (s[0] + delta, s[1] + delta)
              possiblemoves.append((piece, d))
            elif move[0] == 'x':
              d = (s[0] + delta, s[1] + move[1])
              possiblemoves.append((piece, d))
            elif move[1] == 'x':
              d = (s[0] + move[0], s[1] + delta)
              possiblemoves.append((piece, d))
        else:
          d = (s[0] + move[0], s[1] + move[1])
          possiblemoves.append((piece, d))

    # Prune invalid moves
    prunedmoves = []
    for move in possiblemoves:
      p = deepcopy(move[0])
      s = p.getcoords()
      d = move[1]
      if board.moveisvalid(s, d, p):
        prunedmoves.append(move)

    # Create frontier of possible boardstates
    # Contains tuples of form (Move, Value) where
    # Move is the move that would be made and
    # Value is the utility of the resulting boardstate
    frontier = []
    for move in prunedmoves:
      p = deepcopy(move[0])
      s = p.getcoords()
      d = move[1]
      u = self.utility(board.mockmove(s,d,p))
      frontier.append(((s, d), u))

    # Return move that produces highest utility
    beststate = frontier[0]
    for state in frontier:
      if state[1] > beststate[1]:
        beststate = state
    return coordtoal(beststate[0][0]) + ' ' + coordtoal(beststate[0][1])
