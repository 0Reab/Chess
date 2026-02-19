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
                piece = square.get_piece().show()

                if piece == None:
                    result += '[ ]'
                else:
                    result += f'[{piece}]'
            
            result += '\n'
        return result

    def __init_squares(self):
        rows = []
        square = []

        for num in range(1, 9):
            for let in self.letters:
                square.append(Square(let, num, Piece(num, let)))

            rows.append(square)
            square = []

        return rows

    def display_data(self):
        print(''.join([f'{self.display_row_data(row)}\n' for row in self.board])) 

    def display_row_data(self, row):
        row -= 1
        s = ''
        for sqr in self.board[row]:
            s += ''.join(str(sqr.get_pos())) + '-'
            s += ' '.join(sqr.get_piece().get_data()) + '  '
        return s

    def get_array_idx(self, square):
        col, row = square.get_pos()
        return [row - 1, self.letters_to_idx[col]]

    def get_horizontal_file(self, square):
        row, _ = self.get_array_idx(square)

        return self.board[row]

    def get_vertical_file(self, square):
        _, col = self.get_array_idx(square)

        return [ row[col] for row in self.board ]

    def get_diags(self, square):
        return NotImplemented

    def get_square(self, col, row):
        # row is number, col is letter E4
        row -= 1 # adjust for 0 indexed array;
        col_idx = 0

        for idx, letter in enumerate(self.letters):
            if col == letter:
                col_idx = idx

        square = self.board[row][col_idx]
        return square

    def get_moves(self, square):
        moves = []
        piece = square.get_piece()

        piece_pos = self.get_array_idx(square)
        horizontal_file = self.get_horizontal_file(square)
        vertical_file = self.get_vertical_file(square)

        #diags = self.get_diags(square)

        piece_kind = piece.get_kind()
        piece_color = piece.get_color()
        piece_range = piece.get_range()

        #print(f'{piece_pos[0]} {piece_range}')

        x = piece_pos[0]
        y = piece_pos[1]

        if piece_color == 'w':
            x -= piece_range
        else:
            x += piece_range

        new_pos = [x, y]

        moves.append(new_pos)
        return moves

        #print(f'range={piece_range} pos={piece_pos} ; new={new_pos} ; {piece_kind},{piece_color}')

        #return piece_range


board = Board()

square = board.get_square('E', 2)
row_data = board.display_row_data(1)
pic = square.get_piece()

data = pic.get_data()
board_idx = board.get_array_idx(square)

piece_range = board.get_moves(square)

print(piece_range)
#print(board)
#print(sqr)
#print(pic)
#print(data)
#print(board_idx)
#print(row_data)

#print(files)

'''
for file in files:
    for square in file:
        print(square.get_piece().get_data()[0])
'''