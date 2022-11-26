from unittest import TestCase
from opponents.boardstate_heuristic import OppBoardStateHeuristic
from piece import Piece
from board import Board

class TestingBoardstateHeuristic(TestCase):
  def test_constructor(self):
    testOpp = OppBoardStateHeuristic(1)
    assert (isinstance(testOpp, OppBoardStateHeuristic))

  def test_coordtoutil(self):
    testOpp = OppBoardStateHeuristic(1)
    # Test that the corners have 1 utility
    util = testOpp.coordtoutil(1,1)
    assert (util == 1)
    util = testOpp.coordtoutil(8,1)
    assert (util == 1)
    util = testOpp.coordtoutil(8,8)
    assert (util == 1)
    util = testOpp.coordtoutil(1,8)
    assert (util == 1)
    # Test that the center 4 tiles have 16 utility
    util = testOpp.coordtoutil(4,4)
    assert (util == 16)
    util = testOpp.coordtoutil(4,5)
    assert (util == 16)
    util = testOpp.coordtoutil(5,5)
    assert (util == 16)
    util = testOpp.coordtoutil(5,4)
    assert (util == 16)

  def test_utility(self):
    testOpp = OppBoardStateHeuristic(1)
    # Friendly Queen in starting position should be 36
    testPieces = [
      Piece('Queen', 'Q', [('x',0), ('x','x'), (0,'x')], 1, (4,1), 9)
    ]
    util = testOpp.utility(testPieces)
    assert (util == 36)
    # Enemy Queen in starting position should be -36
    testPieces = [
      Piece('Queen', 'Q', [('x',0), ('x','x'), (0,'x')], 2, (5,8), 9)
    ]
    util = testOpp.utility(testPieces)
    assert (util == -36)

  def test_makemove(self):
    testOpp = OppBoardStateHeuristic(1)
    '''
    # Optimal move should be to take enemy Queen
    testPieces = [
      Piece('Queen', 'Q', [('x',0), ('x','x'), (0,'x')], 1, (4,4), 9),
      Piece('Queen', 'q', [('x',0), ('x','x'), (0,'x')], 2, (5,5), 9)
    ]
    testBoard = Board(testPieces)
    move = testOpp.makemove(testBoard, testPieces)
    assert (move == 'd4 e5')
    '''
    # Optimal move should be to move to center of board
    testPieces = [
      Piece('Rook', 'R', [('x',0), (0,'x')], 1, (1,1), 9),
      Piece('Rook', 'r', [('x',0), (0,'x')], 2, (8,8), 5)
    ]
    testBoard = Board(testPieces)
    mv = testOpp.makemove(testBoard, testPieces)
    iM = ['a1 a4', 'a1 a5', 'a1 d1', 'a1 e1']
    assert (mv == iM[0] or mv == iM[1] or mv == iM[2] or mv == iM[3])
