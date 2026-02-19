from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.running = True
        self.player_turn = 1 # or 2

    def play(self):
        while self.running:
            self.prompt_selection()

    def prompt_selection(self):
        print(self.board)
        user_input = input("select start square: ") # eg. 'E 2'
        
        data = user_input.split()

        col = data[0]
        row = int(data[1])

    def select_start_square(self, square):
        pass

    def select_destination_square(self, square):
        pass



game = Game()
game.play()
