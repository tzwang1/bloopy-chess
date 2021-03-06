import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.autograd import Variable

class ChessNNet(nn.Module):
    def __init__(self, game, args):
        self.board_x, self.board_y = game.board.n, game.board.n
        self.args = args
        self.all_actions = game.board.get_all_actions()
        self.action_size = len(self.all_actions)

        super(ChessNNet, self).__init__()
        self.conv1 = nn.Conv2d(1, args.num_channels, args.kernel_size, stride=args.stride, padding=args.padding)
        self.conv2 = nn.Conv2d(args.num_channels, args.num_channels, args.kernel_size, stride=args.stride, padding=args.padding)
        self.conv3 = nn.Conv2d(args.num_channels, args.num_channels, args.kernel_size, stride=args.stride, padding=args.padding)
        self.conv4 = nn.Conv2d(args.num_channels, args.num_channels, args.kernel_size, stride=args.stride, padding=args.padding)

        self.bn1 = nn.BatchNorm2d(args.num_channels)
        self.bn2 = nn.BatchNorm2d(args.num_channels)
        self.bn3 = nn.BatchNorm2d(args.num_channels)
        self.bn4 = nn.BatchNorm2d(args.num_channels)

        self.fc1 = nn.Linear(self.args.num_channels*(self.board_x-4)*(self.board_y-4), 1024)
        self.fc_bn1 = nn.BatchNorm1d(1024)

        self.fc2 = nn.Linear(1024, 512)
        self.fc_bn2 = nn.BatchNorm1d(512)

        self.fc3 = nn.Linear(512, self.action_size)
        self.fc4 = nn.Linear(512, 1)

    def forward(self, x):
                                                           # s: batch_size x board_x x board_y
        x = x.view(-1, 1, self.board_x, self.board_y)                # batch_size x 1 x board_x x board_y
        x = F.relu(self.bn1(self.conv1(x)))                          # batch_size x num_channels x board_x x board_y
        x = F.relu(self.bn2(self.conv2(x)))                          # batch_size x num_channels x board_x x board_y
        x = F.relu(self.bn3(self.conv3(x)))                          # batch_size x num_channels x (board_x-2) x (board_y-2)
        x = F.relu(self.bn4(self.conv4(x)))                          # batch_size x num_channels x (board_x-4) x (board_y-4)
        x = x.view(-1, self.args.num_channels*(self.board_x-4)*(self.board_y-4))

        x = F.dropout(F.relu(self.fc_bn1(self.fc1(x))), p=self.args.dropout, training=self.training)  # batch_size x 1024
        x = F.dropout(F.relu(self.fc_bn2(self.fc2(x))), p=self.args.dropout, training=self.training)  # batch_size x 512

        pi = self.fc3(x)                                                                         # batch_size x action_size
        v = self.fc4(x)                                                                          # batch_size x 1

        return F.log_softmax(pi, dim=1), F.tanh(v)

