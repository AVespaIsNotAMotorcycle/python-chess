from unittest import TestCase
from board import Board, generatepieces
from piece import Piece

class TestingBoard(TestCase):
  # Test the constructor
  def test_constructor(self):
    testBoard = Board(generatepieces())
    assert (isinstance(testBoard, Board))

  # Test the fetchpiece() method
  def test_fetchpiece(self):
    testBoard = Board(generatepieces())
    pieces = generatepieces()
    for piece in pieces:
      pcoords = piece.getcoords()
      assert (testBoard.fetchpiece(pcoords) == piece)

  # Test the moveinrange() method
  def test_moveinrange(self):
    testBoard = Board(generatepieces())
    pieces = generatepieces()
    # Test that Pawn in a2 can move to a3, a4, and not a5 or a1
    # To a3
    s = (1,2)
    d = (1,3)
    p = testBoard.fetchpiece(s)
    inrange = testBoard.moveinrange(s,d,p)
    assert (inrange == True)
    # to a4
    d = (1,4)
    inrange = testBoard.moveinrange(s,d,p)
    assert (inrange == True)
    # to a5
    d = (1,5)
    inrange = testBoard.moveinrange(s,d,p)
    assert (inrange == False)
    # to a1
    d = (1,1)
    inrange = testBoard.moveinrange(s,d,p)
    assert (inrange == False)
    # Test that Queen at d4 in empty board can move all over
    queen = Piece("Queen",'Q',[('x',0),('x','x'),(0,'x')],1,(4,4),9)
    testBoard = Board([queen])
    # to a1
    s = (4,4)
    d = (1,1)
    p = queen
    inrange = testBoard.moveinrange(s,d,p)
    # to d1
    d = (4,1)
    inrange = testBoard.moveinrange(s,d,p)
    # to g1
    d = (7,1)
    inrange = testBoard.moveinrange(s,d,p)
    # to a4
    d = (1,4)
    inrange = testBoard.moveinrange(s,d,p)
    # to h4
    d = (8,4)
    inrange = testBoard.moveinrange(s,d,p)
    # to a7
    d = (1,7)
    inrange = testBoard.moveinrange(s,d,p)
    # to d8
    d = (4,8)
    inrange = testBoard.moveinrange(s,d,p)
    # to h8
    d = (8,8)
    inrange = testBoard.moveinrange(s,d,p)

  def test_cancapture(self):
    # Given board with 3 pieces:
    # white queen in d4
    # white rook in a1
    # black rook in h8
    pieces = [
      Piece("Queen",'Q',[('x',0),('x','x'),(0,'x')],1,(4,4),9),
      Piece("Rook",'R',[('x',0),(0,'x')],1,(1,1),5),
      Piece("Rook",'r',[('x',0),(0,'x')],2,(8,8),5)
    ]
    testBoard = Board(pieces)
    s = (4,4)
    p = pieces[0]
    # check that queen can go to empty tile
    d = (8,1)
    cancapture = testBoard.cancapture(s,d,p)
    assert (cancapture == True)
    # check that queen can go to h8
    d = (8,8)
    cancapture = testBoard.cancapture(s,d,p)
    assert (cancapture == True)
    # check that queen cannot go to a1
    d = (1,1)
    cancapture = testBoard.cancapture(s,d,p)
    assert (cancapture == False)

  def test_pawncapture(self):
    # white pawn at b5 should capture
    # black pawn moving from a7 to a5
    testBoard = Board([
      Piece("Pawn",'P',[(0,1),(0,2)],1,(2,5),1),
      Piece("Pawn",'p',[(0,-1),(0,-2)],2,(1,5),1)
    ])
    testBoard.moves.append(((1,7),(1,5),testBoard.pieces[1]))
    s = (2,5)
    d = (1,6)
    p = testBoard.pieces[0]
    cancapture = testBoard.validpawncapture(s,d,p)
    assert (cancapture == True)

    # white pawn at b5 should capture
    # black pawn moving from c7 to c5
    testBoard = Board([
      Piece("Pawn",'P',[(0,1),(0,2)],1,(2,5),1),
      Piece("Pawn",'p',[(0,-1),(0,-2)],2,(3,5),1)
    ])
    testBoard.moves.append(((3,7),(3,5),testBoard.pieces[1]))
    s = (2,5)
    d = (3,6)
    p = testBoard.pieces[0]
    cancapture = testBoard.validpawncapture(s,d,p)
    assert (cancapture == True)

    # white pawn at b5 should capture
    # black pawn at a6
    testBoard = Board([
      Piece("Pawn",'P',[(0,1),(0,2)],1,(2,5),1),
      Piece("Pawn",'p',[(0,-1),(0,-2)],2,(1,6),1)
    ])
    s = (2,5)
    d = (1,6)
    p = testBoard.pieces[0]
    cancapture = testBoard.validpawncapture(s,d,p)
    assert (cancapture == True)

    # white pawn at b5 should capture
    # black pawn at c6
    testBoard = Board([
      Piece("Pawn",'P',[(0,1),(0,2)],1,(2,5),1),
      Piece("Pawn",'p',[(0,-1),(0,-2)],2,(3,6),1)
    ])
    s = (2,5)
    d = (3,6)
    p = testBoard.pieces[0]
    cancapture = testBoard.validpawncapture(s,d,p)
    assert (cancapture == True)

    # white pawn at b5 should not capture
    # black pawn at b6
    testBoard = Board([
      Piece("Pawn",'P',[(0,1),(0,2)],1,(2,5),1),
      Piece("Pawn",'p',[(0,-1),(0,-2)],2,(2,6),1)
    ])
    s = (2,5)
    d = (2,6)
    p = testBoard.pieces[0]
    cancapture = testBoard.validpawncapture(s,d,p)
    assert (cancapture == False)
