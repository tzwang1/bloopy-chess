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

print("Passed tests for ChessPieces.py")

print("Running unit tests for ChessGame.py")
