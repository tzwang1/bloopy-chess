import sys
import numpy as np
import pytest
sys.path.append('..')
import ChessLogic as logic
import ChessGame as game
import ChessPieces as piece
import ChessPlayers as players

# ============================================================================
# Unit tests for ChessPieces.py
# ============================================================================

def test_chess_pieces():
    w_king = piece.King((7,4), 1)
    b_king = piece.King((0,4), -1)

    assert w_king.pos == (7,4)
    assert b_king.pos == (0,4)
    assert w_king.player == 1
    assert b_king.player == -1
    assert w_king.has_moved == False

# ============================================================================
# Unit tests for ChessLogic.py
# ============================================================================

def test_chess_logic():
    board = logic.Board(8)

    assert len(board.pieces["w_pieces"]) == 16
    assert len(board.pieces["b_pieces"]) == 16
    assert len(board.board) ==  8
    assert isinstance(board.board[7,4], piece.King) == True
    assert isinstance(board.board[0,4], piece.King) == True
    assert isinstance(board.board[0,1], piece.Knight) == True
    assert isinstance(board.board[0,0], piece.Rook) == True
    assert board.board[5,5] == None

def test_execute_action():

    board = logic.Board(8)
    w_P_0 = board.pieces["w_pieces"]["w_P_0"]
    action = (-2,0)
    board.execute_action([w_P_0, action])
    assert w_P_0.pos == (4, 0)
    assert board.board[4,0] == w_P_0

    board.switch_orientation()
    b_P_1 = board.pieces["b_pieces"]["b_P_1"]
    action = (-2,0)
    board.execute_action([b_P_1, action])
    assert b_P_1.pos == (4, 1)
    assert board.board[4,1] == b_P_1

    board.switch_orientation()
    action = (-1,1)
    board.execute_action([w_P_0, action])
    assert w_P_0.pos == (3,1)
    assert board.board[4,0] == None

def test_switch_orientation():
    board = logic.Board(8)
    w_P_0 = board.pieces["w_pieces"]["w_P_0"]
    
    cur_pos = w_P_0.pos
    assert cur_pos == (6,0)
    board.switch_orientation()
    
    cur_pos = w_P_0.pos
    assert cur_pos == (1,0)

def test_check_legal():
    # Creating pieces, and a toy board of size 4x4
    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}
    w_pieces["w_Q"] = piece.Queen((1,1), 1)
    b_pieces["b_Q"] = piece.Queen((3,1), -1)
    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces 

    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n
    legal_actions = test_board.get_legal_actions(1)

    assert legal_actions[w_pieces["w_Q"]] == [[1, 0], [2, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [0, 2], [1, 1], [2, 2]]

def test_check_legal_Pawn():
    n = 8
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}
    w_pieces["w_P_0"] = piece.Pawn((6,0), 1)
    b_pieces["b_P_1"] = piece.Pawn((1,1), -1)
    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n
    legal_actions = test_board.get_legal_actions(1)

    assert legal_actions[w_pieces["w_P_0"]] == [(-1, 0), (-2, 0)]
    w_pawn = w_pieces["w_P_0"]
    action = [-2, 0]
    move = (w_pawn, action)
    test_board.execute_action(move)
    
    legal_actions = test_board.get_legal_actions(1)
    action = legal_actions[w_pawn][0]
    move = (w_pawn, action)
    test_board.execute_action(move)
    
    test_board.switch_orientation()
    legal_actions = test_board.get_legal_actions(-1)
    assert legal_actions[b_pieces["b_P_1"]] == [(-1,0), (-2,0)]

    b_pawn = b_pieces["b_P_1"]
    action = legal_actions[b_pawn][1]
    move = (b_pawn, action)
    test_board.execute_action(move)

    test_board.switch_orientation()
    legal_actions = test_board.get_legal_actions(1)

    assert legal_actions[w_pawn] == [(-1,1), (-1,0)]
    test_board.switch_orientation()
    
    b_pawn = b_pieces["b_P_1"]
    b_pawn.pos = (5,1)

    test_board.board[5,1] = b_pawn
    test_board.switch_orientation()
    legal_actions = test_board.get_legal_actions(1)
    
    assert legal_actions[w_pawn] == [(-1,1), (-1,0)]

def test_check_legal_King():
    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}
    w_pieces["w_K"] = piece.King((0,0), 1)
    b_pieces["b_R_r"] = piece.Rook((2,1), -1)
    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n
    king = test_board.pieces["w_pieces"]["w_K"]
    assert test_board.check_legal_king((0,1),king.player,king.pos) == False
    assert test_board.check_legal_king((1,0),king.player,king.pos) == True

def test_king_in_check():
    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_K"] = piece.King((1,1), 1)
    b_pieces["b_Q"] = piece.Queen((3,1), -1)
    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces
    
    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n 
    
    assert test_board.king_in_check(1) == True

    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_K"] = piece.King((0,1), 1)
    w_pieces["w_Q"] = piece.Queen((0,2), 1)
    b_pieces["b_Q"] = piece.Queen((1,1), -1)
    b_pieces["b_R_r"] = piece.Rook((3,1), -1)

    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces
    
    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n 

    assert test_board.king_in_check(1) == True

def test_king_in_checkmate():
    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_K"] = piece.King((0,0), 1)
    b_pieces["b_Q"] = piece.Queen((1,1), -1)
    b_pieces["b_B_l"] = piece.Bishop((3,3), -1)
    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)
    
    # King is in checkmate
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n
    assert test_board.king_in_checkmate(1) == True
    
    # Move Queen so king is not in checkmate
    queen = test_board.pieces["b_pieces"]["b_Q"]
    queen.pos = (1,3)
    test_board.board[1,1] = None
    test_board.board[1,3] = queen
    assert test_board.king_in_checkmate(1) == False

    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_K"] = piece.King((0,1), 1)
    w_pieces["w_Q"] = piece.Queen((0,2), 1)
    b_pieces["b_Q"] = piece.Queen((1,1), -1)
    b_pieces["b_R_r"] = piece.Rook((3,1), -1)

    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces
    
    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n 

    assert test_board.king_in_checkmate(1) == False

def test_stalemate():
    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_K"] = piece.King((0,0),1)
    b_pieces["b_R_l"] = piece.Rook((1,2),-1)
    b_pieces["b_R_r"] = piece.Rook((2,1),-1)

    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)

    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n

    assert test_board.stalemate(1) == True

    rook = test_board.pieces["b_pieces"]["b_R_l"]
    rook.pos = (2,2)
    test_board.board[1,2] = None
    test_board.board[2,2] = rook

    assert test_board.stalemate(1) == False

def test_promote_pawn():
    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_P_0"] = piece.Pawn((0,0),1)
    b_pieces["b_P_0"] = piece.Pawn((0,2),-1)

    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)

    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n

    piece_list = test_board.promote_pawn()
    
    assert isinstance(piece_list[0], piece.Knight)

def test_king_can_castle():
    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_K"] = piece.King((0,0),1)
    w_pieces["w_R_r"] = piece.Rook((0,3),1)
    b_pieces["b_P_0"] = piece.Pawn((3,2),-1)

    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)

    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n

    action = (0, 2)

    assert test_board.king_can_castle(1, action) == True

    n = 5
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_K"] = piece.King((0,4),1)
    w_pieces["w_R_l"] = piece.Rook((0,0),1)
    b_pieces["b_P_0"] = piece.Pawn((3,2),-1)

    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    board = logic.initialize_board(all_pieces, n)
    test_board = logic.Board(8)

    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n

    action = (0, -2)
    assert test_board.king_can_castle(1, action) == True

# ============================================================================
# Unit tests for ChessGame.py
# ============================================================================
def test_chess_game():
    test_game = game.Game(10, 8)
    assert test_game.time == 10
    assert test_game.cur_player == 1

    board = test_game.board
    assert isinstance(board.pieces["w_pieces"]["w_K"], piece.King) == True
    assert board.pieces["w_pieces"]["w_K"].pos == (7,4)

def test_get_next_state():
    test_game = game.Game(10, 8)
    legal_actions = test_game.board.get_legal_actions(test_game.cur_player)
    w_Knight = test_game.board.pieces["w_pieces"]["w_N_l"]
    
    move = (w_Knight, legal_actions[w_Knight][1])
    test_game.get_next_state(1, move)
    assert isinstance(test_game.board.board[2,0], piece.Knight) == True
    assert test_game.board.pieces["w_pieces"]["w_N_l"].pos == (2,0)
    assert test_game.cur_player == -1

def test_convert_to_nums():
    test_game = game.Game(10, 8)
    matrix_board = test_game.convert_to_nums()
    assert np.array_equal(matrix_board, 
    np.array([[-4, -2, -3, -5, -6, -3, -2, -4],
              [-1, -1, -1, -1, -1, -1, -1, -1],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0], 
              [ 0, 0, 0, 0, 0, 0, 0, 0], 
              [ 1, 1, 1, 1, 1, 1, 1, 1], 
              [ 4, 2, 3, 5, 6, 3, 2, 4]])) == True
                        
    legal_actions = test_game.board.get_legal_actions(test_game.cur_player)
    w_Knight = test_game.board.pieces["w_pieces"]["w_N_l"]
    move = (w_Knight, legal_actions[w_Knight][1])
    test_game.get_next_state(test_game.cur_player, move)
    matrix_board = test_game.convert_to_nums()
    assert np.array_equal(matrix_board, 
    np.array([[4, 0, 3, 5, 6, 3, 2, 4],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [ 2, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0],
              [ 0, 0, 0, 0, 0, 0, 0, 0], 
              [ 0, 0, 0, 0, 0, 0, 0, 0], 
              [ -1, -1, -1, -1, -1, -1, -1, -1], 
              [ -4, -2, -3, -5, -6, -3, -2, -4]])) == True

# ============================================================================
# Unit tests for ChessPlayers.py
# ============================================================================
def test_random_player():
    np.random.seed(0)
    test_game = game.Game(10, 8)

    rand_player = players.RandomPlayer(test_game)
    move = rand_player.play()
   
    assert isinstance(move[0], piece.Pawn) == True
    assert move[1] == (-1,0)

if __name__=="__main__":
    
# ============================================================================
# Unit tests for ChessPieces.py
# ============================================================================
    print("#" * 50)
    print("Running tests for ChessPieces.py")
    test_chess_pieces()
    print("Passed tests for ChessPieces.py")
    print("#" * 50)
    
# # ============================================================================
# # Unit tests for ChessLogic.py
# # ============================================================================
    print("Running tests for ChessLogic.py")
    test_chess_logic()
    print("\tRunning unit test for execute_action")
    test_execute_action()
    print("\tRunning unit tests for switch_orientation")
    test_switch_orientation()
    print("\tRunning unit test for king_in_check")
    test_king_in_check()
    print("\tRunning unit test for king_in_checkmate")
    test_king_in_checkmate()
    print("\tRunning unit test for check_legal")
    test_check_legal()
    print("\tRunning unit test for check_legal_Pawn")
    test_check_legal_Pawn()
    print("\tRunning unit test for check_legal_King")
    test_check_legal_King()
    print("\tRunning unit test for stalemate")
    test_stalemate()
    print("\tRunning unit test for promote_pawn")
    test_promote_pawn()
    print("\tRunning unit test for king_can_castle")
    test_king_can_castle()
    print("Passed tests for ChessLogic.py")
    print("#" * 50)

# ============================================================================
# Unit tests for ChessGame.py
# ============================================================================
    print("Running tests for ChessGame.py")
    test_chess_game()
    print("\tRunning unit test for get_next_state")
    test_get_next_state()
    print("\tRunning unit test for convert_to_nums")
    test_convert_to_nums()
    print("Passed tests for ChessGame.py")
    print("#" * 50)

# ============================================================================
# Unit tests for ChessPlayers.py
# ============================================================================
    print("Running tests for ChessPlayers.py")
    print("\tRunning unit test for RandomPlayer")
    test_random_player()
    print("Passed tests for ChessPlayers.py")
    print("#" * 50)

