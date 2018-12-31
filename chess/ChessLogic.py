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
def initialize_pieces():
    all_pieces = {}
    w_pieces = {}
    b_pieces = {}

    # Initialize white pieces
    w_pieces["w_K"] = piece.King((7,4), 1)
    w_pieces["w_Q"] = piece.Queen((7,3), 1)
    w_pieces["w_B_l"] = piece.Bishop((7,2), 1)
    w_pieces["w_B_r"] = piece.Bishop((7,5), 1)
    w_pieces["w_N_l"] = piece.Knight((7,1), 1)
    w_pieces["w_N_r"] = piece.Knight((7,6), 1)
    w_pieces["w_R_l"] = piece.Rook((7,0), 1)
    w_pieces["w_R_r"] = piece.Rook((7,7), 1)
    w_pieces["w_P_0"] = piece.Pawn((6,0), 1)
    w_pieces["w_P_1"] = piece.Pawn((6,1), 1)
    w_pieces["w_P_2"] = piece.Pawn((6,2), 1)
    w_pieces["w_P_3"] = piece.Pawn((6,3), 1)
    w_pieces["w_P_4"] = piece.Pawn((6,4), 1)
    w_pieces["w_P_5"] = piece.Pawn((6,5), 1)
    w_pieces["w_P_6"] = piece.Pawn((6,6), 1)
    w_pieces["w_P_7"] = piece.Pawn((6,7), 1)
    
    # Initialize black pieces
    b_pieces["b_K"] = piece.King((0,4), -1)
    b_pieces["b_Q"] = piece.Queen((0,3), -1)
    b_pieces["b_B_l"] = piece.Bishop((0,2), -1)
    b_pieces["b_B_r"] = piece.Bishop((0,5), -1)
    b_pieces["b_N_l"] = piece.Knight((0,1), -1)
    b_pieces["b_N_r"] = piece.Knight((0,6), -1)
    b_pieces["b_R_l"] = piece.Rook((0,0), -1)
    b_pieces["b_R_r"] = piece.Rook((0,7), -1)
    b_pieces["b_P_0"] = piece.Pawn((1,0), -1)
    b_pieces["b_P_1"] = piece.Pawn((1,1), -1)
    b_pieces["b_P_2"] = piece.Pawn((1,2), -1)
    b_pieces["b_P_3"] = piece.Pawn((1,3), -1)
    b_pieces["b_P_4"] = piece.Pawn((1,4), -1)
    b_pieces["b_P_5"] = piece.Pawn((1,5), -1)
    b_pieces["b_P_6"] = piece.Pawn((1,6), -1)
    b_pieces["b_P_7"] = piece.Pawn((1,7), -1)
   
    all_pieces["w_pieces"] = w_pieces
    all_pieces["b_pieces"] = b_pieces

    return all_pieces

def initialize_board(all_pieces, n):
    
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
        self.pieces = initialize_pieces()

        # Adding pieces to the board (always starts from perspective of white player
        self.board = initialize_board(self.pieces, n)

    def __getitem__(self, pos):
        x, y = pos
        return self.board[x][y]
    
    def __str__(self):
        return str(self.board)
    
    def get_all_attacked_positions(self, enemy_player):
        '''
        Returs a list of all positions that are currently being attacked by other_player's pieces
        '''
        if enemy_player == 1:
            pieces = self.pieces["w_pieces"]
        else:
            pieces = self.pieces["b_pieces"]
        
        attacked_pos = []
        for key in pieces:
            # Check if pieces[key] exists on the board
            if self.board[pieces[key].pos] != pieces[key]:
                continue
            cur_piece = pieces[key]
            cur_pos = cur_piece.pos
            for attack in cur_piece.attacking:
                for speed in cur_piece.speed:
                    attacked = (cur_pos[0] + speed * attack[0], cur_pos[1] + speed * attack[1])
                    if attacked[0] <  0 or attacked[0] > self.n-1 or attacked[1] < 0 or attacked[1] > self.n-1:
                        break
                    if self.board[attacked[0], attacked[1]] == None:
                        attacked_pos.append(attacked)
                    else:
                        # There is some piece at attacked position
                        other_piece = self.board[attacked[0], attacked[1]]
                        if other_piece.player != enemy_player:
                            attacked_pos.append(attacked) #Attacked piece belongs to cur player
                        break

        return attacked_pos

    def check_legal(self, action, player, pos):
        '''
        Checks if an action is legal.
        First return value says if the action is legal
        Second return value says if the following actions are legal
        '''
        new_pos = (pos[0] + action[0], pos[1] + action[1])
        # Check if new position is in the board
        if (new_pos[0] < 0 or new_pos[0] > self.n-1 or new_pos[1] < 0 or new_pos[1] > self.n-1): 
            return False, True
    
        # Check if new position is empty
        if self.board[new_pos[0], new_pos[1]] == None:
            return self.king_not_vulnerable(pos, new_pos, player), False
        
        # New position has a piece
        other_piece = self.board[new_pos[0], new_pos[1]]
        if other_piece.player == player:
            return False, True
        else:
            return self.king_not_vulnerable(pos, new_pos, player), True

    
    def check_legal_pawn(self, action, player, pos):
        '''
        Checks if an action is legal for pawn pieces.
        '''
        new_pos = (pos[0] + action[0], pos[1] + action[1])
        if (new_pos[0] < 0 or new_pos[0] > self.n-1 or new_pos[1] < 0 or new_pos[1] > self.n-1): 
            return False
 
        if action == (-2,0):
            if pos[0] != 6:
                return False
            
            if self.board[new_pos[0]+1, new_pos[1]] != None or self.board[new_pos[0], new_pos[1]] != None:
                return False
            else:
                return self.king_not_vulnerable(pos, new_pos, player)

        elif action == (-1,0):
            if self.board[new_pos[0], new_pos[1]] != None:
                return False
            else:
                return self.king_not_vulnerable(pos, new_pos, player)
            
        # Action to capture an opponent piece
        elif action == (-1,1) or action == (-1,-1):
            other_piece = self.board[new_pos[0], new_pos[1]]
            if other_piece == None:
                enpassant_piece = self.board[new_pos[0]+1, new_pos[1]]
                if enpassant_piece == None:
                    return False
                else:
                    if enpassant_piece.player != player and isinstance(enpassant_piece, piece.Pawn):
                        if enpassant_piece.enpassant:
                            return self.king_not_vulnerable(pos, new_pos, player)

            elif other_piece.player != player:
                return self.king_not_vulnerable(pos, new_pos, player)
        
        return False
 
    def check_legal_king(self, action, player, pos):
        '''
        Checks if an action is legal for king pieces.
        '''
        if action == (0,-2) or action == (0,2):
            return self.king_can_castle(player, action)

        new_pos = (pos[0] + action[0], pos[1] + action[1])
        if (new_pos[0] < 0 or new_pos[0] > self.n-1 or new_pos[1] < 0 or new_pos[1] > self.n-1):
            return False

        if player == 1:
            king = self.pieces["w_pieces"]["w_K"]
        else:
            king = self.pieces["b_pieces"]["b_K"]

        if self.board[new_pos[0], new_pos[1]] == None:
            pos = king.pos
            return self.king_not_vulnerable(pos, new_pos, player)

        cur_piece = self.board[new_pos[0], new_pos[1]]
        if cur_piece.player == player:
            return False
        else:
            return self.king_not_vulnerable(pos, new_pos, player)
    
    def king_can_castle(self, player, action):
        '''
        Checks if it is legal for the King to castle
        '''
        if self.king_in_check(player) or self.king_in_checkmate(player):
            return False
        
        if action != (0,-2) and action != (0,2):
            return False

        if player == 1:
            king = self.pieces["w_pieces"]["w_K"]
            if action == (0,-2):
                if "w_R_l" in self.pieces["w_pieces"]:
                    rook = self.pieces["w_pieces"]["w_R_l"]
                    half_action = (0, -1)
                else:
                    return False
            else:
                if "w_R_r" in self.pieces["w_pieces"]:
                    rook = self.pieces["w_pieces"]["w_R_r"]
                    half_action = (0, 1)
                else:
                    return False
        else:
            king = self.pieces["b_pieces"]["b_K"]
            if action == (0,-2):
                if "b_R_l" in self.pieces["b_pieces"]:
                    rook = self.pieces["b_pieces"]["b_R_l"]
                    half_action = (0, -1)
                else:
                    return False
            else:
                if "b_R_r" in self.pieces["b_pieces"]:
                    rook = self.pieces["b_pieces"]["b_R_r"]
                    half_action = (0, 1)
                else:
                    return False
        
        if king.has_moved or rook.has_moved:
            return False

        
        moves = [half_action, action]

        for move in moves:
            new_king_pos = (king.pos[0] + move[0], king.pos[1] + move[1])
            if self.board[new_king_pos[0], new_king_pos[1]] != None:
                return False

            if not self.king_not_vulnerable(king.pos, new_king_pos, player):
                return False
        
        return True


    def king_not_vulnerable(self, pos, new_pos, player):
        '''
        Checks if moving the piece as pos to new_pos will leave the king in check
        '''
        cur_piece = self.board[pos[0], pos[1]]
        other_piece = self.board[new_pos[0], new_pos[1]]

        cur_piece.pos = new_pos
        self.board[pos[0], pos[1]] = None
        self.board[new_pos[0], new_pos[1]] = cur_piece

        if self.king_in_check(player):
            not_vulnerable = False
        else:
            not_vulnerable = True
        
        cur_piece.pos = pos
        self.board[pos[0], pos[1]] = cur_piece
        self.board[new_pos[0], new_pos[1]] = other_piece

        return not_vulnerable
  
    def get_legal_actions_piece(self, cur_piece):
        '''
        Returns a list of all the legal actions for the given piece.
        (1 for white piece, -1 for black piece)
        '''
       
        all_actions = []        
        # Different action behaviour for pawns, so must be handled separately
        if isinstance(cur_piece, piece.Pawn):
            for action in cur_piece.actions:
                if self.check_legal_pawn(action, cur_piece.player, cur_piece.pos):
                    all_actions.append(action)
        elif isinstance(cur_piece, piece.King):
            for action in cur_piece.actions:
                if self.check_legal_king(action, cur_piece.player, cur_piece.pos):
                    all_actions.append(action)
        else:
            for action in cur_piece.actions:
                for speed in cur_piece.speed:
                    cur_action = [action[0]*speed, action[1]*speed]
                    legal, blocked = self.check_legal(cur_action, cur_piece.player, cur_piece.pos)
                    if legal:
                        all_actions.append(cur_action)
                        if blocked:
                            break
                    else:
                        break

        return all_actions

    def get_legal_actions(self, player):
        '''
        Returns a list of all legal actions
        '''
        legal_actions = {}
        if player == 1:
            pieces = self.pieces["w_pieces"]
        else:
            pieces = self.pieces["b_pieces"]
        for key in pieces:
            actions = self.get_legal_actions_piece(pieces[key])
            if len(actions) > 0:
                if pieces[key] not in legal_actions:
                    legal_actions[pieces[key]] = []
                
                legal_actions[pieces[key]].extend(actions)

        return legal_actions
    
    def execute_action(self, action):
        '''
        Executes an action on the board
        '''
        cur_piece = action[0]
        action = action[1]

        cur_pos = cur_piece.pos

        if isinstance(cur_piece, piece.King):
            # Handles case when action is to castle
            if action == (0,2) or action == (0,-2):
                if cur_piece.player == 1:
                    pieces = self.pieces["w_pieces"]
                    if action == (0,2):
                        if "w_R_r" in pieces:
                            rook = pieces["w_R_r"]
                            new_rook_pos = (cur_pos[0], cur_pos[1]+1)
                        else:
                            return
                    
                    if action == (0,-2):
                        if "w_R_l" in pieces:
                            rook = pieces["w_R_l"]
                            new_rook_pos = (cur_pos[0], cur_pos[1]-1)
                        else:
                            return
                else:
                    pieces = self.pieces["b_pieces"]
                    if action == (0,2):
                        if "b_R_r" in pieces:
                            rook = self.pieces["b_pieces"]["b_R_r"]
                            new_rook_pos = (cur_pos[0], cur_pos[1]+1)
                        else:
                            return
                    
                    if action == (0,-2):
                        if "b_R_l" in pieces:
                            rook = self.pieces["b_pieces"]["b_R_l"]
                            new_rook_pos = (cur_pos[0], cur_pos[1]-1)
                        else:
                            return

                new_king_pos = (cur_pos[0]+action[0], cur_pos[1]+action[1])
                cur_piece.pos = new_king_pos
                rook.pos = new_rook_pos
                cur_piece.has_moved = True
                rook.has_moved = True

                self.board[new_king_pos[0], new_king_pos[1]] = cur_piece
                self.board[new_rook_pos[0], new_rook_pos[1]] = rook

                return
        
        # All other types of actions, excluding castling
        if isinstance(cur_piece, piece.Rook):
            cur_piece.has_moved = True

        if isinstance(cur_piece, piece.Pawn):
            if action == (-2,0):
                cur_piece.enpassant = True
            else:
                cur_piece.enpassant = False

        new_pos = (cur_pos[0] + action[0], cur_pos[1] + action[1])
        other_piece = self.board[new_pos[0], new_pos[1]]
        if other_piece != None:
            if other_piece.player == 1:
                pieces = self.pieces["w_pieces"]
            else:
                pieces = self.pieces["b_pieces"]
            
            for key in list(pieces):
                if pieces[key] == other_piece:
                    pieces.pop(key, None)

        self.board[new_pos[0], new_pos[1]] = cur_piece
        self.board[cur_pos[0], cur_pos[1]] = None
        cur_piece.pos = new_pos
    
    def switch_orientation(self):
        '''
        Switches the orientation of the board, so it is in the perspective of the person
        whose turn it is.
        '''
        all_pieces = self.pieces
        w_pieces = all_pieces["w_pieces"]
        b_pieces = all_pieces["b_pieces"]

        for key in w_pieces:
            cur_piece = w_pieces[key]
            cur_pos = cur_piece.pos

            #Switch piece from one side to the other
            new_pos = (self.n-1 - cur_pos[0], cur_pos[1])
            cur_piece.pos = new_pos

        for key in b_pieces:
            cur_piece = b_pieces[key]
            cur_pos = cur_piece.pos
    
            #switch piece from one side to the other
            new_pos = (self.n-1 - cur_pos[0], cur_pos[1])
            cur_piece.pos = new_pos

        self.board = initialize_board(all_pieces, self.n)

   
    def king_in_check(self, cur_player):
        '''
        Checks if the King is currently in check
        '''
        other_player = cur_player*-1
        if cur_player == 1:
            pieces = self.pieces["w_pieces"]
            if "w_K" in pieces:
                cur_piece = pieces["w_K"]
            else:
                #print("White King is not on the board")
                return False
        else:
            pieces = self.pieces["b_pieces"]
            if "b_K" in pieces:
                cur_piece = pieces["b_K"]
            else:
                #print("Black King is not on the board")
                return False

        if not isinstance(cur_piece, piece.King):
            print("Error, piece is not a King")
            return

        king_pos = cur_piece.pos
        attacked_pos = self.get_all_attacked_positions(other_player)
        if king_pos in attacked_pos:
            return True
        
        return False

    def king_in_checkmate(self, cur_player):
        if not self.king_in_check(cur_player):
            return False
        
        if cur_player == 1:
            king = self.pieces["w_pieces"]["w_K"]
        else:
            king = self.pieces["b_pieces"]["b_K"]
       
        actions = self.get_legal_actions(cur_player)
        if len(actions) == 0:
            return True
        else:
            return False

    def stalemate(self, cur_player):
        '''
        Checks if the game is in stalemate
        '''
        w_pieces = self.pieces["w_pieces"]
        b_pieces = self.pieces["b_pieces"]
        
        w_draw = False
        b_draw = False
        if len(w_pieces) <= 2 and len(b_pieces) <= 2:
            if len(w_pieces) == 1:
                w_draw = True
            
            if len(b_pieces) == 1:
                b_draw = True

            for key in w_pieces:
                if isinstance(w_pieces[key], piece.Knight) or isinstance(w_pieces[key], piece.Bishop):
                    w_draw = True
            
            for key in b_pieces:
                if isinstance(b_pieces[key], piece.Knight) or isinstance(b_pieces[key], piece.Bishop):
                    b_draw = True
            
            if b_draw and w_draw:
                return True

        legal_actions = self.get_legal_actions(cur_player)
        if len(legal_actions) == 0:
            return True
        else:
            return False
    
    def promote_pawn(self):
        '''
        Promotes a pawn if there is a pawn in the last row or first row
        '''
        for i in range(self.n):
            if isinstance(self.board[self.n-1][i], piece.Pawn):
                cur_player = self.board[self.n-1][i].player
                knight = piece.Knight((self.n-1,i), cur_player)
                bishop = piece.Bishop((self.n-1,i), cur_player)
                rook = piece.Rook((self.n-1,i), cur_player)
                queen = piece.Queen((self.n-1,i), cur_player)

                return [knight, bishop, rook, queen]
            
            if isinstance(self.board[0][i], piece.Pawn):
                cur_player = self.board[0][i].player
                knight = piece.Knight((0,i), cur_player)
                bishop = piece.Bishop((0,i), cur_player)
                rook = piece.Rook((0,i), cur_player)
                queen = piece.Queen((0,i), cur_player)

                return [knight, bishop, rook, queen]
        
        return []
    
    def get_player_actions(self, player):
        '''
        Returns a list of all possible actions (not all actions are valid) for a specific player - will not
        return actions from pieces that have been captured.
        '''
        player_actions = {}
        if player == 1:
            pieces = self.pieces["w_pieces"]
        else:
            pieces = self.pieces["b_pieces"]
        
        
        for key in pieces:
            cur_piece = pieces[key]
            if cur_piece not in player_actions:
                player_actions[cur_piece] = []

            for action in pieces[key].actions:
                for speed in pieces[key].speed:
                    player_actions[cur_piece].append((action[0] * speed, action[1] * speed))
        
        return player_actions

    
    def get_all_actions(self):
        '''
        Returns a list of all possible actions (not all actions are valid) - will not return actions
        from all pieces if some pieces have been captured. 
        '''

        white_player_actions = self.get_player_actions(1)
        black_player_actions = self.get_player_actions(-1)

        all_actions = {**white_player_actions, **black_player_actions}

        return all_actions
