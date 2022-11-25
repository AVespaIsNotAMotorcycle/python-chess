from utils import DEFAULT_SETTINGS, altocoord, coordtoal
from piece import Piece
from board import Board, generatepieces
from opponent import Opponent


'''
handles user input given a turn number 'turn'
and a boardstate 'board'
and a dictionary 'settings'
of form:
{
  opponent: ai || human (required)
  playercolor: white || black (optional)
}
returns 1 if user input was valid
otherwise returns 0
'''
def handleinput(turn, board, settings):
  team = 2 - turn % 2
  teamstring = 'white'
  if team == 2:
    teamstring = 'black'
  active = settings['players'][teamstring]

  # tell the user whose turn it is
  print('Turn ' + str(turn) + ': ' + teamstring + ' to move')
 
  # handle ai turn
  if active == 'ai':
    if turn % 2 == team % 2:
      ai = Opponent(team)
      mv = ai.makemove(board, board.getpieces())
      mv = mv.split()
      print(mv)

  # handle input
  if active == 'human':
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
  if board.playerincheck(turn % 2 + 1):
    if board.playermated(turn % 2 + 1):
      print('Checkmate!')
      return(-10000)
    else:
      print('Check!')
  return 1

def playerprefs():
  settings = DEFAULT_SETTINGS().copy()

  # Check if the user is playing or observing
  while settings['observing'] == 'None':
    print('Would you like to play or observe two AIs play?')
    i = input('Type "play" or "observe"\n')
    if i == 'play' or i == 'observe':
      settings['observing'] = i
      settings['players']['white'] = 'ai'
      settings['players']['black'] = 'ai'

  if settings['observing'] == 'observe':
    return settings

  # Check if playing against human or ai
  while settings['opponent'] == 'None':
    print('Would you like to play against an AI or a human?')
    i = input('Type "ai" or "human"\n');
    if i == 'ai' or i == 'human':
      settings['opponent'] = i

  if settings['opponent'] == 'human':
    return settings

  # if against ai, ask for player color
  while settings['playercolor'] == 'None':
    print('Would you like to play as white or black?')
    i = input('Type "white" or "black" \n')
    if i == 'white' or i == 'black':
      settings['playercolor'] = i
      if i == 'white':  
        settings['players']['black'] = 'ai'
      else:
        settings['players']['white'] = 'ai'
  return settings

def main():
  # Setup
  settings = playerprefs()

  # initialize board
  pieces = generatepieces()
  board = Board(pieces)
  board.settings = settings
  board.render()
  turn = 1

  # handle input
  while(True):
    if turn < 0:
      return
    if turn > 100:
      return
    turn += handleinput(turn, board, settings);

if __name__ == '__main__':
  main()
