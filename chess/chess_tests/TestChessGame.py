import sys
sys.path.append('..')
import ChessLogic as logic
import ChessGame as game
import ChessPieces as piece
import ChessPlayers as players
import numpy as np
import time
import ChessBoard as board

if __name__=="__main__":
    np.random.seed(0)
    test_game = game.Game(10, 8)

    random_p = players.RandomPlayer(test_game)
    whites_turn = True
    
    while test_game.get_game_ended(test_game.cur_player) == None:
        move = random_p.play(test_game.board)
        test_game.get_next_state(test_game.cur_player, move)
        matrix_board = test_game.convert_to_nums()
        if not whites_turn:
            matrix_board = np.flip(matrix_board, 1)
            whites_turn = True
        else:
            whites_turn = False
        attacked_pos = test_game.board.get_all_attacked_positions(test_game.cur_player)
        print(attacked_pos)
        print(board.game(np.transpose(matrix_board)))
        time.sleep(3)
