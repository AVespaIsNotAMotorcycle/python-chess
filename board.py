from piece import Piece

class Board:

    def __init__(self,pieces):
        self.pieces = pieces
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
        for piece in self.pieces:
            if piece.getcoords() == c:
                return piece
        return 'none'

    # moveisvalid(s,d,p)
    # takes a scalar s, the start coords
    # and a scalar d, the destination coords
    # and a piece p, the piece being moved
    def moveisvalid(self, s, d, p):
        moves = p.getmoves()
        for move in moves:
            if move == ('x','x'):
                tracker = s
                while tracker != d:
                    tracker = (tracker[0] + 1, tracker[1] + 1)
                    if tracker == d:
                        return True
                    else:
                        if self.fetchpiece(tracker) != 'none':
                            break
            elif move == ('x',0):
                tracker = s
                while tracker != d:
                    tracker = (tracker[0] + 1, tracker[1])
                    if tracker == d:
                        return True
                    else:
                        if self.fetchpiece(tracker) != 'none':
                            break
            elif move == (0,'x'):
                tracker = s
                while tracker != d:
                    tracker = (tracker[0], tracker[1] + 1)
                    if tracker == d:
                        return True
                    else:
                        if self.fetchpiece(tracker) != 'none':
                            break

            elif move == (d[0] - s[0],d[1] - s[1]):
                return True
        return False

    # movepiece(s,d,p)
    # takes a scalar s, the start coords
    # and a scalar d, the destination coords
    # and a piece p, the piece being moved
    def movepiece(self, s, d, p):
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
