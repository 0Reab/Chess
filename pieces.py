class Piece:
    def __init__(self, row, col):
        self.row = row
        self.col = col 
        self.range = 8
        self.piece_data = self.__square_to_piece(row,col)

        if self.piece_data:
            self.kind, self.color = self.piece_data
        else:
            self.kind, self.color = None, None

    def get_data(self): # simple fetch data
        return [self.kind, self.color]

    def get_kind(self):
        return self.kind

    def get_color(self):
        return self.color

    def get_row(self):
        return self.row

    def get_col(self):
        return self.col

    def get_range(self):
        return self.range

    def show(self): # just for display
        return self.kind[0] if self.kind else None
    
    def __square_to_piece(self, row, col):
        # implement pawn promotion handling when initializing a piece
        if row not in [1,2,7,8]:
            return None
        
        color, kind = '', ''

        if row in [1,2]:
            color = "W"
        else:
            color = "B"

        if row in [2,7]:
            kind = 'pawn'
            self.range = 1
            return [kind, color]

        match col:
            case 'A'|'H': kind = 'rook'
            case 'B'|'G': kind = 'knight' ; self.range = -1
            case 'C'|'F': kind = 'bishop'
            case 'D': kind = 'queen'
            case 'E': kind = 'king' ; self.range = 1
        
        return [kind, color]