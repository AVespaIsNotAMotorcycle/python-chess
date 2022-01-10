class Piece:

    def __init__(self, name, icon, moves, team, coords):
        self.name = name
        self.icon = icon
        self.moves = moves
        self.team = team
        self.coords = coords

    # getcoords() method
    # returns coords
    def getcoords(self):
        return self.coords

    # geticon() method
    # returns icon
    def geticon(self):
        return self.icon
