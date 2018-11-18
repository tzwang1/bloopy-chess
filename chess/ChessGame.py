import numpy as np
import ChessLogic as logic
import ChessPieces as piece

encoder = {}
encoder["p"] = 1
encoder["n"] = 2
encoder["b"] = 3
encoder["r"] = 4
encoder["q"] = 5
encoder["k"] = 6

class Game():
    def __init__(self, time, n):
        '''
        Initializes initial game state
        '''
        self.time = time
        self.board = logic.Board(n)
        self.cur_player = 1
    
    def get_next_state(self, player, action):
        '''
        Get the next board state when action is taken by player.
        '''
        if player != self.cur_player:
            print("Incorrect player!")

        self.board.execute_action(action)
        self.cur_player *= -1
        self.board.switch_orientation()
        
    def get_game_ended(self):
        '''
        Check if the game has ended (checkmate, or stalemate).
        and return 1 if the player one, -1 if the player lost, 
        and 0 if it is a stalemate.
        '''

        if self.board.stalemate(self.cur_player):
            return True
        
        if self.board.king_in_checkmate(self.cur_player):
            return True
        
        return False

    def convert_to_nums(self):
        '''
        Returns the board state in the form of 
        a numerial matrix represention.
        0 represents an unoccupied spot
        1 - white pawn
        2 - white knight
        3 - white bishop
        4 - white rook
        5 - white queen
        6 - white king
        -1 - black pawn
        -2 - black knight
        -3 - black bishop
        -4 - black rook
        -5 - black queen
        -6 - black king
        '''
        matrix_board = np.zeros((self.board.n, self.board.n),dtype=int)
        for i in range(self.board.n):
            for j in range(self.board.n):
                if self.board.board[i,j] == None:
                    value = 0
                else:
                    cur_piece = self.board.board[i,j]
                    if cur_piece.player == 1:
                        player_mult = 1
                    else:
                        player_mult = -1
                    
                    if isinstance(cur_piece, piece.Pawn):
                        value = player_mult * encoder["p"]
                    elif isinstance(cur_piece, piece.Knight):
                        value = player_mult * encoder["n"]
                    elif isinstance(cur_piece, piece.Bishop):
                        value = player_mult * encoder["b"]
                    elif isinstance(cur_piece, piece.Rook):
                        value = player_mult * encoder["r"]
                    elif isinstance(cur_piece, piece.Queen):
                        value = player_mult * encoder["q"]
                    elif isinstance(cur_piece, piece.King):
                        value = player_mult * encoder["k"]
                    else:
                        print("Something went wrong! Invalid Piece")

                matrix_board[i][j] = value

        return matrix_board
    
         
    
