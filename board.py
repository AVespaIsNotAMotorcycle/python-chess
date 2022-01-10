from piece import Piece

class Board:

    def __init__(self,pieces):
        self.pieces = pieces
        self.gamestate = ""
        for i in range(100):
            # Borders
            if i < 9:
                self.gamestate += '#'
            elif i % 10 == 0:
                self.gamestate += '#'
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

    # indextocoords() method
    # takes an int 0 - 99
    # and converts it to a scalar (x,y)
    def indextocoords(self,i):
        if i > 9:
            y = int(str(i)[0])
            x = int(str(i)[1])
            return (x,y)
        else:
            return (i, 0)

    # coordstoindex() method
    # takes a scalar (x,y)
    # where x and y are both integers 0 - 9
    # and converts it to an integer 0 - 99
    def coordstoindex(self,c):
        return c[0] + ( c[1] * 10 )
