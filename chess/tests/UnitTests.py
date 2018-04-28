import sys
sys.path.append('..')
import ChessLogic as logic
import ChessGame as game
import ChessPieces as piece
def test_chessPieces():
    w_king = piece.King((4,0), 1)
    b_king = piece.King((4,7), -1)

    assert w_king.pos == (4,0)
    assert b_king.pos == (4,7)
    assert w_king.player == 1
    assert b_king.player == -1
    assert w_king.has_moved == False

def test_chessGame():
    board = logic.Board(8)

    assert len(board.pieces["w_pieces"]) == 16
    assert len(board.pieces["b_pieces"]) == 16
    assert len(board.board) ==  8
    assert isinstance(board.board[4,0], piece.King) == True
    assert isinstance(board.board[4,7], piece.King) == True
    assert isinstance(board.board[1,0], piece.Knight) == True
    assert isinstance(board.board[0,0], piece.Rook) == True
    assert board.board[5,5] == None

def test_execute_action():

    board = logic.Board(8)
    w_P_0 = board.pieces["w_pieces"]["w_P_0"]
    action = (0,2)
    board.execute_action([w_P_0, action])
    assert w_P_0.pos == (0, 3)

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

    board = logic.initializeBoard(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n
    legal_actions = test_board.get_legal_actions(1)

    assert legal_actions[0][1] == [[1, 0], [2, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1], [0, 2], [1, 1], [2, 2]]

def test_check_legal_Pawn():
    n = 8
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}
    w_pieces["w_P_0"] = piece.Pawn((0,1), 1)
    b_pieces["b_P_1"] = piece.Pawn((1,6), -1)
    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    board = logic.initializeBoard(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n
    legal_actions = test_board.get_legal_actions(1)
    
    assert legal_actions[0][1] == [(0, 1), (0, 2)]

def test_king_in_check():
    n = 4
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    w_pieces["w_K"] = piece.King((1,1), 1)
    b_pieces["b_Q"] = piece.Rook((3,1), -1)
    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces
    
    board = logic.initializeBoard(all_pieces, n)
    test_board = logic.Board(8)
    test_board.pieces = all_pieces
    test_board.board = board
    test_board.n = n 
    
    assert test_board.king_in_check(1) == True

if __name__=="__main__":
    print("#" * 80)
    print("Running tests for ChessPieces.py")
    test_chessPieces()
    print("Passed tests for ChessPieces.py")
    print("#" * 80)
    
    print("Running tests for ChessGame.py")
    test_chessGame()
    print("\tRunning unit test for execute_action")
    test_execute_action()
    print("\tRunning unit test for check_legal")
    test_check_legal()
    print("\tRunning unit test for check_legal_Pawn")
    test_check_legal_Pawn()
    print("\tRunning unit test for king_in_check")
    test_king_in_check()
    print("Passed tests for ChessGame.py")
    print("#" * 80)
    print('dsf")
