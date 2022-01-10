from piece import Piece
from board import Board

def generatepieces():
    pieces = []
    pieces.append(Piece("Rook",'R','',1,(1,1)))
    pieces.append(Piece("Knight",'K','',1,(2,1)))
    return pieces

def main():
    print("Hello World")
    pieces = generatepieces()
    board = Board(pieces)
    board.render()

if __name__ == '__main__':
    main()
