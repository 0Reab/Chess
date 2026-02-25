from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.running = True
        self.players = ['W', 'B'] # aka ['white', 'black']
        self.player_color = self.players[0]
        self.message = lambda error, description: self.msg(error, description)

    def play(self, start, desti) -> bool:
        '''Main game loop, passing turns'''
        if self.running:
            board = self.board

            # get players move attempt
            start_square = board.get_square(start)
            desti_square = board.get_square(desti)

            # legal and illegal moves of a given piece in this square
            all_piece_moves = board.get_moves(start_square)

            # get pieces from start and destination squares
            moving_piece = start_square.piece
            target_piece = desti_square.piece

            if not self.move_is_legal(moving_piece, target_piece, start_square, desti_square):
                return False

            return self.move(moving_piece, start_square, desti_square)

    def get_board_state(self) -> list:
        '''Data from board for frontend HTML template'''
        result = []
        colors = ['B', 'W']
        i = 0

        for row in self.board.board:
            row_result = []
            # alternate for row (board colors)
            if i:
                i -=1
            else:
                i +=1

            for square in row:
                # alterante B/W each square (board colors) - jank
                if i:
                    i -=1
                else:
                    i +=1

                if square.is_ocupied():
                    row_result.append([square.piece.svg, colors[i], square.get_notation()])
                else:
                    row_result.append(['', colors[i], square.get_notation()])
            result.append(row_result)
        
        return result[::-1] # for player 1 perspective or naur

    def move_is_legal(self, moving_piece, target_piece, start_square, desti_square) -> bool:
        '''Check if move is legal, if not -> give reason via msg()'''
        msg = self.message
        path = self.get_path(moving_piece, start_square, desti_square)

        if start_square == desti_square:
            return msg(False, 'you cannot move to start square')

        if moving_piece.color != self.player_color:
            return msg(False, 'you cant move your opponents pieces')

        if path == None:
            return msg(False, 'cannot find path to destination square')

        if moving_piece.kind == 'king':
            if self.is_square_attacked(start_square, desti_square):
               return msg(False, 'king can not go to attacked square')

        if moving_piece.kind == 'pawn':
            if not self.is_pawn_moving_forward(start_square, desti_square):
                return msg(False, 'pawns only go forward')

            if self.is_pawn_moving_diagonally(start_square, desti_square):
                if self.is_pawn_capture_valid(desti_square, path):
                    return msg(False, 'illegal pawn capture')
            else:
                if desti_square.is_ocupied():
                    return msg(False, 'pawns path forward is blocked')

        if moving_piece.kind == 'knight':
            if desti_square not in self.board.get_knight_moves(start_square):
                return msg(False, 'destination not in knight square list')

        if not self.is_move_in_range(moving_piece, path):
            return msg(False, 'exceeded piece range')

        if self.path_obstructed(path):
            return msg(False, 'you cant move thru pieces')

        if desti_square.is_ocupied():
            if self.is_same_color(moving_piece, target_piece):
                return msg(False, 'same color piece on target square')
            else:
                return msg(True, description=f'capturing {target_piece.kind} on {desti_square.get_pos()}')

        return msg(True, description=f'{desti_square.get_pos()}')

    def is_square_attacked(self, start, desti):
        '''Check if square is attacked by opponents piece (for king mainly)'''
        my_color = self.player_color
        board = self.board
        possible_knight_moves = self.board.get_knight_moves(desti)

        # check if knight is attacking the destination square
        for square in possible_knight_moves:
            if square.piece.kind == 'knight':
                if square.piece.color != my_color:
                    return True

        # checking if square is covered by opponents pawn
        # take destination square and find its diagonal 1 up left, and 1 up right squares (respectively for color)
        x, y = board.get_array_idx(desti)
        if my_color == 'W': # adjust row based on player color
            x +=1
        else:
            x -=1

        top_left = [x, y-1]
        top_right = [x, y+1]

        left_valid = board.in_bounds(array=top_left)
        right_valid = board.in_bounds(array=top_right)

        if left_valid:
            row, col = top_left[0], top_left[1]
            square_left = board.board[row][col]
            if square_left.piece.kind == 'pawn' and square_left.piece.color != my_color: 
                return True

        if right_valid:
            row, col = top_right[0], top_right[1]
            square_right = board.board[row][col]
            if square_right.piece.kind == 'pawn' and square_right.piece.color != my_color: 
                return True
        
        # pawns are not attacking the square - checking for other pieces now (rooks, bishops, queen and king)
        # check files and diags for unobstructed paths to opponent piece

        diagnonal_ne_sw = board.get_diagonal(desti, 'NE-SW')
        diagnonal_nw_se = board.get_diagonal(desti, 'NW-SE')

        vertical = board.get_vertical_file(desti)
        horizontal = board.get_horizontal_file(desti)

        x, y = board.get_array_idx(desti)

        def can_piece_see_the_square(aggressor, full_path, desti, moving_piece):
            for square in full_path:
                if square.piece.kind == aggressor and square.piece.color != my_color:
                    path = self.get_path(moving_piece, desti, square) # odd args because we are checking for desti square not start
                    if aggressor == 'king':
                        if len(path) <= 0:
                            print(f'hit king edge case for {aggressor} - {len(path)}')
                            return True # edge case for the king
                        return
                    if not self.path_obstructed(path):
                        print(f'hit king edge case for {aggressor} - {len(path)}')
                        return True # opponent "piece" can see us

        if can_piece_see_the_square('rook', vertical, desti, start.piece):
            return True
        if can_piece_see_the_square('rook', horizontal, desti, start.piece):
            return True

        if can_piece_see_the_square('bishop', diagnonal_ne_sw, desti, start.piece):
            return True
        if can_piece_see_the_square('bishop', diagnonal_nw_se, desti, start.piece):
            return True

        all_directions = [vertical, horizontal, diagnonal_nw_se, diagnonal_ne_sw]
        for dir in all_directions:
            if can_piece_see_the_square('queen', dir, desti, start.piece):
                return True
            if can_piece_see_the_square('king', dir, desti, start.piece):
                return True

    def is_pawn_moving_forward(self, start, desti) -> bool:
        '''Determine move direction based on player color and start-end squares'''
        row_1 = start.number
        row_2 = desti.number

        if self.player_color == 'W':
            return row_1 < row_2
        else:
            return row_1 > row_2
    
    def is_pawn_moving_diagonally(self, start, desti) -> bool:
        '''Compare column idx of two squares'''
        col1 = self.board.get_array_idx(start)[1]
        col2 = self.board.get_array_idx(desti)[1]

        return col1 != col2

    def is_pawn_capture_valid(self, desti, path) -> bool:
        '''Check if pawn capture attempt is legal - en pessant not implemented yet'''
        return len(path) != 0 or desti.is_ocupied() == False # one diagonal square has lenght of path of 0

    def path_obstructed(self, path) -> bool:
        '''Check each square in between start square and end square'''
        if path == None:
            return True
        for square in path:
            if square.is_ocupied():
                return True
        return False
    
    def msg(self, result, description='') -> None:
        '''Print reason for error and return bool'''
        if result == True:
            msg_type = 'valid move ->'

        if result == False:
            msg_type = 'invalid move ->'
        
        print(f'{msg_type} {description}')
        return result
    
    def is_move_in_range(self, piece, path) -> bool:
        '''Check piece range against path to destination'''
        return piece.range >= len(path) + 1 # path doesn't include end square
        
    def get_path(self, moving_piece, start, destination) -> list:
        '''Returns all squares in between start square and destination square'''
        if moving_piece.kind == 'knight':
            return []

        path = None
        full_path = None
        board = self.board

        vertical = board.get_vertical_file(start)
        horizontal = board.get_horizontal_file(start)

        diagonal_nw_se = board.get_diagonal(start, direction='NW-SE')
        diagonal_ne_sw = board.get_diagonal(start, direction='NE-SW')

        # something is bugd here fo sho
        if moving_piece.kind in ['king', 'queen', 'pawn', 'rook']:
            if destination in vertical:
                full_path = vertical
            elif destination in horizontal:
                full_path = horizontal

        if moving_piece.kind in ['king', 'queen', 'pawn', 'bishop']:
            if destination in diagonal_nw_se:
                full_path = diagonal_nw_se
            elif destination in diagonal_ne_sw:
                full_path = diagonal_ne_sw
        
        if full_path == None: # failsafe check
            return None

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

    def move(self, piece, start, destination) -> bool:
        '''Move the piece and clear previous square -> log message'''
        # move piece and clear previous square
        piece.update()
        destination.set_piece(piece)
        start.clear()

        if self.player_color == 'W':
            self.player_color = 'B'
        else: 
            self.player_color = 'W'
        
        return True

    def is_same_color(self, piece_1, piece_2) -> bool:
        '''Are two pieces same color'''
        return piece_1.color == piece_2.color

    def prompt_player(self) -> tuple[str, int]:
        '''Prompt player to select a square eg. "E2" -> and return it'''
        selected = input(f'player {self.player_color} select square: ') # eg. 'E2'

        col = selected[0]
        row = int(selected[1])

        return [col, row]


#game = Game()
#game.play()
