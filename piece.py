class Piece:

    def __init__(self, name, icon, moves, team, coords, points):
        self.name = name
        self.icon = icon
        self.moves = moves
        self.team = team
        self.coords = coords
        self.points = points

    # getname() method
    # returns name
    def getname(self):
        return self.name

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

    # getteam() method
    # returns team
    def getteam(self):
        return self.team

    # getpoints() method
    # returns points
    def getpoints(self):
        return self.points
