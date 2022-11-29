from utils import DEFAULT_SETTINGS, AI_LIST, altocoord, coordtoal
from piece import Piece
from board import Board, generatepieces
from tournament import Tournament
from opponents.utils import create_opponent
import sys

'''
handles user input given a turn number 'turn'
and a boardstate 'board'
and a dictionary 'settings'
of form:
{
  opponent: {ai_name} || human (required)
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
  if active != 'human':
    if turn % 2 == team % 2:
      ai = create_opponent(team, active)
      mv = ai.makemove(board, board.getpieces())
      print(mv)
      if mv == 'concede':
        return -101
      mv = mv.split()

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

  movedpiece = board.fetchpiece(s)
  # ensure that there's a piece at the first coord
  if movedpiece == 'none':
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
  if board.fetchpiece(d) != 'none':
    print('took', board.fetchpiece(d).getname())
  board.movepiece(s, d, movedpiece)
  print(len(board.getpieces()),'pieces remaining')
  if board.playerincheck(turn % 2 + 1):
    if board.playermated(turn % 2 + 1):
      print('Checkmate!')
      return(-10000)
    else:
      print('Check!')
  return 1

def playerprefs(settings = DEFAULT_SETTINGS().copy()):
  # Check if the user is playing or observing
  while settings['observing'] == 'None':
    print('Would you like to play or observe two AIs play?')
    i = input('Type "play" or "observe"\n')
    if i == 'play' or i == 'observe':
      settings['observing'] = i

  if settings['observing'] == 'observe' or settings['observing'] == 'tournament':
    if settings['players']['white'] == 'None':
      settings['players']['white'] = 'ai'
    if settings['players']['black'] == 'None':
      settings['players']['black'] = 'ai'
    settings['opponent'] = 'ai'

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

  # if white is ai, ask for ai name
  while settings['players']['white'] == 'ai':
    print('What AI should play as white?')
    ai_list = AI_LIST()
    ai_str = 'Choose from: '
    for ai in ai_list:
      ai_str += '\n"' + ai + '"'
    i = input(ai_str + '\n')
    if ai_list.count(i) > 0:
      settings['players']['white'] = i

  # if black is ai, ask for ai name
  while settings['players']['black'] == 'ai':
    print('What AI should play as black?')
    ai_list = AI_LIST()
    ai_str = 'Choose from: '
    for ai in ai_list:
      ai_str += '\n"' + ai + '"'
    i = input(ai_str + '\n')
    if ai_list.count(i) > 0:
      settings['players']['black'] = i

  return settings

def playergame(settings, board):
  board.render()
  turn = 1

  # handle input
  while(True):
    if turn < 0:
      return
    if turn > settings['maxturns']:
      return
    turn += handleinput(turn, board, settings);
    board.render()

def observergame(settings, board):
  board.render()
  turn = 1

  # handle input
  while(True):
    if turn < 0:
      return
    if turn > settings['maxturns']:
      return
    turn += handleinput(turn, board, settings);
    board.render()

def tournamentgame(settings, board):
  t = Tournament(settings['players']['white'], settings['players']['black'])
  print('tournament')
  t.runtournament(settings)

def main(argv):
  # Setup
  settings = DEFAULT_SETTINGS().copy()
 
  ## Determine game type 
  gametype = 'player'
  if argv.count('-p') > 0:
    gametype = 'player'
    settings['observing'] = 'play'
  if argv.count('-o') > 0:
    gametype = 'observer'
    settings['observing'] = 'observe'
  if argv.count('-t') > 0:
    gametype = 'tournament'
    settings['observing'] = 'tournament'
    settings['playercolor'] = 'tournament'

  ## Determine AI Opponent
  if argv.count('p1') > 0:
    i = argv.index('p1')
    if AI_LIST().count(argv[i + 1]) > 0:
      settings['opponent'] = 'ai'
      settings['playercolor'] = 'black'
      settings['players']['white'] = argv[i + 1]
      print('set player 1 to ' + argv[i + 1])
  if argv.count('p2') > 0:
    i = argv.index('p2')
    if AI_LIST().count(argv[i + 1]) > 0:
      settings['opponent'] = 'ai'
      settings['playercolor'] = 'white'
      settings['players']['black'] = argv[i + 1]
      print('set player 2 to ' + argv[i + 1])

  ## Set maxturns
  if argv.count('maxturns') > 0:
    i = argv.index('maxturns')
    if argv[i + 1].isnumeric():
      settings['maxturns'] = int(argv[i + 1])

  settings = playerprefs(settings)

  print(settings)
  # initialize board
  pieces = generatepieces()
  board = Board(pieces)
  board.settings = settings

  if gametype == 'player':
    playergame(settings, board)
  if gametype == 'observer':
    observergame(settings, board)
  if gametype == 'tournament':
    tournamentgame(settings, board)

if __name__ == '__main__':
  main(sys.argv)
