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
    
    def check_legal(self, action, player, pos):
        '''
        Checks if an action is legal.
        '''
        new_pos = [pos[0] + action[0], pos[1] + action[1]]
        if (new_pos[0] < 0 or new_pos[0] > 7 or new_pos[1] < 0 or new_pos[1] > 7): 
            return False
                
        if self.board[new_pos[0], new_pos[1]] == None:
            return True
        
        cur_piece = self.board[new_pos[0], new_pos[1]]
        if cur_piece.player == player:
            return False
        else: 
            return True
    
    def check_legal_pawn(self, action, player, pos):
        '''
        Checks if an action is legal for pawn pieces.
        '''
        new_pos = [pos[0] + action[0], pos[1] + action[1]]
        if (new_pos[0] < 0 or new_pos[0] > 7 or new_pos[1] < 0 or new_pos[1] > 7): 
            return False
 
        if action == (0,2):
            if pos[1] != 1:
                return False
            
            if self.board[new_pos[0], new_pos[1]-1] != None or self.board[new_pos[0], new_pos[1]] != None:
                return False

            return True
        
        elif action == (0,1):
            if self.board[new_pos[0], new_pos[1]] != None:
                return False
            else:
                return True
        
        # Action to capture an opponent piece
        elif action == (-1,1) or action == (1,1):
            cur_piece = self.board[new_pos[0], new_pos[1]]
            if cur_piece == None:
                other_piece = self.board[new_pos[0], new_pos[1]-1]
                if other_piece == None:
                    return False
                else:
                    if other_piece.player != player and type(other_piece) == piece.Pawn:
                        if other_piece.enpassant:
                            return True
                        else:
                            return False
            elif cur_piece.player == player:
                return False
        
        return False

    def get_legal_actions_piece(self, cur_piece):
        '''
        Returns a list of all the legal actions for the given piece.
        (1 for white piece, -1 for black piece)
        '''
       
        legal_actions = []
        legal_actions.append(cur_piece)
        
        # Different action behaviour for pawns, so must be handled separately
        if isinstance(cur_piece, piece.Pawn):
            for action in cur_piece.actions:
                if self.check_legal_pawn(action, cur_piece.player, cur_piece.pos):
                    legal_actions.append(action)
        else:
            for action in cur_piece.actions:
                for speed in cur_piece.speed:
                    cur_action = [action[0]*speed, action[1]*speed]
                    if self.check_legal(cur_action, cur_piece.player, cur_piece.pos):
                        legal_actions.append(cur_action)
                    else:
                        break
        return legal_actions

    def get_legal_actions(self, player):
        '''
        Returns a list of all legal actions
        '''
        legal_actions = []
        if player == 1:
            pieces = self.pieces["w_pieces"]
        else:
            pieces = self.pieces["b_pieces"]
        
        for key in pieces:
            legal_actions.append(self.get_legal_actions_piece(pieces[key]))

        return legal_actions

    def execute_action(self, action):
        '''
        Executes an action on the board
        '''
        cur_piece = action[0]
        action = action[1]

        cur_pos = cur_piece.pos
        new_pos = [cur_pos[0] + action[0], cur_pos[1] + action[1]]
        self.board[new_pos[0], new_pos[1]] = cur_piece
        self.board[cur_pos[0], cur_pos[1]] = None


if __name__=="__main__":
    board = Board(8)
    print(board)
    legal_actions = board.get_legal_actions(1)
    print(legal_actions)
