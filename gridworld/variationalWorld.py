class VariationalWorld():

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
		return self.buff

	def setBuffer(self, state, action, reward):
		self.__stateBuffer__, self.__actionBuffer__, self.__rewardBuffer__ = state, action, reward


	def addEffects(self, preEffect=None, postEffect=None):

		self.preEffect = preEffect
		self.postEffect = postEffect

	def transition(self, state, action, prevReward=None):

		# print(f'in variational transition-  s:{state}  a:{action}  r:{prevReward}')
		state, action = self.__applyPreEffects__(state, action, prevReward, self.buff)
		# print(f'preEffect out-  s:{state}  a:{action}  r:{prevReward}')

		newState, reward = self.world.transition(state, action)
		# print(f'transition out-  s:{newState}  a:{action}  r:{reward}')

		newState, newReward = self.__applyPostEffects__(state, action, reward, self.buff)
		# print(f'postEffect out-  s:{newState}  a:{action}  r:{newReward}')

		return newState, newReward