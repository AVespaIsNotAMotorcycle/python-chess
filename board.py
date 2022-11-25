from utils import DEFAULT_SETTINGS, altocoord, coordtoal
from piece import Piece
from opponent import Opponent

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
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(1,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(2,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(3,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(4,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(5,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(6,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(7,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(8,2),1))

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
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(1,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(2,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(3,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(4,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(5,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(6,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(7,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(8,7),1))

    return pieces

class Board:

    def __init__(self,pieces):
        self.pieces = pieces
        self.points = [0,0]
        self.enpassent = 'none'
        self.gamestate = ""
        self.settings = DEFAULT_SETTINGS().copy()
        # castlereqs[0] = white left rook hasn't moved, king hasn't moved, right rook hasn't moved
        # castlereqs[1] = black left rook hasn't moved, king hasn't moved, right rook hasn't moved
        self.castlereqs = [[True,True,True],[True,True,True]]
        for i in range(100):
            # Borders
            if i < 9:
                if i == 0:
                    self.gamestate += '#'
                else:
                    self.gamestate += chr(i + 96)
            elif i % 10 == 0:
                if i == 90:
                    self.gamestate += '#'
                else:
                    self.gamestate += str(i)[0]
            elif i % 10 == 9:
                self.gamestate += '#'
            elif i >= 90:
                self.gamestate += '#'

            # Content
            else:
                pieceplaced = False
                for piece in pieces:
                    if piece.getcoords() == self.indextocoords(i):
                        self.gamestate += piece.geticon()
                        pieceplaced = True
                if not pieceplaced:
                    if (i + int(str(i)[0])) % 2 == 0:
                        self.gamestate += '-'
                    else:
                        self.gamestate += ' '


    # render() method
    # outputs board state to console
    def render(self):
        print(' - - - - - - - - - - - - - - ')
        # print(f'Points: White {self.points[0]}, Black {self.points[1]}')
        rstate = ''
        for index, c in enumerate(self.gamestate):
            rstate += ' ' + c + ' '
            if index % 10 == 9:
                rstate += '\n'
        print(rstate)

    # fetchpiece(c)
    # takes a scalar c = (x,y)
    # where x and y are both integers 0 - 9
    # and return any piece found at those coords
    def fetchpiece(self, c):
        for index, piece in enumerate(self.pieces):
            if piece.getcoords() == c:
                return (index, piece)
        return 'none'

    # moveisvalid(s,d,p)
    # takes a scalar s, the start coords
    # and a scalar d, the destination coords
    # and a piece p, the piece being moved
    def moveisvalid(self, s, d, p):
        # check that neither s nor d are out of bounds
        if s[0] < 1 or s[1] < 1:
          return False
        if s[0] > 8 or s[1] > 8:
          return False
        if d[0] < 1 or d[1] < 1:
          return False
        if d[0] > 8 or d[1] > 8:
          return False

        #Pawn Exceptions
        if p.getname() == "Pawn":
            # 2 tile move
            if abs(d[1] - s[1]) == 2 and s[0] == d[0]:
                if d[0] != s[0]:
                    return False
                if p.getteam() == 1:
                    if s[1] == 2 and d[1] == 4 and self.fetchpiece((d[0],d[1]-1)) == 'none' and self.fetchpiece(d) == 'none':
                        # enable en passent
                        return True
                else:
                    if s[1] == 7 and d[1] == 5 and self.fetchpiece((d[0],d[1] + 1)) == 'none' and self.fetchpiece(d) == 'none':
                        #enable en passent
                        return True
            # Capturing
            elif self.fetchpiece(d) != 'none' and abs(s[0] - d[0]) == 1 and s[1] - d[1] == -1 * (2 * (p.getteam() % 2) - 1):
                return True
            # Standard move
            elif s[0] - d[0] == 0 and s[1] - d[1] == -1 * (2 * (p.getteam() % 2) - 1) and self.fetchpiece(d) == 'none':
                return True
            # En passent
            elif d == self.enpassent and abs(s[0] - d[0]) == 1 and s[1] - d[1] == -1 * (2 * (p.getteam() % 2) - 1):
                return True
            else:
                return False

        # King exceptions
        if p.getname() == "King" and s[1] == d[1] and ((d[0] == s[0] - 2 and self.castlereqs[p.getteam() - 1][0] and self.castlereqs[p.getteam() - 1][1]) or (d[0] == s[0] + 2 and self.castlereqs[p.getteam() - 1][1] and self.castlereqs[p.getteam() - 1][2])):
            if d[0] == s[0] + 2 and self.fetchpiece((s[0] + 1,s[1])) == 'none' and self.fetchpiece((s[0] + 2,s[1])) == 'none' and self.fetchpiece((s[0] + 3,s[1])) == 'none':
                return True
            elif d[0] == s[0] - 2 and self.fetchpiece((s[0] - 1,s[1])) == 'none' and self.fetchpiece((s[0] - 2,s[1])) == 'none' and self.fetchpiece((s[0] - 3,s[1])) == 'none' and self.fetchpiece((s[0] - 4, s[1])):
                return True
            else:
                return False

        if d[0] < 1 or d[0] > 8 or d[1] < 1 or d[1] > 8:
            return False
        moves = p.getmoves()
        if self.fetchpiece(d) != 'none' and self.fetchpiece(d)[1].getteam() == p.getteam():
            return False
        for move in moves:
            # Check diagonal moves
            if move == ('x','x') and abs(s[0] - d[0]) == abs(s[1] - d[1]):
                tracker = s
                cx = 1
                cy = 1
                if d[0] < s[0]:
                    cx = -1
                if d[1] < s[1]:
                    cy = -1
                while tracker != d:
                    tracker = (tracker[0] + cx, tracker[1] + cy)
                    if tracker == d:
                        return True
                    else:
                        if self.fetchpiece(tracker) != 'none' or self.coordstoindex(tracker) > 89 or self.coordstoindex(tracker) < 9:
                            break
            # Check horizontal moves
            elif move == ('x',0) and (s[1] - d[1]) == 0:
                tracker = s
                coeff = 1
                if (s[0] - d[0]) > 0:
                    coeff = -1
                while tracker != d:
                    tracker = (tracker[0] + (1 * coeff), tracker[1])
                    if tracker == d:
                        return True
                    else:
                        if self.fetchpiece(tracker) != 'none' or self.coordstoindex(tracker) > 89 or self.coordstoindex(tracker) < 9:
                            break
            # Check vertical moves
            elif move == (0,'x') and (s[0] - d[0]) == 0:
                tracker = s
                coeff = 1
                if (s[1] - d[1]) > 0:
                    coeff = -1
                while tracker != d:
                    tracker = (tracker[0], tracker[1] + (1 * coeff))
                    if tracker == d:
                        return True
                    else:
                        if self.fetchpiece(tracker) != 'none' or self.coordstoindex(tracker) > 89 or self.coordstoindex(tracker) < 9:
                            break
            # Check bounded moves
            elif move == (d[0] - s[0],d[1] - s[1]):
                return True
        return False

    # movepiece(s,d,p)
    # takes a scalar s, the start coords
    # and a scalar d, the destination coords
    # and a piece p, the piece being moved
    def movepiece(self, s, d, p):
        # Castling
        rf = -1
        rn = -1
        if p.getname() == "King" and abs(s[0] - d[0]) == 2 and s[1] == d[1]:
            self.castlereqs[p.getteam() - 1] = (False, False, False)
            p.setcoords(d)
            if d[0] > s[0]:
                rf = self.coordstoindex((8,d[1]))
                self.fetchpiece((8,s[1]))[1].setcoords((d[0]-1,d[1]))
                rn = self.coordstoindex((d[0]-1,d[1]))
            else:
                rf = self.coordstoindex((1,d[1]))
                self.fetchpiece((1,s[1]))[1].setcoords((d[0]+1,d[1]))
                rn = self.coordstoindex((d[0]+1,d[1]))
        # Enpassent
        e = -1
        if d == self.enpassent and p.getname() == "Pawn":
            t = (d[0], d[1] + (-1 * ((2 * (p.getteam() % 2)) - 1)))
            e = self.coordstoindex(t)
            self.points[p.getteam() - 1] += self.fetchpiece(t)[1].getpoints()
            self.pieces.pop(self.fetchpiece(t)[0])
        elif p.getname() == "Pawn" and abs(s[1] - d[1]) == 2:
            if s[1] < d[1]:
                self.enpassent = (d[0],d[1] - 1)
            else:
                self.enpassent = (d[0],d[1] + 1)
        else:
            self.enpassent = 'none'
        if self.fetchpiece(d) != 'none':
            self.points[p.getteam() - 1] += self.fetchpiece(d)[1].getpoints()
            self.pieces.pop(self.fetchpiece(d)[0])
        p.setcoords(d)
        i = self.coordstoindex(s)
        k = self.coordstoindex(d)
        # Pawn Promotion
        if p.getname() == "Pawn" and ((d[1] == 8 and p.getteam() == 1) or (d[1] == 1 and p.getteam() == 2)):
            # Check if player is AI or human
            promo = ''
            piece_team_string = 'white'
            if p.getteam() == 2:
              piece_team_string = 'black'
            if self.settings['players'][piece_team_string] == 'ai':
              promo = Opponent(p.getteam()).promotepiece(self)
            else:
              promo = input("Choose a piece:")
            if p.getteam() == 1:
                if promo.capitalize() == "Queen":
                    p = Piece("Queen",'Q',[('x',0),('x','x'),(0,'x')],1,d,9)
                if promo.capitalize() == "Rook":
                    p = Piece("Rook",'R',[('x',0),(0,'x')],1,d,5)
                if promo.capitalize() == "Bishop":
                    p = Piece("Bishop",'B',[('x','x')],1,d,3)
                if promo.capitalize() == "Knight":
                    p = Piece("Knight",'N',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],1,d,3)
            if p.getteam() == 2:
                if promo.capitalize() == "Queen":
                    p = Piece("Queen",'q',[('x',0),('x','x'),(0,'x')],2,d,9)
                if promo.capitalize() == "Rook":
                    p = Piece("Rook",'r',[('x',0),(0,'x')],2,d,5)
                if promo.capitalize() == "Bishop":
                    p = Piece("Bishop",'b',[('x','x')],2,d,3)
                if promo.capitalize() == "Knight":
                    p = Piece("Knight",'n',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],2,d,3)
        ngs = ""
        for c in range(len(self.gamestate)):
            if c == i:
                if s[0] % 2 == s[1] % 2:
                    ngs += '-'
                else:
                    ngs += ' '
            elif c == e:
                if self.indextocoords(e)[0] % 2 == self.indextocoords(e)[1] % 2:
                    ngs += '-'
                else:
                    ngs += ' '
            elif c == rf:
                if self.indextocoords(rf)[0] % 2 == self.indextocoords(rf)[1] % 2:
                    ngs += '-'
                else:
                    ngs += ' '
            elif c == k:
                ngs += p.geticon()
            elif c == rn:
                ngs += self.fetchpiece(self.indextocoords(rn))[1].geticon()
            else:
                ngs += self.gamestate[c]
        self.gamestate = ngs
        self.render()

    # resultsincheck(s,d,p) method
    # computes an otherwise valid move
    # to see if it would result in that
    # player being in check
    def resultsincheck(self,s,d,p):
        ngs = ""
        i = self.coordstoindex(s)
        k = self.coordstoindex(d)
        for c in range(len(self.gamestate)):
            if c == i:
                if s[0] % 2 == 0 and s[1] % 2 == 0:
                    ngs += ' '
                else:
                    ngs += '-'
            elif c == k:
                ngs += p.geticon()
            else:
                ngs += self.gamestate[c]
        tk = self.pieces[0]
        for index, piece in enumerate(self.pieces):
            if piece.getname() == 'King' and piece.getteam() == p.getteam():
                tk = piece
                break
        for index, piece in enumerate(self.pieces):
            if piece.getteam() != p.getteam():
                if p.getname() != 'King':
                    if self.moveisvalid(piece.getcoords(), tk.getcoords(), piece):
                        return True
                else:
                    if self.moveisvalid(piece.getcoords(), d, piece):
                        return True
        return False

    # playerincheck(p) method
    # returns whether a player p is currently in check
    def playerincheck(self,p):
        tk = self.pieces[0]
        for index, piece in enumerate(self.pieces):
            if piece.getname() == 'King' and piece.getteam() == p:
                tk = piece
                break
        for index, piece in enumerate(self.pieces):
            if self.moveisvalid(piece.getcoords(), tk.getcoords(), piece):
                return True
        return False

    # playermated(p) method
    # returns whether a player p is in checkmate
    def playermated(self,p):
        for index, piece in enumerate(self.pieces):
            if piece.getteam() == p:
                for i in range(99):
                    if self.moveisvalid(piece.getcoords(), self.indextocoords(i),piece):
                        if not self.resultsincheck(piece.getcoords(),self.indextocoords(i),piece):
                            return False
        return True

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
        return c[0] + ( c[1] * 10 )

    # getpieces() method
    # returns self.pieces
    def getpieces(self):
      return self.pieces
