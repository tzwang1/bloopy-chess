import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from ChessGame import Game
from MCTS import MCTS
import numpy as np
from pickle import Pickler, Unpickler
from collections import deque


class Coach(object):
    def __init__(self, nnet, game, args):
        self.game = game
        self.nnet = nnet
        self.pnet = self.nnet.__class__(self.game) # competitor network
        self.args = args
        self.mcts = MCTS(self.game, self.nnet, self.args)
        self.train_example_history = [] # list containing args.num_iters_for_training_example_history latest training examples
        self.skip_first_play = False

    def execute_episode(self):
        """
        This function executes one episode of self-play, starting with player 1.
        As the game is played, each turn is added as a training example to
        train_examples. The game is played till the game ends. After the game
        ends, the outcome of the game is used to assign values to each example
        in train_examples.
        It uses a temp=1 if episodeStep < tempThreshold, and thereafter
        uses temp=0.
        Returns:
            train_examples: a list of examples of the form (board,pi,v)
                           pi is the MCTS informed policy vector, v is +1 if
                           the player eventually won the game, else -1.
        """
        train_examples = []
        game = Game(10, 8)
        # board = game.board.board # May need to instatiate a new game
        episode_step = 0

        while True:
            episode_step+=1
            board = game.convert_to_nums()
            temp = int(episode_step < self.args.temp_threshold)

            self.mcts = MCTS(game, self.nnet, self.args) 

            pi = self.mcts.get_action_prob(game, temp=temp)
            train_examples.append([board, game.cur_player, pi, None])
            
            action_index = np.random.choice(len(pi), p=pi) # Finding the action index with highest probability
            action = self.mcts.all_actions[action_index] 
            game.get_next_state(game.cur_player, action)

            if game.get_game_ended():
                r = 1
                if game.board.king_in_checkmate(game.cur_player):
                    r = -1
                elif game.board.stalemate(game.cur_player):
                    r = 0
            
                return [(x[0],x[2],r*((-1)**(x[1]!=game.cur_player))) for x in train_examples]

    def learn(self):
        """
        Performs numIters iterations with numEps episodes of self-play in each
        iteration. After every iteration, it retrains neural network with
        examples in train_examples (which has a maximium length of maxlenofQueue).
        It then pits the new neural network against the old one and accepts it
        only if it wins >= updateThreshold fraction of games.
        """

        for i in range(1, self.args.num_iters+1):
            # bookkeeping
            print('------ITER ' + str(i) + '------')
            # examples of the iteration
            if not self.skip_first_play or i>1:
                iterationTrainExamples = deque([], maxlen=self.args.max_len_queue)

                for eps in range(self.args.num_eps):
                    # game = Game(10, 8)
                    # self.mcts = MCTS(game, self.nnet, self.args)   # reset search tree
                    iterationTrainExamples += self.execute_episode()
            
                 # save the iteration examples to the history 
                self.train_example_history.append(iterationTrainExamples)

            if len(self.train_example_history) > self.args.num_iters_train_example_history:
                print("len(trainExamplesHistory) =", len(self.train_example_history), " => remove the oldest train_examples")
                self.train_example_history.pop(0)

            # backup history to a file
            # NB! the examples were collected using the model from the previous iteration, so (i-1)  
            self.saveTrainExamples(i-1)

            # shuffle examples before training
            train_examples = []
            for e in self.train_example_history:
                train_examples.extend(e)
            shuffle(train_examples)

            # training new network, keeping a copy of the old one
            self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            self.pnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            pmcts = MCTS(self.game, self.pnet, self.args)
            
            self.nnet.train(train_examples)
            nmcts = MCTS(self.game, self.nnet, self.args)

            print('PITTING AGAINST PREVIOUS VERSION')
            game = Game(10, 8)
            arena = Arena(lambda x: np.argmax(pmcts.get_action_prob(x, temp=0)),
                          lambda x: np.argmax(nmcts.get_action_prob(x, temp=0)), game)
            pwins, nwins, draws = arena.playGames(self.args.arena_compare)

            print('NEW/PREV WINS : %d / %d ; DRAWS : %d' % (nwins, pwins, draws))
            if pwins+nwins > 0 and float(nwins)/(pwins+nwins) < self.args.update_threshold:
                print('REJECTING NEW MODEL')
                self.nnet.load_checkpoint(folder=self.args.checkpoint, filename='temp.pth.tar')
            else:
                print('ACCEPTING NEW MODEL')
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename=self.get_checkpoint_file(i))
                self.nnet.save_checkpoint(folder=self.args.checkpoint, filename='best.pth.tar')           


    def get_checkpoint_file(self, iteration):
        return 'checkpoint_' + str(iteration) + '.pth.tar'

    def save_train_examples(self, iteration):
        folder = self.args.checkpoint
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = os.path.join(folder, self.get_checkpoint_file(iteration)+".examples")
        with open(filename, "wb+") as f:
            Pickler(f).dump(self.train_example_history)
        f.closed

    def load_train_examples(self):
        modelFile = os.path.join(self.args.load_folder_file[0], self.args.load_folder_file[1])
        examplesFile = modelFile+".examples"
        if not os.path.isfile(examplesFile):
            print(examplesFile)
            r = input("File with train_examples not found. Continue? [y|n]")
            if r != "y":
                sys.exit()
        else:
            print("File with train_examples found. Read it.")
            with open(examplesFile, "rb") as f:
                self.train_example_history = Unpickler(f).load()
            f.closed
            # examples based on the model were already collected (loaded)
            self.skipFirstSelfPlay = True