from piece import Piece

class Board:

    def __init__(self,pieces):
        self.pieces = pieces
        self.points = [0,0]
        self.enpassent = 'none'
        self.gamestate = ""
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
                self.gamestate += '#\n'
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
        #for piece in self.pieces:
        #    print(f'{piece.getname()}, {piece.getteam()}')
        print(f'Points: White {self.points[0]}, Black {self.points[1]}')
        rstate = ''
        for c in self.gamestate:
            if c != '\n':
                rstate += ' ' + c + ' '
            else:
                rstate += c
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
        # print(f"Checking: move {p.getname()} from {s} to {d}")
        #Pawn Exceptions
        if p.getname() == "Pawn":
            # 2 tile move
            if abs(d[1] - s[1]) == 2 and s[0] == d[0]:
            #    print('2 tile move')
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
            #    print('valid capture')
                return True
            # Standard move
            elif s[0] - d[0] == 0 and s[1] - d[1] == -1 * (2 * (p.getteam() % 2) - 1) and self.fetchpiece(d) == 'none':
            #    print('normal move')
                return True
            # En passent
            elif d == self.enpassent and abs(s[0] - d[0]) == 1 and s[1] - d[1] == -1 * (2 * (p.getteam() % 2) - 1):
            #    print('valid enpassent')
                return True
            else:
            #    print('invalid move')
                return False

        if d[0] < 1 or d[0] > 8 or d[1] < 1 or d[1] > 8:
            return False
        moves = p.getmoves()
        if self.fetchpiece(d) != 'none' and self.fetchpiece(d)[1].getteam() == p.getteam():
            # print('Square occupied by teammate')
            return False
        for move in moves:
            # print(f'{move} {s} {d}')
            # Check diagonal moves
            if move == ('x','x') and abs(s[0] - d[0]) == abs(s[1] - d[1]):
                # print("Checking both axes")
                tracker = s
                cx = 1
                cy = 1
                if d[0] < s[0]:
                    cx = -1
                if d[1] < s[1]:
                    cy = -1
                while tracker != d:
                    # print(f"(x,x) check {tracker}")
                    tracker = (tracker[0] + cx, tracker[1] + cy)
                    if tracker == d:
                        return True
                    else:
                        if self.fetchpiece(tracker) != 'none' or self.coordstoindex(tracker) > 89 or self.coordstoindex(tracker) < 9:
                            break
            # Check horizontal moves
            elif move == ('x',0) and (s[1] - d[1]) == 0:
                # print("Checking x-axis")
                tracker = s
                coeff = 1
                if (s[0] - d[0]) > 0:
                    coeff = -1
                while tracker != d:
                    # print(f"(x,0) check {tracker}")
                    tracker = (tracker[0] + (1 * coeff), tracker[1])
                    if tracker == d:
                        return True
                    else:
                        if self.fetchpiece(tracker) != 'none' or self.coordstoindex(tracker) > 89 or self.coordstoindex(tracker) < 9:
                            break
            # Check vertical moves
            elif move == (0,'x') and (s[0] - d[0]) == 0:
                # print("Checking y-axis")
                tracker = s
                coeff = 1
                if (s[1] - d[1]) > 0:
                    coeff = -1
                while tracker != d:
                    # print(f"(0,x) check {tracker}")
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
        # print('movepiece()')
        e = -1
        if d == self.enpassent and p.getname() == "Pawn":
            # print('enpassent')
            t = (d[0], d[1] + (-1 * ((2 * (p.getteam() % 2)) - 1)))
            e = self.coordstoindex(t)
            # print(t)
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
            elif c == k:
                ngs += p.geticon()
            else:
                ngs += self.gamestate[c]
        self.gamestate = ngs
        self.render()

    # resultsincheck(s,d,p) method
    # computes an otherwise valid move
    # to see if it would result in that
    # player being in check
    def resultsincheck(self,s,d,p):
        # print('resultsincheck()')
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
                        print(f'{piece.getcoords()} {tk.getcoords()}')
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
        # print('Checking for mate')
        for index, piece in enumerate(self.pieces):
            if piece.getteam() == p:
                for i in range(99):
                    if self.moveisvalid(piece.getcoords(), self.indextocoords(i),piece):
                        if not self.resultsincheck(piece.getcoords(),self.indextocoords(i),piece):
                            # print(f'valid move: {piece.getcoords()} {self.indextocoords(i)} {piece.getname()}')
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
        return c[0] + ( c[1] * 10 ) + c[1]
