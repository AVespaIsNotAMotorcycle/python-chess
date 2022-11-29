class Piece:

    def __init__(self, name, icon, moves, team, coords, points):
        self.name = name
        self.icon = icon
        self.moves = moves
        self.team = team
        self.coords = coords
        self.points = points
        self.lastcoords = coords

    # getname() method
    # returns name
    def getname(self):
        return self.name

    # setcoords(c) method
    # takes a scalar c, the new coords
    # and sets coords = c
    def setcoords(self,c):
        self.lastcoords = self.coords
        self.coords = c

    # getcoords() method
    # returns coords
    def getcoords(self):
        return self.coords

    # getlastcoords() method
    # returns lastcoords
    def getlastcoords(self):
        return self.lastcoords

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
        return self.moves.copy()

    # getteam() method
    # returns team
    def getteam(self):
        return self.team

    # getpoints() method
    # returns points
    def getpoints(self):
        return self.points

    # copy() method
    # returns a deep copy
    def copy(self):
      # (self, name, icon, moves, team, coords, points):
      c = Piece(self.name,self.icon,self.moves,self.team,self.coords,self.points)
      c.lastcoords = self.lastcoords
      return c

    # __repr__() method
    # returns name and coords
    # enables print() statements
    def __repr__(self):
      return '<Piece ' + self.name + ', ' + str(self.coords) + '>'

    def __eq__(self, other):
      try:
        return self.getcoords() == other.getcoords() and self.getname() == other.getname()
      except:
        return False
