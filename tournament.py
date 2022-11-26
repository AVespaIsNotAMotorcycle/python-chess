import time

class Tournament:

  '''
  Tournament initializer
  player1: an Opponent()
  player2: an Opponent()
  '''
  def __init__(self, player1, player2):
    self.player1 = player1
    self.player2 = player2
    self.maxrounds = rounds
    
    # Non-required props
    self.gametime = 1.0     # How many seconds a game can last
    self.rounds = 100       # How many rounds a tournament lasts

  '''
  runturn(turn, board) method where
  turn: what game turn we're on
  board: Board() representing current boardstate
  returns either 1 or 0, where
  1 means a move was valid and that the turn should pass
  0 means a move was invalid and the Opponent should try again
  '''
  def runturn(self, turn, board):
    team = 2 - turn % 2
    teamstring = 'white'
    active = self.player1
    if team == 2:
      teamstring = 'black'
      active = self.player2
    
    # Ask ai for move
    mv = active.makemove(board, board.getpieces())
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

  '''
  game() method
  returns 0, 1, or 2 where
  0 means draw
  1 means player1 won
  2 means player2 won
  '''
  def game(self):
    pieces = generatepieces()
    board = Board(pieces)
    turn = 1

    # Run turns until game is complete,
    # either by draw or victory
    gamestart = time.time()
    while time.time() - gamestart < gametime:
      team = 2 - turn % 2
      turn += self.runturn(turn, board)
      if turn < 1:
        return team
      if turn > 100:
        return 0
    return 0

  '''
  runtournament() methond
  runs a number of games equal to self.rounds
  prints the results
  '''
  def runtournament(rounds = self.rounds, report = True):
    results = []
    starttime = time.time()
    for i in range(rounds):
      results.append(game())
    endtime = time.time()
    if (report):
      print(str(rounds) + ' games completed in ' + endtime - startime + ' seconds')
    return results
