import numpy as np
from abc import abstractmethod
import matplotlib.pyplot as plt

class GridWorld():

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

        newState = self.transitionTable[state][action]
        reward = self.rewards[newState]

        return newState, reward


