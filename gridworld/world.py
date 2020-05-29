import numpy as np

class GridWorld():
    """
    A 2D classic grid-world.

    The classic grid-world where the agent has 4 actions at every given state:
    0:left, 1:right 2:up & 3:down. The dimensions dim=(row,col) defines the dimensions
    of this grid-world. There are row*col number of states in this world indexed in 
    row-major order from 0, ..., row*col-1. The transition function for this world
    takes in a (state, action) pair to return (new_state, reward).

    Parameters
        dim (tuple): a tuple (row, col) indincating the dimensions of the grid world.

        rewards (dictionary): a dictionary of states and their associated rewards when
        they are reached via a transition.

        defaultReward (float): for all the states not present in the rewards dictionary
        a default reward can be set.

        transitionTable (optional, numpy array): a numpy array containing transitions for 
        each state action pair.

    Example
        >>> rewards = {0:0, 2:-3, 5:-3, 6:-3, 9:-2, 12:-2}
        >>> w = GridWorld((4, 4), rewards=rewards, defaultReward=-1)
        >>> print(w(0,3))  # 0,3 represents the state action pair of (state=0, action='down')
        (4,-1)             # the reward here is -1 as it is the default reward
        >>> print(w(4,1))  # 4,1 represents the state action pair of (state=4, action='left')
        (5,-3)             # the reward here is -3 since there is a non-default reward associated with this state
    """

    def __init__(self, dim=(4, 4), rewards={},
                 defaultReward=0, transitionTable=None):

        self.dim = dim
        self.row, self.col = dim
        self.defaultReward = defaultReward

        self.actions = range(4)
        self.states = range(self.row * self.col)
        self.rewards = self.__setRewards__(rewards)
        self.transitionTable = transitionTable if transitionTable is not None else self.__setTransitions__()
        
        return

    def __call__(self, state, action):
        return self.transition(state, action)

    def __setRewards__(self, rewards):

        rewardTable = []

        for state in self.states:       
            try:
                r = rewards[state]
            except:
                r = self.defaultReward

            rewardTable.append(r)

        return np.array(rewardTable)

    def __setTransitions__(self):

        transitionTable = []
        for state in self.states:
            stateTransitions = [ self.__transitionFunction__(state, action) for action in self.actions ]
            transitionTable.append(stateTransitions)

        return np.array(transitionTable)

    def __transitionFunction__(self, state, action):

        row, col = self.dim
        
        if action == 0:
            action = 'left'
            new_state = state - 1
            if new_state // col != state // col:
                new_state = state

        elif action == 1:
            action = 'right'
            new_state = state + 1
            if new_state // col != state // col:
                new_state = state

        # when up or down action is taken
        # the states are a row (number) away from
        # each other in enumeration

        if action == 2:
            action = 'up'
            new_state = state - col
            if new_state < 0 or new_state >= row * col:
                new_state = state

        elif action == 3:
            action = 'down'
            new_state = state + col
            if new_state < 0 or new_state >= row * col:
                new_state = state

        return new_state

    def transition(self, state, action):
        """
        A transition function for the 2D classic grid-world.

        Takes in (state, action) pair to return (new_state, reward).

        Parameters
            state (int): A integer representing the state.

            action (int): An integer representing one of the actions.

        Returns
            state (int): A new state that the agent has transitioned into.

            reward (float): reward for having enterd the new_state.
        """

        newState = self.transitionTable[state][action]
        reward = self.rewards[newState]

        return newState, reward


