import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import argparse
from Coach import Coach
import ChessGame
from NNet import NNetWrapper as nn

parser = argparse.ArgumentParser(description='RL Chess')
parser.add_argument('--numIters', type=int, default=1000,
                    help='number of iterations to train the data')
parser.add_argument('--numEps', type=int, default=100,
                    help='number of episodes to train the data')
parser.add_argument('--tempThreshold', type=int, default=15,
                    help='')
parser.add_argument('--updateThreshold', type=float, default=0.6,
                    help='')
parser.add_argument('--maxlenOfQueue', type=int, default='200000',
                    help='maximum number of samples to train on')
parser.add_argument('--numMCTSSims', type=int, default=25,
                    help='number of MCTS simulations to run')
parser.add_argument('--arenaCompare', type=int, default=40,
                    help='')
parser.add_argument('--cpuct', type=int, default=1,
                    help='number of CPUs to train on')
parser.add_argument('--checkpoint', type=str, default='./temp',
                    help='folder to save checkpoints in')
parser.add_argument('--load_model', type=bool,  default=False,
                    help='load the model or not')
parser.add_argument('--load_folder_file', type=str, default='',
                    help='')
parser.add_argument('--numItersForTrainExamplesHistory', type=int, default=20,
                    help='number of previous examples to save')

args = parser.parse_args()
# args = dict({
#     'numIters': 1000,
#     'numEps': 100,
#     'tempThreshold': 15,
#     'updateThreshold': 0.6,
#     'maxlenOfQueue': 200000,
#     'numMCTSSims': 25,
#     'arenaCompare': 40,
#     'cpuct': 1,

#     'checkpoint': './temp/',
#     'load_model': False,
#     'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
#     'numItersForTrainExamplesHistory': 20,

# })

if __name__=="__main__":
    game = ChessGame.Game(10, 8)
    nnet = nn(game)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(game, nnet, args)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()