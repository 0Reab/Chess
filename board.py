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

    def __get_diagonal_half(self, square, direction) -> list[int]:
        '''Helper method - Get half of a diagonal of the input square, specify direction via compass sign "NW" -> northwest half diagonal'''
        result = []

        # top left half of the diagonal
        current = self.get_array_idx(square)
        x, y = current[0], current[1]

        while True:
            match direction: # compass world directions
                case 'NW': current = [ x+1, y-1 ] # (1 step top left square)
                case 'NE': current = [ x+1, y+1 ] # (1 step top right square)
                case 'SW': current = [ x-1, y-1 ] # (1 step bottom left square)
                case 'SE': current = [ x-1, y+1 ] # (1 step bottom right square)

            x, y = current[0], current[1]

            if self.in_bounds(x, y):
                result.append(current)
            else:
                break

        return result

    def get_diagonal(self, square, direction: str) -> list[Square]:
        '''Full diagonal for eg - from: North West -> South East (top left -> bottom right) of your given square - Choose diagonal "NW-SE" or "NE-SW" with arg'''

        # chosen diagonal from arg
        if direction == 'NW-SE':
            top_dir, bottom_dir = 'NW', 'SE'
        if direction == 'NE-SW':
            top_dir, bottom_dir = 'NE', 'SW'

        # get diagonal halves (lists of indices)
        top_idxs = self.__get_diagonal_half(square, top_dir)
        bottom_idxs = self.__get_diagonal_half(square, bottom_dir)

        # reverse top, result arr starts from board edge
        top_squares = [ self.board[row][col] for row, col in top_idxs ][::-1]
        bottom_squares = [ self.board[row][col] for row, col in bottom_idxs]

        diagonal = top_squares + [square] + bottom_squares

        return diagonal

    def in_bounds(self, x=None, y=None, array=None) -> bool:
        '''Check if indices x and y (or array [x,y]) are within board array bounds'''
        if array:
            x, y = array[0], array[1]
        return x in range(0,8) and y in range(0,8)

    def get_square(self, position) -> Square:
        '''From notation (eg. E4) return square object from the board'''
        # row is number, col is letter E4
        col, row = position
        row = int(row)
        row -= 1 # adjust for 0 indexed array;
        col_idx = 0

        for idx, letter in enumerate(self.letters):
            if col == letter:
                col_idx = idx

        square = self.board[row][col_idx]
        return square

    def get_knight_moves(self, square) -> list[Square]:
        current = self.get_array_idx(square)
        x, y = current[0], current[1] # current xy pos

        coord_list = [ # knight transforms
            [ x+2, y-1 ], # NW top
            [ x+1, y-2 ], # NW dwn

            [ x+2, y+1 ], # NE top
            [ x+1, y+2 ], # NE dwn

            [ x-2, y-1 ], # SW top
            [ x-1, y-2 ], # SW dwn

            [ x-2, y+1 ], # SE top
            [ x-1, y+2 ] # SE dwn
        ]

        squares = [ self.board[x][y] for x, y in coord_list if self.in_bounds(x, y) ]

        return squares

    def get_moves(self, square) -> list[Square]:
        '''All possible piece moves of the given square -> obsolete'''
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
    
    def get_king_square(self, color) -> Square:
        king = None
        for row in self.board:
            for square in row:
                if square.piece.kind == 'king' and square.piece.color == color:
                    king = square
                    break

        if king == None:
            raise ValueError("King not on the board lol")
        return king
    
    def get_rooks_for_castling(self, color) -> list:
        '''Returns a list of rooks that haven't moved yet of your player color - still have castling rights'''
        result = []
        if color == 'W': # first row corner squares
            rook1 = self.board[0][0]
            rook2 = self.board[0][-1]

        if color == 'B': # last row corner squares
            rook1 = self.board[-1][0]
            rook2 = self.board[-1][-1]
        
        if rook1.is_ocupied():
            if not rook1.piece.has_moved():
                result.append(rook1)

        if rook2.is_ocupied():
            if not rook2.piece.has_moved():
                result.append(rook2)
        
        return result