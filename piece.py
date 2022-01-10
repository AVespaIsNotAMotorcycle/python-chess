class Piece:

    def __init__(self, name, icon, moves, team, coords):
        self.name = name
        self.icon = icon
        self.moves = moves
        self.team = team
        self.coords = coords

    # setcoords(c) method
    # takes a scalar c, the new coords
    # and sets coords = c
    def setcoords(self,c):
        self.coords = c

    # getcoords() method
    # returns coords
    def getcoords(self):
        return self.coords

    # geticon() method
    # returns icon
    def geticon(self):
        return self.icon

    # getmoves() method
    # returns moves
    # moves are scalars (x,y)
    # where x is the difference in position horizontally
    # and y is the difference vertically
    def getmoves(self):
        return self.moves
