from squares import Square
from pieces import Piece
from game import Game
import unittest


class Test(unittest.TestCase):
    # i should deffo make a separate test case to check if every square has inited ok and piece too, each should have the objects
    '''Test pawns movement, promotion, capturing, two/one square moves'''
    game = Game()
    board = game.board

    def test_piece_init(self, notation) -> tuple[Square, Piece]:
        square = self.board.get_square(notation)

        assert isinstance(square, Square)
        assert isinstance(square.piece, Piece)

        return square, square.piece


    def test_pawn_move(self):
        '''Does pawn move two, and one squares ok'''
        game = self.game
        board = self.board

        move1 = 'E4'
        move2 = 'E5'

        mv1 = game.play('E2', move1) # white plays 2 square pawn move
        assert mv1
        mv2 = game.play('E7', move2) # black plays it too
        assert mv2

        print(board)

        square1, pawn_white = self.test_piece_init(move1)
        square2, pawn_black = self.test_piece_init(move2)

        assert pawn_white.color == 'W'
        assert pawn_black.color == 'B'

        assert pawn_white.range == 1
        assert pawn_black.range == 1

        # check if start squares have been updated properly
        start1 = board.get_square('E2')
        start2 = board.get_square('E7')

        assert isinstance(start1, Square)
        assert isinstance(start2, Square)

        assert start1.is_ocupied
        assert start2.is_ocupied


test = Test()
test.test_pawn_move()