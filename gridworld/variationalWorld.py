class VariationalWorld():
	"""
	A framework to apply effects to the world object.

	Variational World takes in a world and applies pre-transition &
	post-transition effects on state action and reward. If these are left
	unmentioned it is same as the world object.

	Example
		>>> rewards = {0:0, 2:-3, 5:-3, 6:-3, 9:-2, 12:-2}
		>>> w = GridWorld((4, 4), rewards=rewards, defaultReward=-1)
		>>> eff = SomeEffect(w, *kwargs)
		>>> vw = VariationalWorld(w, postEffect=eff)
		>>> vw(state, action)
	"""

	def __init__(self, world, postEffect=None, preEffect=None):

		self.world = world
		self.preEffect = preEffect
		self.postEffect = postEffect

		self.__stateBuffer__ = self.__actionBuffer__ = self.__rewardBuffer__ = None
		self.buff = (self.__stateBuffer__, self.__actionBuffer__, self.__rewardBuffer__)

	def __call__(self, state, action, prevReward=None):
		return self.transition(state, action, prevReward)

	def __str__(self):

		s = str(self.world)
		return s

	def __applyPreEffects__(self, state, action, reward, buff):

		if self.preEffect is not None :
			self.__stateBuffer__, self.__actionBuffer__, self.__rewardBuffer__ = \
				self.preEffect(state, action, reward, buff)
		else :
			self.__stateBuffer__, self.__actionBuffer__, self.__rewardBuffer__ = \
				state, action, reward

		return self.__stateBuffer__, self.__actionBuffer__

	def __applyPostEffects__(self, state, action, reward, buff):

		if self.postEffect is not None :
			self.__stateBuffer__, self.__actionBuffer__, self.__rewardBuffer__ = \
				self.postEffect(state, action, reward, buff)
		else :
			state, reward = self.world(state, action)
			self.__stateBuffer__, self.__actionBuffer__, self.__rewardBuffer__ = \
				state, action, reward

		return self.__stateBuffer__, self.__rewardBuffer__

	def getBuffer(self):
		"""
		Returns the buffer before or after the transition.

		Returns
			state, action, reward
		"""
		return self.buff

	def setBuffer(self, state, action, reward):
		"""
		Sets the buffer before or after the transition.

		Parameters
			state, action, reward
		"""
		self.__stateBuffer__, self.__actionBuffer__, self.__rewardBuffer__ = state, action, reward


	def addEffects(self, preEffect=None, postEffect=None):

		self.preEffect = preEffect
		self.postEffect = postEffect

	def transition(self, state, action, prevReward=None):
		"""
		Performs transition in the variation of the world.

		Parameters
			state : state of an agent.

			action : action that the agent takes int that state

			preReward (optional): takes in the reward of the previous time step, can be used 
			for transition effects.
		"""

		# print(f'in variational transition-  s:{state}  a:{action}  r:{prevReward}')
		state, action = self.__applyPreEffects__(state, action, prevReward, self.buff)
		# print(f'preEffect out-  s:{state}  a:{action}  r:{prevReward}')

		newState, reward = self.world.transition(state, action)
		# print(f'transition out-  s:{newState}  a:{action}  r:{reward}')

		newState, newReward = self.__applyPostEffects__(state, action, reward, self.buff)
		# print(f'postEffect out-  s:{newState}  a:{action}  r:{newReward}')

		return newState, newReward