from opponents.opponent import Opponent
from utils import coordtoal, interpretmoves
from copy import deepcopy
import time

class OppBoardStateHeuristic(Opponent):
  def __init__(self, team):
    self.team = team
    self.time_generating_moves = 0
    self.time_pruning_moves = 0
    self.time_searching_frontier = 0

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

  # utility(pieces) where
  # pieces is a list of extant pieces
  # returns u, where u is an evaluation of the
  # utility of that gamestate
  def utility(self, pieces):
    u = 0
    for piece in pieces:
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
    start = time.time()
    possiblemoves = []
    for piece in ownedpieces:
      piecemoves = piece.getmoves()
      s = piece.getcoords()
      imoves = interpretmoves(s,piecemoves)
      for move in imoves:
        possiblemoves.append((piece,move))
    end = time.time()
    self.time_generating_moves += end - start

    # Prune invalid moves
    start = time.time()
    prunedmoves = []
    for move in possiblemoves:
      p = move[0].copy()
      s = p.getcoords()
      d = move[1]
      if not board.moveisvalid(s, d, p):
        continue
      if board.resultsincheck(s, d, p):
        continue  
      prunedmoves.append(move)
    end = time.time()
    self.time_pruning_moves += end - start

    # Create frontier of possible boardstates
    # Contains tuples of form (Move, Value) where
    # Move is the move that would be made and
    # Value is the utility of the resulting boardstate
    start = time.time()
    frontier = []
    for move in prunedmoves:
      p = move[0].copy()
      s = p.getcoords()
      d = move[1]
      mockpieces = board.mockmove(s,d,p)
      u = 0
      if board.mockplayerincheck(mockpieces, self.team):
        u = -1000
      elif board.mockplayerincheck(mockpieces, 3 - self.team):
        u = 1000
      else:
        u = self.utility(mockpieces)
      frontier.append(((s, d), u))
    end = time.time()
    self.time_searching_frontier += end - start

    print(f'Time generating moves: {self.time_generating_moves * 1000} ms')
    print(f'Time pruning: {self.time_pruning_moves * 1000} ms')
    print(f'Time searching frontier: {self.time_searching_frontier * 1000} ms')
    # If no valid moves, concede
    if len(frontier) == 0:
      return 'concede'

    # Return move that produces highest utility
    beststate = frontier[0]
    for state in frontier:
      if state[1] > beststate[1]:
        beststate = state
    
    return coordtoal(beststate[0][0]) + ' ' + coordtoal(beststate[0][1])
