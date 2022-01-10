from piece import Piece
from board import Board

def generatepieces():
    pieces = []
    
    #White
    pieces.append(Piece("Rook",'R',[('x',0),(0,'x')],1,(1,1)))
    pieces.append(Piece("Knight",'K',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],1,(2,1)))
    
    #Black
    pieces.append(Piece("Rook",'r','',2,(1,8)))
    pieces.append(Piece("Knight",'k','',2,(2,8)))

    return pieces

# converts chessboard notation to coordinates
def altocoord(i):
    return (ord(i[0]) - 96,int(i[1]))

def main():
    print("Hello World")
    pieces = generatepieces()
    board = Board(pieces)
    board.render()

    while(True):
        mv = input()
        mv = mv.split()
        if len(mv) == 2:
            s = altocoord(mv[0])
            d = altocoord(mv[1])
            movedpiece = board.fetchpiece(s)
            if movedpiece == 'none':
                print('No piece at ' + mv[0])
            else:
                if board.moveisvalid(s,d,movedpiece):
                    board.movepiece(s,d,movedpiece)
                else:
                    print("Move invalid")
        else:
            print('Please input 2 coordinates')

if __name__ == '__main__':
    main()
