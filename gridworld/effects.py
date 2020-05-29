from abc import ABC, abstractmethod

class Effect(ABC):
	"""
	An abstract base class for defining effects.

	This class contains the abstract methods to be implemented for 
	an effect to be applied to the simple grid-world object via 
	Variational World module.
	"""

	def __init__(self, world, preEffect=False):
		self.world = world
		self.preEffect = preEffect
		
	def __call__(self, state, action, reward, buff):
		return self.effect(state, action, reward, buff)

	@abstractmethod
	def effect(self, state, action, reward, buff):
		pass

def __getPenalty__(penalty, state):

	a = {}
	if type(penalty) == type(a):
		return penalty[state]
	else:
		return penalty


def __getState__(jumpStates, state):
	try:
		newState = jumpStates[state]
	except:
		newState = state

	return newState



class JumpEffect(Effect):
	"""
	This changes the state of the agent when certain defined states are reached.

	We define jump states to be a dictionary {S_t : S_d} of target (S_t) and 
	destination states (S_d). When an agent reaches a target state S_t present in the
	dictionary the state of the agent is changed to the destination state S_d. 

	If there is a penalty associated with these states then it is applied and returned as
	the reward rather than the reward recieved during the transition. Else the reward 
	recieved during the transition is returned.

	Parameters
		
		world : A world object on whose transitions the post effects will act on.
		
		jumpStates (dictionary): A Dictionary containing target state and their associated destination state.

		penalty (dictionary or float) : if dictionary for every target state present in 
		jumpStates an associated reward needs to be mentioned. If it is a float then for 
		all states the same penalty is applied.

	Example 
		>>> rewards = {0:0, 2:-3, 5:-3, 6:-3, 9:-2, 12:-2}
		>>> jumpStates = { 2:0, 4:0, 11:13 }
		>>> w = GridWorld((4, 4), rewards=rewards, defaultReward=-1)
		>>> je = JumpEffect(w, jumpStates=jumpStates)
		>>> vw = VariationalWorld(w, postEffect=je)
		>>> print(vw(10,1))
		(13, -1)
	"""

	def __init__(self, world, jumpStates, penalty=None):
		super().__init__(world=world, preEffect=False)
		self.jumpStates = jumpStates
		self.penalty = penalty

	def effect(self, state, action, reward, buff):
		newState, newReward = self.world(state, action)
		newReward = reward

		st = __getState__(self.jumpStates, newState)

		if st != newState:
			newState = st
			if self.penalty is not None:
				newReward = __getPenalty__(self.penalty, newState)
			else:
				newReward = reward

		return newState, action, newReward


class BlockEffect(Effect):
	"""
	This blocks certain states and prevents the agent from entering them.

	We define block states to be a list of states [S_t].
	When an agent reaches a target state S_t via the transition function the 
	states are reset to the former state from which the target state was reached i.e. if
	> S <- transition(S_0, A)
	> S_t <- S if S not in blockStates else S_0

	If there is a penalty associated with these states then it is applied and returned as
	the reward rather than the reward recieved during the transition. Else the reward 
	recieved during the transition is returned.

	Parameters
		
		world : A world object on whose transitions the post effects will act on.
		
		blockStates (list): A list of forbidden states reaching which the state of the 
		agent is reset to the previous state.

		penalty (dictionary or float) : if dictionary, for every target state present in 
		blockStates an associated reward needs to be mentioned. If it is a float then for 
		all states the same penalty is applied.

	Example 
		>>> rewards = {0:0, 2:-3, 5:-3, 6:-3, 9:-2, 12:-2}
		>>> blockStates = [2, 4, 11]
		>>> w = GridWorld((4, 4), rewards=rewards, defaultReward=-1)
		>>> be = blockEffect(w, blockStates=blockStates)
		>>> vw = VariationalWorld(w, postEffect=be)
		>>> print(vw(10,1))
		(10, -1)
	"""

	def __init__(self, world, blockStates, penalty=None):
		super().__init__(world=world, preEffect=False)
		self.blockStates = blockStates
		self.penalty = penalty

	def effect(self, state, action, reward, buff):

		newState, newReward = self.world(state, action)
		newReward = reward
		if newState in self.blockStates:
			newState = state

			if self.penalty is not None:
				newReward = __getPenalty__(self.penalty, newState)
			else:
				newReward = reward

		return newState, action, newReward


class EdgeEffect(Effect):
	"""
	Penalizing an agent hitting the edges og the 2D grid-world.

	When an agent takes an action that results in returning to the same state 
	he was previously in a penalty is applied.

	Warning
		This is not exactly penalizing the agent for hitting the 2D grid-world's
		edges but also the when they hit block states or have effects that make the 
		agent return to the same state that it started taking the action in.

	Parameters
		
		world : A world object on whose transitions the post effects will act on.
		
		penalty (float) : for all Edge states that are reached by the transition the
		penalty is applied.

	Example 
		>>> rewards = {0:0, 2:-3, 5:-3, 6:-3, 9:-2, 12:-2}
		>>> w = GridWorld((4, 4), rewards=rewards, defaultReward=-1)
		>>> ee = blockEffect(w, penalty=-10)
		>>> vw = VariationalWorld(w, postEffect=ee)
		>>> print(vw(11,1))
		(11, -10)
		>>> print(vw(10,1))
		(11, -1)
	"""

	def __init__(self, world, penalty):
		super().__init__(world=world, preEffect=False)
		self.penalty = penalty

	def effect(self, state, action, reward, buff):

		newState, newReward = self.world(state, action)
		if newState == state:
			newReward = __getPenalty__(self.penalty, newState)

		return state, action, newReward
