from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.running = True
        self.players = ['W', 'B'] # read as ['white', 'black']
        self.player_color = self.players[0]

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
            moving_piece = start_square.get_piece()
            target_piece = desti_square.get_piece()

            if moving_piece.get_color() != self.player_color:
                print('you cant move your opponents pieces')
                continue

            path = self.get_path(moving_piece, start_square, desti_square)
            for square in path:
                if square.is_ocupied():
                    print('invalid move, you cant move thru pieces')
                    continue

            # is move legal
            if desti_square.is_ocupied():
                if self.is_same_color(moving_piece, target_piece):
                    print('invalid move, same color piece on target square')
                    continue

                print(f'valid move capturing {target_piece.get_kind()} on {desti_square.get_pos()}')

            # -> dissalow move conditions -> methods
            # if piece is pinned
            # if your piece is king, and target square is under attack by opponents pieces
            # only move your own pieces xd

            #print(moving_piece)
            #print(start_square)
            #print(desti_square)
            self.move(moving_piece, start_square, desti_square)

            print(f'valid move to {desti_square.get_pos()}')
        
    def get_path(self, piece, start, destination):
        # returns all squares in between start square and destination square
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

        path = full_path[path_start, path_end]

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
