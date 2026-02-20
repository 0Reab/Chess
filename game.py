from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.running = True
        self.players = ['W', 'B'] # aka ['white', 'black']
        self.player_color = self.players[0]

    def play(self):
        while self.running:
            board = self.board
            msg = lambda error, description: self.msg(error, description)
            error = True
            print(board)

            # get players move attempt
            start_square = board.get_square(self.prompt_player())
            desti_square = board.get_square(self.prompt_player())

            # legal and illegal moves of a given piece in this square
            all_piece_moves = board.get_moves(start_square)

            # get pieces from start and destination squares
            moving_piece = start_square.get_piece()
            target_piece = desti_square.get_piece()

            path = self.get_path(moving_piece, start_square, desti_square)

            if moving_piece.get_color() != self.player_color:
                msg(error, 'you cant move your opponents pieces')
                continue

            if not self.is_move_in_range(moving_piece, path):
                msg(error, 'exceeded piece range')
                continue

            if self.path_obstructed(path):
                msg(error, 'you cant move thru pieces')
                continue

            if desti_square.is_ocupied():
                if self.is_same_color(moving_piece, target_piece):
                    msg(error, 'same color piece on target square')
                    continue

                print(f'valid move capturing {target_piece.get_kind()} on {desti_square.get_pos()}')

            self.move(moving_piece, start_square, desti_square)

            print(f'valid move to {desti_square.get_pos()}')

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
    
    def is_move_in_range(self, piece, path):
        # not implemented for nyow
        return True
        
    def get_path(self, moving_piece, start, destination):
        # returns all squares in between start square and destination square
        if moving_piece.get_kind() == 'knight':
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

        print(type(path_start))
        print(type(path_end))

        path = full_path[path_start : path_end]
        return path

    def move(self, piece, start, destination):
        # move piece and clear previous square
        destination.set_piece(piece)
        start.clear()

        if self.player_color == 'W':
            self.player_color = 'B'
        else: 
            self.player_color = 'W'

    def is_same_color(self, piece_1, piece_2):
        return piece_1.get_color() == piece_2.get_color()

    def prompt_player(self):
        selected = input(f'player {self.player_color} select square: ') # eg. 'E2'

        col = selected[0]
        row = int(selected[1])

        return [col, row]


game = Game()
game.play()
