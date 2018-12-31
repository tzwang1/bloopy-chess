import numpy as np

class Player():
    def __init__(self, game):
        self.game = game

class RandomPlayer(Player):

    def play(self):
        legal_moves = self.game.board.get_legal_actions(self.game.cur_player)

        all_moves = []
        for piece in legal_moves:
            for action in legal_moves[piece]:
                all_moves.append([piece, action])
    
        num_moves = len(all_moves)

        rand_move = np.random.randint(num_moves)

        return all_moves[rand_move]
    
    def promote_pawn(self):
        pieces_list = self.game.board.promote_pawn()
        if len(pieces_list) == 0:
            return

        rand_piece = np.random.randint(len(pieces_list)) # Select knight, bishop, rook, queen
        cur_piece = pieces_list[rand_piece]
        if cur_piece.player == 1:
            pieces = self.game.board.pieces["w_pieces"]
            color = "w_pieces"
        else:
            pieces = self.game.board.pieces["b_pieces"]
            color = "b_pieces"
        
        for key in pieces:
            if pieces[key].pos == cur_piece.pos:
                piece_name = key
                self.game.board.board[cur_piece.pos[0], cur_piece.pos[1]] = cur_piece
                pieces[piece_name] = cur_piece
                self.game.board.pieces[color] = pieces
    
                break
        


class AlwaysAttackingPlayer(Player):
    def __init__(self, game):
        self.game = game
    
    def play(self, board):
        legal_moves = self.game.board.get_legal_actions(self.game.cur_player)
        num_pieces = len(legal_moves)
        

