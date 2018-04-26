import numpy as np
import ChessLogic as logic

class Game():
    def __init__(self, time, n):
        '''
        Initializes initial game state
        '''
        self.time = time
        self.board = logic.Board(n)
        self.cur_player = 1
    
    def getNextState(self, player, action):
        '''
        Get the next board state when action is taken by player.
        '''
        if player != self.cur_player:
            print("Incorrect player!")

    
