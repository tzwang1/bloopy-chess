import sys
sys.path.append('..')
import ChessLogic as logic
import ChessGame as game
import ChessPieces as piece

print("Running unit tests for ChessPieces.py")
w_king = piece.King((4,0), 1)
b_king = piece.King((4,7), -1)

assert w_king.pos == (4,0)
assert b_king.pos == (4,7)
assert w_king.player == 1
assert b_king.player == -1
assert w_king.has_moved == False

print("Passed tests for ChessPieces.py")

print("Running unit tests for ChessGame.py")
board = logic.Board(8)

assert len(board.pieces["w_pieces"]) == 16
assert len(board.pieces["b_pieces"]) == 16
assert len(board.board) ==  8
assert isinstance(board.board[4,0], piece.King) == True
assert isinstance(board.board[4,7], piece.King) == True
assert isinstance(board.board[1,0], piece.Knight) == True
assert isinstance(board.board[0,0], piece.Rook) == True
assert board.board[5,5] == None

print("\tRunning unit tests for check_legal type functions")
# Creating pieces, and a toy board of size 4x4
all_pieces = {}
w_pieces = {}
b_pieces = {}
w_pieces["w_K"] = piece.King((1,1), 1)
b_pieces["b_K"] = piece.King((3,1), -1)
all_pieces["w_pieces"] = w_pieces
all_pieces["b_pieces"] = b_pieces 

board = logic.initializeBoard(all_pieces, 4)
test_board = logic.Board(8)
test_board.pieces = all_pieces
test_board.board = board
legal_actions = test_board.get_legal_actions(1)
print(test_board)
print(legal_actions)
