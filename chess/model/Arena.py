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

        game = Game(10, 8)
        while not game.get_game_ended():
            it+=1
            if verbose:
                assert(self.display)
                print("Turn ", str(it), "Player ", str(game.cur_player))
                #self.display(board)
            action_index = players[curPlayer+1](game.convert_to_nums())

            legal_actions = game.board.get_legal_actions(game.cur_player)

            # if legal_actions[action_index] == 0:
            #     print(action)
            #     assert legal_actions[action] > 0
            
            game.get_next_state(game.cur_player, legal_actions[action_index])

        if verbose:
            assert(self.display)
            print("Game over: Turn ", str(it), "Result ", str(game.get_game_ended()))
            # self.display(board)
        return game.get_game_ended() #TODO change to return 1/-1/0 instead of True/False
    
    def playGames(self, num, verbose=False):
        """
        Plays num games in which player1 starts num/2 games and player2 starts
        num/2 games.
        Returns:
            oneWon: games won by player1
            twoWon: games won by player2
            draws:  games won by nobody
        """
        # eps_time = AverageMeter()
        # bar = Bar('Arena.playGames', max=num)
        # end = time.time()
        eps = 0
        maxeps = int(num)

        num = int(num/2)
        oneWon = 0
        twoWon = 0
        draws = 0
        for _ in range(num):
            gameResult = self.playGame(verbose=verbose)
            if gameResult==1:
                oneWon+=1
            elif gameResult==-1:
                twoWon+=1
            else:
                draws+=1

            # bookkeeping +  TODO: plot progress
            eps += 1

        self.player1, self.player2 = self.player2, self.player1
        
        for _ in range(num):
            gameResult = self.playGame(verbose=verbose)
            if gameResult==-1:
                oneWon+=1                
            elif gameResult==1:
                twoWon+=1
            else:
                draws+=1
            # bookkeeping + TODO: plot progress
            eps += 1
        
        return oneWon, twoWon, draws
    