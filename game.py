class Game:
  def __init__(
    self,
    playerWhite,
    playerBlack,
    turn = 1,
    board = [],
  ):
    safeBoard = board
    if not safeBoard:
      safeBoard = [
        [],
      ]

    self.playerWhite = playerWhite
    self.playerBlack = playerBlack
    self.turn = turn
    self.board = board
