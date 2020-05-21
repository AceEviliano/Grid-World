import numpy as np
import matplotlib.pyplot as plt

class GridWorld():

    def __init__(self, row=4, col=4, rewards={},
                 defaultReward=0, transitionTable=None):

        self.row = row
        self.col = col
        self.dim = (row, col)
        self.defaultReward = defaultReward

        self.actions = range(4)
        self.states = range(row * col)
        self.rewards = self.__setRewards__(rewards)
        self.transitionTable = transitionTable if transitionTable is not None else self.__setTransitions__()
        
        return

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

        #print(f"oldstate : {state},  action : {action},  newstate : {new_state}")

        return new_state

    def transition(self, state, action):

        new_state = self.transitionTable[state][action]
        return new_state, self.rewards[new_state]

    def getEpisode(self, startState, termState, policy):

        states = []
        actions = []
        rewards = []
        newState = startState
        inx = 0

        while newState != termState:
            
            action = policy(newState)
            newState, reward = self.transition(newState, action)

            assert newState not in states, 'Termination not possible, Cyclic policy'

            states.append(newState)
            actions.append(action)
            rewards.append(reward)

        return states, actions, rewards
