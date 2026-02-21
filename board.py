from squares import Square
from pieces import Piece


class Board:
    def __init__(self):
        self.letters = [ "A", "B", "C", "D", "E", "F", "G", "H" ]
        self.letters_to_idx = {letter: idx for idx, letter in enumerate(self.letters)}
        self.board = self.__init_squares()

    def __repr__(self):
        result = ''

        for row in self.board[::-1]:
        # invert board for white perspective only for visualizing
            for square in row:
                if square.is_ocupied():
                    piece = square.piece.show()
                    result += f'[{piece}]'
                else:
                    result += '[ ]'
            
            result += '\n'
        return result

    def __init_squares(self) -> list:
        '''Initialize pieces to home squares on the board'''
        rows = []
        square = []

        for num in range(1, 9):
            for let in self.letters:
                square.append(Square(let, num, Piece(let, num)))

            rows.append(square)
            square = []

        return rows

    def display_data(self) -> None:
        '''Prints each board row in more detail'''
        print(''.join([f'{self.display_row_data(row)}\n' for row in self.board])) 

    def display_row_data(self, row) -> str:
        '''Helper method for display_data() compiles a string of board row information'''
        row -= 1
        s = ''
        for sqr in self.board[row]:
            s += ''.join(str(sqr.get_pos())) + '-'
            s += ' '.join(sqr.get_piece().get_data()) + '  '
        return s

    def get_array_idx(self, square) -> tuple[int, int]:
        '''Square to board array indices [x,y]'''
        col, row = square.get_pos()
        return [row - 1, self.letters_to_idx[col]]

    def get_horizontal_file(self, square) -> list[Square]:
        '''Get whole row of the input square'''
        row, _ = self.get_array_idx(square)

        return self.board[row]

    def get_vertical_file(self, square) -> list[Square]:
        '''Get whole column of the input square'''
        _, col = self.get_array_idx(square)

        return [ row[col] for row in self.board ]

    def get_diags(self, square) -> list[Square]:
        '''Get whole diagonals of the input square'''
        return NotImplemented

    def get_square(self, position) -> Square:
        '''From notation (eg. E4) return square object from the board'''
        # row is number, col is letter E4
        col, row = position
        row -= 1 # adjust for 0 indexed array;
        col_idx = 0

        for idx, letter in enumerate(self.letters):
            if col == letter:
                col_idx = idx

        square = self.board[row][col_idx]
        return square

    def get_moves(self, square) -> list[Square]:
        '''All possible piece moves of the given square'''
        moves = []
        piece = square.piece

        piece_pos = self.get_array_idx(square)
        horizontal_file = self.get_horizontal_file(square)
        vertical_file = self.get_vertical_file(square)

        x = piece_pos[0]
        y = piece_pos[1]

        if piece.color == 'W':
            x -= piece.range
        else:
            x += piece.range

        new_pos = [x, y]

        moves.append(new_pos)
        return moves