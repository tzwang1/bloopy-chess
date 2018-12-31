import numpy as np
import math
EPS = 1e-8

class MCTS(object):
    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.args = args
        self.Qsa = {}       # stores Q values for s,a (as defined in the paper)
        self.Nsa = {}       # stores #times edge s,a was visited
        self.Ns = {}        # stores #times board s was visited
        self.Ps = {}        # stores initial policy (returned by neural net)

        self.Es = {}        # stores game.get_game_ended ended for board s
        self.Vs = {}        # stores game.board.get_legal_actions for board s

        self.white_actions = game.board.get_player_actions(1)
        self.black_actions = game.board.get_player_actions(-1)
        
        self.action_size = len(self.white_actions)
    
    def get_action_prob(self, game, temp=1):
        """
        This function performs numMCTSSims simulations of MCTS starting from the current state in
        game.
        Returns:
            probs: a policy vector where the probability of the ith action is
                   proportional to Nsa[(s,a)]**(1./temp)
        """
        for i in range(self.args.num_MCTS_sims):
            self.search(game)
        
        # s = self.game.stringRepresentation(canonicalBoard)
        s = str(game.convert_to_nums())
        counts = [self.Nsa[(s,a)] if (s,a) in self.Nsa else 0 for a in range(self.action_size)]

        if temp==0:
            bestA = np.argmax(counts)
            probs = [0]*len(counts)
            probs[bestA]=1
            return probs

        counts = [x**(1./temp) for x in counts]
        probs = [x/float(sum(counts)) for x in counts]
        return probs
    
    def search(self, game):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. While searching it updates Qsa, Nsa, Ns, and Ps.
        
        The action chosen at each node is one that has the maximum 
        upper confidence bound as in the paper.

        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propogated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propogated up the search path. The values of Ns, Nsa, Qsa are
        updated.

        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.
        Returns:
            v: the negative of the value of the current canonicalBoard
        """

        s = str(game.convert_to_nums()) # converts the numerical representation of a board state to a string

        if s not in self.Es:
            self.Es[s] = self.game.get_game_ended()
        if self.Es[s]!=0:
            # terminal node
            return -self.Es[s]

        if s not in self.Ps:
            # leaf node
            self.Ps[s], v = self.nnet.predict(game.convert_to_nums())
            legal_actions = game.board.get_legal_actions(game.cur_player) #TODO: verify if this method of getting valid moves is correct
            valids = []

            if game.cur_player == 1:
                all_actions = self.white_actions
            else:
                all_actions = self.black_actions

            for piece in all_actions:
                if piece not in legal_actions:
                    continue
                
                # import pdb; pdb.set_trace()
                for action in all_actions[piece]:
                    if action in legal_actions[piece]:
                        valids.append(1)
                    else:
                        valids.append(0)

            import pdb; pdb.set_trace()
            self.Ps[s] = self.Ps[s]*valids      # masking invalid moves
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s    # renormalize
            else:
                # if all valid moves were masked make all valid moves equally probable
                
                # NB! All valid moves may be masked if either your NNet architecture is insufficient or you've get overfitting or something else.
                # If you have got dozens or hundreds of these messages you should pay attention to your NNet and/or training process.   
                print("All valid moves were masked, do workaround.")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        # pick the action with the highest upper confidence bound
        for a in range(self.action_size):
            if valids[a]:
                if (s,a) in self.Qsa:
                    u = self.Qsa[(s,a)] + self.args.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                else:
                    u = self.args.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s] + EPS)     # Q = 0 ?

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        # next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
        import pdb; pdb.set_trace()
        game.get_next_state(game.cur_player, a)
        # next_s = self.game.getCanonicalForm(next_s, next_player)

        # v = self.search(next_s)
        v = self.search(game)

        if (s,a) in self.Qsa:
            self.Qsa[(s,a)] = (self.Nsa[(s,a)]*self.Qsa[(s,a)] + v)/(self.Nsa[(s,a)]+1)
            self.Nsa[(s,a)] += 1

        else:
            self.Qsa[(s,a)] = v
            self.Nsa[(s,a)] = 1

        self.Ns[s] += 1
        return -v

