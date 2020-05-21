import numpy as np
from ..World import GridWorld as World

inp_path = 'gridworld/test/inp/'

reward = {2:-3, 4:-2, 5:-2}
default_reward = -1

def policy(state):
	policy = np.array([3,0,1,3,2,2])
	return policy[state]


def test_init():

	w = World(3, 3, reward, default_reward)
	test_w = np.load(inp_path+'GW33.npy')
	assert np.sum( w.transitionTable - test_w ) == 0

	w = World(3, 2, reward, default_reward)
	test_w = np.load(inp_path+'GW32.npy')
	assert np.sum( w.transitionTable - test_w ) == 0

	w = World(2, 3, reward, default_reward)
	test_w = np.load(inp_path+'GW32.npy')
	assert np.sum( w.transitionTable - test_w ) == 0

	w = World(3, 2, reward, default_reward)
	x = np.load(inp_path+'GWrewards32.npy')
	assert np.sum( w.rewards - x ) == 0

def test_getEpisode():

	w = World(3, 2, reward, default_reward)
	
	st, ac, re = w.getEpisode(0, 5, policy)
	results = np.stack((st,ac,re), axis=0)

	x = np.load(inp_path+'GWgetEpisode32.npy')

	assert np.sum( results - x ) == 0

def test_getEpisode2():
	
	w = World(3, 2, reward, default_reward)

	st, ac, re = w.getEpisode(0, 1, policy)
	results = np.stack((st,ac,re), axis=0)


def test_transition():

	w = World(3, 2, reward, default_reward)
	
	a, r = w.transition(0, 0)
	assert a == 0
	a, r = w.transition(3, 3)
	assert a == 5
	a, r = w.transition(4, 2)
	assert a == 2
	a, r = w.transition(2, 1)
	assert a == 3




if __name__ == "__main__":


	print('test for World')
	
