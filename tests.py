from squares import Square
from pieces import Piece
from game import Game
import unittest


class Test(unittest.TestCase):
    '''Test suite, methods are meant to be ran in sequence simulating a game with turns'''
    game = Game()
    board = game.board

    def piece_init(self, notation, color) -> tuple[Square, Piece]:
        square = self.board.get_square(notation)

        self.assertTrue(isinstance(square, Square))
        self.assertTrue(isinstance(square.piece, Piece))
        self.assertEqual(square.piece.color, color)

        return square.piece

    def piece_clear(self, square):
        '''Check if start square has been cleared after move'''
        self.assertTrue(isinstance(square, Square))
        self.assertFalse(square.piece.exists)

    def play_test(self, move, color, illegal=False):
        '''Main move tester, args, black & white moves'''
        start, end = move

        if illegal:
            self.assertFalse(self.game.play(start, end)) # attempts illegal move
            return

        self.assertTrue(self.game.play(start, end)) # plays a move
        piece = self.piece_init(end, color)
        self.assertTrue(piece.has_moved)

        self.piece_clear(self.board.get_square(start))
        print(self.game.board)

        return piece

    def test_pawn_moves(self):
        '''Pawns move two squares e4, e5'''
        white = ['E2', 'E4']
        black = ['E7', 'E5']

        pawn_white = self.play_test(white, 'W')
        pawn_black = self.play_test(black, 'B')

        self.assertEqual(pawn_white.range, 1)
        self.assertEqual(pawn_black.range, 1)
    
    def test_prep_pin(self):
        '''For later pin test'''
        white = ['F1', 'B5']
        black = ['B8', 'C6']

        self.play_test(white, 'W')
        self.play_test(black, 'B')

    def test_other(self):
        ''''''
        white = ['D2', 'D4']
        black = ['D7', 'D5']

        self.play_test(white, 'W')
        self.play_test(black, 'B')
    
    def test_test_pin(self):
        white = ['D1', 'D2']
        black = ['D8', 'D7']
        black_illegal = ['C6', 'D4']

        self.play_test(white, 'W')
        self.play_test(black_illegal, 'B', illegal=True)
        self.play_test(black, 'B')


if __name__ == '__main__':
    unittest.main()