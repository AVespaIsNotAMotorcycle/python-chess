from utils import DEFAULT_SETTINGS, altocoord, coordtoal
from piece import Piece
from opponents.utils import create_opponent
from copy import deepcopy
import numpy

class Board:

  def __init__(self, pieces, settings = DEFAULT_SETTINGS().copy()):
      self.pieces = pieces
      self.settings = settings
      # A log of all moves made on this board
      # (s, d, p)
      self.moves = []

  # render() method
  # outputs board state to console
  def render(self):
    s = ''
    s += '# a b c d e f g h #\n'
    s += '1 -   -   -   -   #\n'
    s += '2   -   -   -   - #\n'
    s += '3 -   -   -   -   #\n'
    s += '4   -   -   -   - #\n'
    s += '5 -   -   -   -   #\n'
    s += '6   -   -   -   - #\n'
    s += '7 -   -   -   -   #\n'
    s += '8   -   -   -   - #\n'
    s += '# # # # # # # # # #\n'
    for piece in self.pieces:
      i = self.coordstoindex(piece.getcoords())
      a = s[0:i]
      p = s[i + 1:]
      s = a + piece.geticon() + p
    print(s)

  # fetchpiece(c)
  # takes a scalar c = (x,y)
  # where x and y are both integers 0 - 9
  # and return any piece found at those coords
  def fetchpiece(self, c):
    for piece in self.pieces:
      if piece.getcoords() == c:
        return piece
    return 'none'

  # moveinrange(s,d,p)
  # s: scalar (x,y) representing starting tile
  # d: scalar (x,y) representing destination tile
  # p: Piece to be moved
  def moveinrange(self,s,d,p):
    # Check that s and d are within the board limits
    bounds = [s[0],s[1],d[0],d[1]]
    for bound in bounds:
      if bound < 1 or bound > 8:
        return False
    moves = p.getmoves()
    for mv in moves:
      # Variable distance moves
      if mv[0] == 'x' or mv[1] == 'x':
        for delta in range(1,9):
          if mv[0] == 'x' and mv[1] == 'x':
            moves.append((delta,delta))
          elif mv[0] == 'x':
            moves.append((delta,mv[1]))
          else:
            moves.append((mv[0],delta))
          continue
      # Constant distance moves
      else:
        comp_d = (s[0] + mv[0], s[1] + mv[1])
        if comp_d == d:
          return True
    return False

  # moveunobstructed(s,d)
  # checks whether there are any pieces blocking
  # the path from s to d
  def moveunobstructed(self,s,d,v):
    delta = (d[0] - s[0], d[1] - s[1])
    # Knights cannot be obstructed
    if delta[0] != delta[1] and not (delta[0] == 0 or delta[1] == 0):
      return True
    # don't want full distance, as we aren't looking at tile d, since an enemy piece there isn't an obstruction
    distance = max(delta[0], delta[1]) - 1
    if distance == 0:
      return True
    for i in range(1,distance):
      nx = 0
      ny = 0
      if delta[0] > 0:
        nx = i
      if delta[1] > 0:
        ny = i
      nd = (s[0] + nx, s[1] + ny)
      if self.fetchpiece(nd) != 'none':
        return False
    return True

  # cancapture(s,d,p)
  # s: scalar (x,y) representing starting tile
  # d: scalar (x,y) representing destination tile
  # p: piece to be moved
  # Returns bool indicating whether d is occupied by
  # a friendly piece
  # Does not factor in whether the piece can actually
  # otherwise move to that tile
  def cancapture(self,s,d,p):
    dpiece = self.fetchpiece(d)
    if dpiece == 'none':
      return True
    if dpiece.getteam() != p.getteam():
      return True
    return False

  # castling banned for now :)
  def isvalidcastle(self, start, destination, piece):
    return False

  # A valid capture must be
  # - diagonal
  # - of distance 1
  # - in the vertical direction of a normal move
  # An enpassent capture is legal if
  # - an enemy pawn is directly adjacent to this pawn
  # - that pawn just moved 2 tiles
  def validpawncapture(self,s,d,p):
    # Check that move is valid
    sign = numpy.sign(p.getmoves()[0][1])
    delta = (d[0] - s[0], d[1] - s[1])
    # If travelling in wrong vertical direction
    # or distance travelled > 1
    if delta[1] != sign:
      return False
    # If horizontal distance != 1
    if not (delta[0] == 1 or delta[0] == -1):
      return False
    # If piece at d, return True
    if self.fetchpiece(d) != 'none':
      return True
    # If not piece at d, check if enpassent is valid
    # Last moved piece must have been an enemy pawn
    if self.moves[-1][2].getname() != 'Pawn':
      return False
    # Enemy pawn piece must have moved 2 tiles
    if abs(self.moves[-1][0][1] - self.moves[-1][1][1]) != 2:
      return False
    # Enemy pawn must have moved adjacent to this pawn
    left = self.fetchpiece((s[0] - 1, s[1]))
    right = self.fetchpiece((s[0] + 1, s[1]))
    if not (left == self.moves[-1][2] or right == self.moves[-1][2]):
      return False
    return True

  # validcastle(s,d,p)
  def validcastle(self,s,d,p):
    return False

  # moveisvalid(s,d,p)
  # takes a scalar s, the start coords
  # and a scalar d, the destination coords
  # and a piece p, the piece being moved
  # and a bool c, True by default, which determines
  # whether to check if the move would put you in check
  # returns true if a piece would be allowed to make the move
  def moveisvalid(self, s, d, p, c = True):
    # Check that move is in range
    inrange = self.moveinrange(s,d,p)
    if not inrange and not (p.getname() == 'King' or p.getname() == 'Pawn'):
      # Pawn captures and castline would both
      # be legal but not inrange
      return False

    # Check that the target tile is either empty
    # or contains a capturable piece
    cancapture = self.cancapture(s,d,p)
    isvalidcastle = self.isvalidcastle(s,d,p)
    if not cancapture and not isvalidcastle:
      # For kings, castling is an exception,
      # as, to make input simpler, I'm breaking from
      # algebraic notation for castling input
      # algebraic notation is o-o or o-o-o,
      # but that's annoying to parse
      return False

    # Check that there is no piece blocking the path
    moveunobstructed = self.moveunobstructed(s,d,True)
    if not moveunobstructed:
      return False

    # If piece is pawn, check whether it is capturing a piece
    # and if it is a valid capture
    if p.getname() == 'Pawn' and not inrange:
      pawncancapture = self.validpawncapture(s,d,p)
      if not pawncancapture:
        return False

    # If piece is king, check whether it is castling
    # and if it is a valid castle
    if p.getname() == 'King' and not inrange:
      validcastle = self.validcastle(s,d,p)
      if not validcastle:
        return False

    # Check that move does not result in check
    if c:
      if self.resultsincheck(s,d,p):
        return False

    return True

    # who knows!?
  def handlecastle(self, s, d, p):
    return

  def handleenpassent(self, s, d, p):
    return

  def handlepromo(self, s, d, p):
    return

  # movepiece(s,d,p)
  # takes a scalar s, the start coords
  # and a scalar d, the destination coords
  # and a piece p, the piece being moved
  # I wrote this and its constituent functions
  # a year ago all as one function. I've broken
  # them up but I do not understand them.
  def movepiece(self, s, d, p):
    self.moveunobstructed(s,d,True)
    # Castling
    # Enpassent
    # Enact move
    targetpiece = self.fetchpiece(d)
    if targetpiece != 'none':
      self.pieces.remove(targetpiece)
    self.moves.append((s,d,p))
    p.setcoords(d)
    # Remove pawn 2 tile move
    if p.getname() == 'Pawn':
      if p.moves.count((0,2)) > 0:
        p.moves.remove((0,2))
      if p.moves.count((0,-2)) > 0:
        p.moves.remove((0,-2))
    # Pawn Promotion
    return

  # mockmove(s,d,p)
  # creates a new board and returns
  # that board's pieces after performing
  # a move
  def mockmove(self,s,d,p):
    mockboard = Board(deepcopy(self.getpieces()))
    np = mockboard.fetchpiece(s)
    mockboard.movepiece(s,d,np)
    return mockboard.getpieces()

  # resultsincheck(s,d,p) method
  # computes an otherwise valid move
  # to see if it would result in that
  # player being in check
  def resultsincheck(self,s,d,p):
    # Find king
    k = self.pieces[0]
    for piece in self.pieces:
      if piece.getname() == 'King' and piece.getteam() == p.getteam():
        k = piece
        break
    if k.getname() != 'King':
      return False
    # See if opposing team can find king
    for piece in self.pieces:
      if piece.getteam() != p.getteam():
        if self.moveisvalid(piece.getcoords(),k.getcoords(),piece,False):
          return True
    return False

  # playerincheck(p) method
  # returns whether a player p is currently in check
  def playerincheck(self,p):
    return False

  # mockplayerincheck(p)
  # pieces: list of Pieces
  # player: 1 || 2, which player to check for
  # creates an board with Pieces pieces
  # and returns whether player is in check
  def mockplayerincheck(self,pieces,player):
    mockboard = Board(pieces)
    return mockboard.playerincheck(player)

  # playermated(p) method
  # returns whether a player p is in checkmate
  def playermated(self,p):
    return False

  # indextocoords(i) method
  # takes an int 0 - 99
  # and converts it to a scalar (x,y)
  def indextocoords(self,i):
    if i > 9:
      y = int(str(i)[0])
      x = int(str(i)[1])
      return (x,y)
    else:
      return (i, 0)

  # coordstoindex(c) method
  # takes a scalar c = (x,y)
  # where x and y are both integers 0 - 9
  # and converts it to an integer 0 - 99
  def coordstoindex(self,c):
    # length 19?
    return (2 * c[0]) + ( c[1] * 20 )

  # getpieces() method
  # returns self.pieces
  def getpieces(self):
    return self.pieces.copy()

  # getstate() method
  # returns self.gamestate
  def getstate(self):
    return self.gamestate

# Create list of Piece objects in correct positions
# for a starting boardstate
def generatepieces():
    pieces = []

    # White
    # Major pieces
    pieces.append(Piece("Rook",'R',[('x',0),(0,'x')],1,(1,1),5))
    pieces.append(Piece("Knight",'N',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],1,(2,1),3))
    pieces.append(Piece("Bishop",'B',[('x','x')],1,(3,1),3))
    pieces.append(Piece("Queen",'Q',[('x',0),('x','x'),(0,'x')],1,(4,1),9))
    pieces.append(Piece("King",'K',[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],1,(5,1),0))
    pieces.append(Piece("Bishop",'B',[('x','x')],1,(6,1),3))
    pieces.append(Piece("Knight",'N',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],1,(7,1),3))
    pieces.append(Piece("Rook",'R',[('x',0),(0,'x')],1,(8,1),5))
    # Pawns
    pieces.append(Piece("Pawn",'P',[(0,1),(0,2)],1,(1,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1),(0,2)],1,(2,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1),(0,2)],1,(3,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1),(0,2)],1,(4,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1),(0,2)],1,(5,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1),(0,2)],1,(6,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1),(0,2)],1,(7,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1),(0,2)],1,(8,2),1))

    # Black
    # Major Pieces
    pieces.append(Piece("Rook",'r',[('x',0),(0,'x')],2,(1,8),5))
    pieces.append(Piece("Knight",'n',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],2,(2,8),3))
    pieces.append(Piece("Bishop",'b',[('x','x')],2,(3,8),3))
    pieces.append(Piece("Queen",'q',[('x',0),('x','x'),(0,'x')],2,(4,8),9))
    pieces.append(Piece("King",'k',[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],2,(5,8),0))
    pieces.append(Piece("Bishop",'b',[('x','x')],2,(6,8),3))
    pieces.append(Piece("Knight",'n',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],2,(7,8),3))
    pieces.append(Piece("Rook",'r',[('x',0),(0,'x')],2,(8,8),5))
    # Pawns
    pieces.append(Piece("Pawn",'p',[(0,-1),(0,-2)],2,(1,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1),(0,-2)],2,(2,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1),(0,-2)],2,(3,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1),(0,-2)],2,(4,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1),(0,-2)],2,(5,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1),(0,-2)],2,(6,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1),(0,-2)],2,(7,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1),(0,-2)],2,(8,7),1))

    return pieces
