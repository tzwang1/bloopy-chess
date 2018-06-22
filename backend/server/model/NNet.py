import argparse

import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.autograd import Variable

from .ChessNNet import ChessNNet as chessnnet

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),
    'num_channels': 512,
})

class NNet():
    def __init__(self, game):
        self.nnet = chessnnet(game, args)
        self.board_x, self.board_y = game.board.n, game.board.n
        self.all_actions = game.board.get_all_actions()
        self.action_size = len(self.all_actions)

        if args.cuda():
            self.nnet.cuda()
    
    def train(self, examples):
        optimizer = optim.Adam(self.nnet.parameters())

        for epoch in range(args.epochs):