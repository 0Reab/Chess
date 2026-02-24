class Piece:
    def __init__(self, col, row, captured=False):
        self.row = row
        self.col = col 
        self.range = 7
        self.exists = True
        self.has_moved = False
        self.piece_data = self.__square_to_piece(row,col, captured)

        if self.piece_data:
            self.kind, self.color, self.svg = self.piece_data
        else:
            self.kind, self.color, self.svg = None, None, None

    def update(self) -> None:
        '''Updates piece properties/flags such as move range etc.'''
        self.has_moved = True

        match self.kind:
            case 'pawn' | 'king': self.range = 1

    def get_data(self) -> tuple[str, str]:
        '''Return piece kind and color'''
        return [self.kind, self.color]

    def show(self) -> str:
        '''Display piece, eg. 'p' for pawn'''
        return self.kind[0]
    
    def __square_to_piece(self, row, col, captured) -> tuple[str, str]:
        '''Based on square position, initialize appropriate piece for the square'''
        # implement pawn promotion handling when initializing a piece
        if captured:
            self.exists = False 
            return [None, None, None]

        if row not in [1,2,7,8]:
            self.exists = False
            return [None, None, None]
        
        color, kind, svg = '', '', ''

        if row in [1,2]:
            color = "W"
        else:
            color = "B"

        if row in [2,7]:
            kind = 'pawn'
            self.range = 2
            svg = f'{color.lower()}{kind[0].upper()}'
            return [kind, color, svg]

        match col:
            case 'A'|'H': kind = 'rook'
            case 'B'|'G': kind = 'knight' ; self.range = -1
            case 'C'|'F': kind = 'bishop'
            case 'D': kind = 'queen'
            case 'E': kind = 'king' ; self.range = 1
        
        svg = f'{color.lower()}{kind[0].upper()}'

        if kind == 'knight': # ductape edgecase
            svg = color.lower()+'N'

        return [kind, color, svg]