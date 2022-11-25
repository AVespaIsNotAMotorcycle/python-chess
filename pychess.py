from piece import Piece
from board import Board, generatepieces

# converts chessboard notation to coordinates
def altocoord(i):
  # check that i is str of len 2
  if len(i) != 2:
    return False
  # check that i[0] is a letter
  if i[0].isalpha() == False:
    return False
  # check that i[1] is a number
  if i[1].isdecimal() == False:
    return False
  return (ord(i[0]) - 96,int(i[1]))

# handles user input given a turn number 'turn'
# and a boardstate 'board'
# returns 1 if user input was valid
# otherwise returns 0
def handleinput(turn, board):
  # tell the user whose turn it is
  if turn % 2 == 1:
    print('Turn ' + str(turn) + ': White to move')
  else:
    print('Turn ' + str(turn) + ': Black to move')
 
  # handle input
  mv = input()
  mv = mv.split()
  # ensure input has at exactly 2 terms
  if len(mv) != 2:
    print('Please input 2 coordinates')
    return 0
  
  s = altocoord(mv[0])
  d = altocoord(mv[1])
  # ensure that coordinates are properly formatted
  if s == False or d == False:
    print('Please input coordinates in the form "d2"')
    return 0

  movedpiece = board.fetchpiece(s)[1]
  # ensure that there's a piece at the first coord
  if movedpiece == 'o':
    print('No piece at ' + mv[0])
    return 0
  
  # ensure that the piece is of the correct color
  if movedpiece.getteam() % 2 != turn % 2:
    print('Piece at ' + mv[0] + ' is of the wrong color')
    return 0

  # ensure that the move is valid
  if board.moveisvalid(s, d, movedpiece) == False:
    print('Move invalid')
    return 0

  # ensure that the move would not put the player in check
  if board.resultsincheck(s, d, movedpiece):
    print('Move invalid - results in check')
    return 0

  # if it has passed all the tests above, enact move
  board.movepiece(s, d, movedpiece)
  if board.playerincheck(turn % 2 == 1):
    if board.playermated(turn % 2 == 1):
      print('Checkmate!')
    else:
      print('Check!')
  return 1

def main():
    # initialize board
    pieces = generatepieces()
    board = Board(pieces)
    board.render()
    turn = 1

    # handle input
    while(True):
      turn += handleinput(turn, board);

if __name__ == '__main__':
    main()
