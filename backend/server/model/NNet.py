import argparse
import numpy as np

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
            print('EPOCH ::: ' + str(epoch+1))
            self.nnet.train() # Switch nnet into training mode

            batch_idx = 0
            while batch_idx < int(len(examples) / args.batch_size):
                sample_ids = np.random.randint(len(examples), size=args.batch_size)
                boards, pis, vs = list(zip(*examples[i] for i in sample_ids))
                boards = torch.FloatTensor(np.array(boards).astype(np.float64))
                target_pis = torch.FloatTensor(np.array(pis))
                target_vs = torch.FloatTensor(np.array(vs).astype(np.float64))

                # predict
                if args.cuda:
                    boards, target_pis, target_vs = boards.contiguous().cuda(), target_pis.contiguous().cuda(), target_vs.contiguous().cuda()
                boards, target_pis, target_vs = Variable(boards), Variable(target_pis), Variable(target_vs)

                out_pi, out_v = self.nnet(boards)
                l_pi = self.loss_pi(target_pis, out_pi)
                l_v = self.loss_v(target_vs, out_v)
                total_loss = l_pi + l_v # Note the original paper uses a different loss function (may want to try that, if this one doesn't work well)
                
                # compute gradient and do SGD step
                optimizer.zero_grad()
                total_loss.backward()
                optimizer.step()

                batch_idx+=1

                # TODO: Plot graph of training data/progress

def predict(self, board):
    board = torch.FloatTensor(board.astype(np.float64))
    if args.cuda: 
        board = board.contiguous().cuda()
    
    board = Variable(board, volatile=True)
    board = board.view(1, self.board_x, self.board_y)

    self.nnet.eval() # Switch neural net to evaluation mode
    pi, v = self.nnet(board)

    return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]


def loss_pi(self, targets, outputs)
    return -torch.sum(targets * outputs)/targets.size()[0]

def loss_v(self, targets, outputs)
    return torch.sum((targets - outputs.view(-1))**2)/targets.size()[0]


