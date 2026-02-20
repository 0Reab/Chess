from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.running = True
        self.players = ['W', 'B'] # aka ['white', 'black']
        self.player_color = self.players[0]
        self.message = lambda error, description: self.msg(error, description)
        self.error = True

    def play(self):
        while self.running:
            board = self.board
            print(board)

            # get players move attempt
            start_square = board.get_square(self.prompt_player())
            desti_square = board.get_square(self.prompt_player())

            # legal and illegal moves of a given piece in this square
            all_piece_moves = board.get_moves(start_square)

            # get pieces from start and destination squares
            moving_piece = start_square.piece
            target_piece = desti_square.piece

            if not self.move_is_legal(moving_piece, target_piece, start_square, desti_square):
                continue

            self.move(moving_piece, start_square, desti_square)

            print()

    def move_is_legal(self, moving_piece, target_piece, start_square, desti_square):
        msg = self.message
        error = self.error
        path = self.get_path(moving_piece, start_square, desti_square)

        if moving_piece.kind == 'pawn':
            if not self.is_pawn_moving_forward(start_square, desti_square):
                return msg(error, 'pawns only go forward')

        if start_square == desti_square:
            return msg(error, 'you cannot move to start square')

        if moving_piece.color != self.player_color:
            return msg(error, 'you cant move your opponents pieces')

        if not self.is_move_in_range(moving_piece, path):
            return msg(error, 'exceeded piece range')

        if self.path_obstructed(path):
            return msg(error, 'you cant move thru pieces')

        if desti_square.is_ocupied():
            if self.is_same_color(moving_piece, target_piece):
                return msg(error, 'same color piece on target square')
            else:
                return msg(error=False, description=f'capturing {target_piece.kind} on {desti_square.get_pos()}')

        return True

    def is_pawn_moving_forward(self, start, desti):
        row_1 = start.number
        row_2 = desti.number

        if self.player_color == 'W':
            return row_1 < row_2
        else:
            return row_1 > row_2

    def path_obstructed(self, path):
        for square in path:
            if square.is_ocupied():
                return True
        return False
    
    def msg(self, error=False, description=''):
        if error:
            msg_type = 'invalid move ->'
        else:
            msg_type = 'valid move ->'
        
        print(f'{msg_type} {description}')
        return error
    
    def is_move_in_range(self, piece, path):
        #print(f'total distance {len(path) + 1} of {piece.get_kind()} of range {piece.get_range()}')
        return piece.range >= len(path) + 1 # path doesn't include end square
        
    def get_path(self, moving_piece, start, destination):
        # returns all squares in between start square and destination square
        if moving_piece.kind == 'knight':
            return []

        path = None
        full_path = None
        board = self.board

        vertical = board.get_vertical_file(start)
        horizontal = board.get_horizontal_file(start)

        if destination in vertical:
            full_path = vertical
        elif destination in horizontal:
            full_path = horizontal

        path_start = full_path.index(start) + 1 # ommit start square: idx+1
        path_end = full_path.index(destination)

        # does not work if start-end indices are end-start
        # therfore invert array and get indices again

        if path_start > path_end:
            full_path = full_path[::-1]

            path_start = full_path.index(start) + 1 # ommit start square: idx+1
            path_end = full_path.index(destination)

        path = full_path[path_start : path_end]
        return path

    def move(self, piece, start, destination):
        # move piece and clear previous square
        piece.update()
        destination.set_piece(piece)
        start.clear()

        if self.player_color == 'W':
            self.player_color = 'B'
        else: 
            self.player_color = 'W'
        
        self.message(error=False, description=f'valid move to {destination.get_pos()}')

    def is_same_color(self, piece_1, piece_2):
        return piece_1.color == piece_2.color

    def prompt_player(self):
        selected = input(f'player {self.player_color} select square: ') # eg. 'E2'

        col = selected[0]
        row = int(selected[1])

        return [col, row]


game = Game()
game.play()
