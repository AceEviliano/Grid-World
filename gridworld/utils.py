#other helpers here
import numpy as np

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


def test_getEpisode():

    w = World((3, 2), reward, default_reward)
    
    st, ac, re = w.getEpisode(0, 5, policy)
    results = np.stack((st,ac,re), axis=0)

    x = np.load(inp_path+'GWgetEpisode32.npy')

    assert np.sum( results - x ) == 0

def test_getEpisode2():
    
    w = World(3, 2, reward, default_reward)

    st, ac, re = w.getEpisode(0, 1, policy)
    results = np.stack((st,ac,re), axis=0)


