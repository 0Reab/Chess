class Piece:
    def __init__(self, col, row, captured=False):
        self.row = row
        self.col = col 
        self.range = 7
        self.exists = True
        self.has_moved = False
        self.piece_data = self.__square_to_piece(row,col, captured)

        if self.piece_data:
            self.kind, self.color = self.piece_data
        else:
            self.kind, self.color = None, None

    def update(self):
        self.has_moved = True

        match self.kind:
            case 'pawn' | 'king': self.range = 1

    def get_data(self): # simple fetch data
        return [self.kind, self.color]

    def show(self): # just for display
        return self.kind[0]
    
    def __square_to_piece(self, row, col, captured):
        # implement pawn promotion handling when initializing a piece
        if captured:
            self.exists = False 
            return [None, None]

        if row not in [1,2,7,8]:
            self.exists = False
            return [None, None]
        
        color, kind = '', ''

        if row in [1,2]:
            color = "W"
        else:
            color = "B"

        if row in [2,7]:
            kind = 'pawn'
            self.range = 2
            return [kind, color]

        match col:
            case 'A'|'H': kind = 'rook'
            case 'B'|'G': kind = 'knight' ; self.range = -1
            case 'C'|'F': kind = 'bishop'
            case 'D': kind = 'queen'
            case 'E': kind = 'king' ; self.range = 1
        
        return [kind, color]