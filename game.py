from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.running = True
        self.player_turn = 1 # or 2

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

            # is move legal
            if desti_square.is_ocupied():
                if self.is_same_color(moving_piece, target_piece):
                    print('invalid move, same color piece on target square')
                    return

                print(f'valid move capturing {target_piece.kind()} on {desti_square.get_pos()}')

            # -> dissalow move conditions -> methods
            # if piece is pinned
            # if your piece is king, and target square is under attack by opponents pieces
            # only move your own pieces xd

            #print(moving_piece)
            #print(start_square)
            #print(desti_square)
            Game.move(moving_piece, start_square, desti_square)

            print(f'valid move to {desti_square.get_pos()}')

    def move(piece, start, destination):
        # move piece and clear previous square
        destination.set_piece(piece)
        start.clear()

    def is_pinned(self):
        return NotImplemented

    def is_square_attacked(self):
        return NotImplemented

    def is_same_color(self, piece_1, piece_2):
        return piece_1.get_color() == piece_2.get_color()

    def prompt_player(self):
        selected = input("select square: ") # eg. 'E 2'
        print(f'square = {selected}')
        
        data = selected.split()

        col = data[0]
        row = int(data[1])

        return [col, row]


game = Game()
game.play()
