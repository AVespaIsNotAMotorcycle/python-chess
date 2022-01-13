from piece import Piece

class Board:

    def __init__(self,pieces):
        self.pieces = pieces
        self.points = [0,0]
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
        moves = p.getmoves()
        if self.fetchpiece(d) != 'none' and self.fetchpiece(d)[1].getteam() == p.getteam():
            return False
        for move in moves:
            # Check diagonal moves
            if move == ('x','x') and (s[0] - d[0]) == (s[1] - d[1]):
                # print("Checking both axes")
                tracker = s
                while tracker != d:
                    print(f"(x,x) check {tracker}")
                    tracker = (tracker[0] + 1, tracker[1] + 1)
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
        if self.fetchpiece(d) != 'none':
            self.points[self.fetchpiece(d)[1].getteam() - 1] += self.fetchpiece(d)[1].getpoints()
            self.pieces.pop(self.fetchpiece(d)[0])
        p.setcoords(d)
        i = self.coordstoindex(s)
        k = self.coordstoindex(d)
        ngs = ""
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
