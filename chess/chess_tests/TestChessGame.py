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
    
    while not test_game.get_game_ended():
        move = random_p.play()
        test_game.get_next_state(test_game.cur_player, move)
        random_p.promote_pawn()
        matrix_board = test_game.convert_to_nums()
        if not whites_turn:
            matrix_board = np.flip(matrix_board, 1)
            whites_turn = True
        else:
            whites_turn = False
        print(board.game(np.transpose(matrix_board)))
        time.sleep(2)
