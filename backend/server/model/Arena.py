import sys
sys.path.append("..")
import chess.ChessGame as Game
import numpy as np

class Arena():
    """
    An Arena class where any 2 agents can be pit against each other.
    """
    def __init__(self, player1, player2, game, display=None):
        """
        Input:
            player 1,2: two functions that takes board as input, return action
            game: Game object
            display: a function that takes board as input and prints it (e.g.
                     display in othello/OthelloGame). Is necessary for verbose
                     mode.
        see othello/OthelloPlayers.py for an example. See pit.py for pitting
        human players/other baselines with each other.
        """
        self.player1 = player1
        self.player2 = player2
        self.game = game
        self.display = display

     def playGame(self, verbose=False):
        """
        Executes one episode of a game.
        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player2, None, self.player1]
        
        it = 0
        while not self.game.get_game_ended():
            it+=1
            if verbose:
                assert(self.display)
                print("Turn ", str(it), "Player ", str(game.cur_player))
                #self.display(board)
            action_index = players[curPlayer+1](self.game.convert_to_nums())

            legal_actions = self.game.board.get_legal_actions(game.cur_player)

            # if legal_actions[action_index] == 0:
            #     print(action)
            #     assert legal_actions[action] > 0
            
            self.game.get_next_state(game.cur_player, legal_actions[action_index])

        if verbose:
            assert(self.display)
            print("Game over: Turn ", str(it), "Result ", str(game.get_game_ended()))
            # self.display(board)
        return self.game.get_game_ended()