import numpy as np
import matplotlib.pyplot as plt

class GridWorld():

	def __init__(self, row=4, col=4, rewards={}, defaultReward=0, transitionTable=None):
		
		self.row = row
		self.col = col
		self.dim = (row,col)
		self.defaultReward=defaultReward

		self.states = range(row*col)
		self.rewards = setRewards(rewards)
		self.transitionTable = transitionTable if transitionTable not None else setTransitions()

	def setRewards(self, rewards):
		
		rewardTable = []

		for state in self.states :
			try :
				r = rewards[state]
			except :
				r = self.defaultReward

			rewardTable.append(r)

		return np.array(rewardTable)

	def setTransitions(self):
		
		transitionTable = []
		
		for state in self.states :
			stateTransitions = [ transition(state, action) for action in self.actions ]
			transitionTable.append(stateTransitions)

		return np.array(transitionTable)

	def transitionFunction(state, action):
    
		if action == 0 :
			new_state = state - 1
			if new_state//col != state//col :
				new_state = state
            
		elif action == 1 :
			new_state = state + 1
			if new_state//col != state//col :
				new_state = state
            
	   # when up or down action is taken
	   # the states are a row (number) away from
	   # each other in enumeration
    
		if action == 2:
			new_state = state - row
			if new_state < 0 or new_state > row*col:
				new_state = state

		elif action == 3:
			new_state = state + row   
		        if new_state < 0 or new_state >= row*col:
		            new_state = state
        
		return new_state	

	def transition(state, action):

		new_state = self.transitionTable[state][action]
		return new_state, self.rewards[new_state]

	def getEpisode(startState, termState, policy):

		states = []
		actions = []
		rewards = []

		while newState!=termState :

			action = policy(startState)
			newState, reward = transition(startState, action)
			states.append(newState)
			actions.append(action)
			rewards.append(reward)
			
		return states, actions, rewards
	
