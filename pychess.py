from piece import Piece
from board import Board

def generatepieces():
    pieces = []
    
    # White
    # Major pieces
    pieces.append(Piece("Rook",'R',[('x',0),(0,'x')],1,(1,1),5))
    pieces.append(Piece("Knight",'N',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],1,(2,1),3))
    pieces.append(Piece("Bishop",'B',[('x','x')],1,(3,1),3))
    pieces.append(Piece("Queen",'Q',[('x',0),('x','x'),(0,'x')],1,(4,1),9))
    pieces.append(Piece("King",'K',[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],1,(5,1),0))
    pieces.append(Piece("Bishop",'B',[('x','x')],1,(6,1),3))
    pieces.append(Piece("Knight",'N',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],1,(7,1),3))
    pieces.append(Piece("Rook",'R',[('x',0),(0,'x')],1,(8,1),5))
    # Pawns
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(1,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(2,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(3,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(4,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(5,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(6,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(7,2),1))
    pieces.append(Piece("Pawn",'P',[(0,1)],1,(8,2),1))

    # Black
    # Major Pieces
    pieces.append(Piece("Rook",'r',[('x',0),(0,'x')],2,(1,8),5))
    pieces.append(Piece("Knight",'n',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],2,(2,8),3))
    pieces.append(Piece("Bishop",'b',[('x','x')],2,(3,8),3))
    pieces.append(Piece("Queen",'q',[('x',0),('x','x'),(0,'x')],2,(4,8),9))
    pieces.append(Piece("King",'k',[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)],2,(5,8),0))
    pieces.append(Piece("Bishop",'b',[('x','x')],2,(6,8),3))
    pieces.append(Piece("Knight",'n',[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)],2,(7,8),3))
    pieces.append(Piece("Rook",'r',[('x',0),(0,'x')],2,(8,8),5))
    # Pawns
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(1,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(2,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(3,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(4,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(5,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(6,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(7,7),1))
    pieces.append(Piece("Pawn",'p',[(0,-1)],2,(8,7),1))

    return pieces

# converts chessboard notation to coordinates
def altocoord(i):
    return (ord(i[0]) - 96,int(i[1]))

def main():
    pieces = generatepieces()
    board = Board(pieces)
    board.render()
    turn = 1

    while(True):
        if turn == 1:
            print("White to move")
        else:
            print("Black to move")
        mv = input()
        mv = mv.split()
        if len(mv) == 2:
            s = altocoord(mv[0])
            d = altocoord(mv[1])
            movedpiece = board.fetchpiece(s)[1]
            if movedpiece == 'o':
                print('No piece at ' + mv[0])
            else:
                if board.moveisvalid(s,d,movedpiece) and movedpiece.getteam() == turn:
                    if board.resultsincheck(s,d,movedpiece):
                        print("Move invalid - results in check")
                    else:
                        print("Move valid")
                        board.movepiece(s,d,movedpiece) 
                        if turn == 1:
                            turn = 2
                            if board.playerincheck(turn):
                                if board.playermated(turn):
                                    print('Checkmate!')
                                    return
                                else:
                                    print('Check!')
                        else:
                            turn = 1
                            if board.playerincheck(turn):
                                print('Check!')
                else:
                    print("Move invalid")
        else:
            print('Please input 2 coordinates')

if __name__ == '__main__':
    main()
