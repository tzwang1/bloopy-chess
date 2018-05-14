import numpy as np

class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        legal_moves = self.game.board.get_legal_actions(self.game.cur_player)
        num_pieces = len(legal_moves)

        rand_piece = np.random.randint(num_pieces)
        num_moves = len(legal_moves[rand_piece][1])

        rand_move = np.random.randint(num_moves)

        move = (legal_moves[rand_piece][0], legal_moves[rand_piece][1][rand_move])

        return move

class AlwaysAttackingPlayer():
    def __init__(self, game):
        self.game = game
    
    def play(self, board):
        legal_moves = self.game.board.get_legal_actions(self.game.cur_player)
        num_pieces = len(legal_moves)
        

