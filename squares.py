class Square:
    def __init__(self, letter, number, piece):
        self.letter = letter 
        self.number = number 
        self.piece = piece

    def get_piece(self):
        return self.piece

    def get_pos(self):
        return [self.letter, self.number]

    def get_letter(self):
        return self.letter

    def get_number(self):
        return self.number

    def set_piece(self, piece):
        self.piece = piece
    
    def clear(self):
        self.piece = None

    def is_ocupied(self):
        return True if self.piece else False