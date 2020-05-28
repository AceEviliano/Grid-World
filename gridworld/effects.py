from abc import ABC, abstractmethod

class Effect(ABC):

	def __init__(self, world, preEffect=False):
		self.world = world
		self.preEffect = preEffect
		
	def __call__(self, state, action, reward, buff):
		return self.effect(state, action, reward, buff)

	@abstractmethod
	def effect(self, state, action, reward, buff):
		pass


class JumpEffect(Effect):

	def __init__(self, world, jumpStates):
		super().__init__(world=world, preEffect=False)
		self.jumpStates = jumpStates

	def __getState__(self, state):
		try:
			newState = self.jumpStates[state]
		except:
			newState = state

		return newState

	def effect(self, state, action, reward, buff):
		newState, _ = self.world(state, action)
		return self.__getState__(newState), action, reward


class BlockEffect(Effect):

	def __init__(self, world, blockStates):
		super().__init__(world=world, preEffect=False)
		self.blockStates = blockStates

	def effect(self, state, action, reward, buff):
		newState, newReward = self.world(state, action)
		if newState in self.blockStates:
			newState = state

		return newState, action, reward


class EdgeEffect(Effect):

	def __init__(self, world, penalty):
		super().__init__(world=world, preEffect=False)
		self.penalty = penalty

	def effect(self, state, action, reward, buff):
		newState, newReward = self.world(state, action)
		if newState == state:
			newReward = self.penalty

		return state, action, newReward
