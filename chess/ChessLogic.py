import numpy as np
import ChessPieces as piece
'''
Board class
Board data:
1 = white -1 = black
K = king
Q = queen
R = rook
B = bishop
N = knight
P = pawn
None is an empty spot
w_k is the  white king
b_q is the black queen
first dim is column, 2nd is row:
    piece[1][7] is the square in column 2
    at the opposite end of the board in row 8
'''
def initializePieces():
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    # Initialize white pieces
    w_pieces["w_K"] = piece.King((4,0), 1)
    w_pieces["w_Q"] = piece.Queen((3,0), 1)
    w_pieces["w_B_l"] = piece.Bishop((2,0), 1)
    w_pieces["w_B_r"] = piece.Bishop((5,0), 1)
    w_pieces["w_N_l"] = piece.Knight((1,0), 1)
    w_pieces["w_N_r"] = piece.Knight((6,0), 1)
    w_pieces["w_R_l"] = piece.Rook((0,0), 1)
    w_pieces["w_R_r"] = piece.Rook((7,0), 1)
    w_pieces["w_P_0"] = piece.Pawn((0,1), 1)
    w_pieces["w_P_1"] = piece.Pawn((1,1), 1)
    w_pieces["w_P_2"] = piece.Pawn((2,1), 1)
    w_pieces["w_P_3"] = piece.Pawn((3,1), 1)
    w_pieces["w_P_4"] = piece.Pawn((4,1), 1)
    w_pieces["w_P_5"] = piece.Pawn((5,1), 1)
    w_pieces["w_P_6"] = piece.Pawn((6,1), 1)
    w_pieces["w_P_7"] = piece.Pawn((7,1), 1)
    
    # Initialize black pieces
    b_pieces["b_K"] = piece.King((4,7), -1)
    b_pieces["b_Q"] = piece.Queen((3,7), -1)
    b_pieces["b_B_l"] = piece.Bishop((2,7), -1)
    b_pieces["b_B_r"] = piece.Bishop((5,7), -1)
    b_pieces["b_N_l"] = piece.Knight((1,7), -1)
    b_pieces["b_N_r"] = piece.Knight((6,7), -1)
    b_pieces["b_R_l"] = piece.Rook((0,7), -1)
    b_pieces["b_R_r"] = piece.Rook((7,7), -1)
    b_pieces["b_P_0"] = piece.Pawn((0,6), -1)
    b_pieces["b_P_1"] = piece.Pawn((1,6), -1)
    b_pieces["b_P_2"] = piece.Pawn((2,6), -1)
    b_pieces["b_P_3"] = piece.Pawn((3,6), -1)
    b_pieces["b_P_4"] = piece.Pawn((4,6), -1)
    b_pieces["b_P_5"] = piece.Pawn((5,6), -1)
    b_pieces["b_P_6"] = piece.Pawn((6,6), -1)
    b_pieces["b_P_7"] = piece.Pawn((7,6), -1)

    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    return all_pieces

def initializeBoard(all_pieces, n):
    
    w_pieces = all_pieces["w_pieces"]
    b_pieces = all_pieces["b_pieces"]
    # Assign pieces to a board
    board = np.empty((n,n), dtype=object)
    
    # Assign white pieces
    for key in w_pieces:
        board[w_pieces[key].pos[0]][w_pieces[key].pos[1]] = w_pieces[key]
    
    # Assign black pieces
    for key in b_pieces:
        board[b_pieces[key].pos[0]][b_pieces[key].pos[1]] = b_pieces[key]
    
    return board

class Board():
    def __init__(self, n):
        '''
        Set up initial board configuration.
        '''
        self.n = n
        self.pieces = initializePieces()

        # Adding pieces to the board (always starts from perspective of white player
        self.board = initializeBoard(self.pieces, n)
 
    def __getitem__(self, pos):
        x, y = pos
        return self.board[x][y]
    
    def __str__(self):
        return str(self.board)
if __name__=="__main__":
    b_K = piece.King((4,0), -1)
    a = np.array([b_K])
    print(a[0])
    board = Board(8)
    print(board)
    #print(board[0])
    print(board[0,1])
