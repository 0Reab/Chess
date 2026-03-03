from squares import Square
from pieces import Piece


class Board:
    def __init__(self):
        self.letters = [ "A", "B", "C", "D", "E", "F", "G", "H" ]
        self.letters_to_idx = {letter: idx for idx, letter in enumerate(self.letters)}
        self.board = self.__init_squares()

    def __repr__(self):
        result = ''
        green, red, nocolor = '\033[92m', '\033[91m', '\033[0m'

        for row in self.board[::-1]: # invert board for white perspective only for visualizing
            for square in row:
                if square.is_ocupied():
                    piece = ''
                    if square.piece.color == 'W':
                        piece = green + square.piece.show() + nocolor
                    else:
                        piece = red + square.piece.show() + nocolor
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

    def display_row_data(self, row) -> str:
        '''Helper method for display_data() compiles a string of board row information'''
        row -= 1 # 0 idx adjusted
        s = ''
        for square in self.board[row]:
            s += square.get_notation() + '-' + ' '.join(square.get_piece().get_data()) + '  '

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

        pos = self.get_array_idx(square)
        x, y = pos[0], pos[1] # current square pos

        while True: # iterate over pos transforms based on "direction" until we reach end of the board
            match direction: # compass world directions
                case 'NW': pos = [ x+1, y-1 ] # (1 step top left square)
                case 'NE': pos = [ x+1, y+1 ] # (1 step top right square)
                case 'SW': pos = [ x-1, y-1 ] # (1 step bottom left square)
                case 'SE': pos = [ x-1, y+1 ] # (1 step bottom right square)

            x, y = pos[0], pos[1]

            if self.in_bounds(x, y):
                result.append(pos)
            else:
                break # current transfrom out of bounds, returning result

        return result

    def get_diagonal(self, square, direction: str) -> list[Square]:
        '''Full diagonal for eg - from: North West -> South East (top left -> bottom right) of your given square - Choose diagonal "NW-SE" or "NE-SW" with arg'''
        board = self.board

        # chosen diagonal from arg
        if direction == 'NW-SE':
            top_dir, bottom_dir = 'NW', 'SE'
        if direction == 'NE-SW':
            top_dir, bottom_dir = 'NE', 'SW'

        # get diagonal halves (lists of indices)
        top = self.__get_diagonal_half(square, top_dir)
        bottom = self.__get_diagonal_half(square, bottom_dir)

        top_diag = [ board[row][col] for row, col in top ]
        bottom_diag = [ board[row][col] for row, col in bottom ]

        diagonal = top_diag[::-1] + [square] + bottom_diag # assemble whole diagonal, reverse top arr 

        return diagonal

    def in_bounds(self, x=None, y=None, array=None) -> bool:
        '''Check if indices x and y (or array [x,y]) are within board array bounds'''
        if array:
            x, y = array[0], array[1]
        return x in range(0,8) and y in range(0,8)

    def get_square(self, position) -> Square:
        '''From notation (eg. E4) return square object from the board'''
        col, row = position 
        row = int(row) - 1

        square = self.board[row][self.letters_to_idx[col]]
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