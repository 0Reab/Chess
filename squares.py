from pieces import Piece


class Square:
    def __init__(self, letter, number, piece):
        self.letter = letter 
        self.number = number 
        self.piece = piece

    def get_piece(self) -> Piece | None:
        '''Get piece object of this square if piece.exists == True'''
        return self.piece if self.piece.exists else None

    def get_pos(self) -> tuple[str, int]:
        '''Get square notation eg. -> ["E", 4]'''
        return [self.letter, self.number]

    def set_piece(self, piece) -> None:
        '''Update square with new piece'''
        # mby do some checks here idek
        self.piece = piece
    
    def clear(self) -> None:
        '''Clear square by instanciating new empty piece object'''
        self.piece = Piece(self.letter, self.number, captured=True)

    def is_ocupied(self) -> bool:
        '''Check piece object of the square, does piece.exists == True'''
        return self.piece.exists