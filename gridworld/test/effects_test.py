import os.path as path
import numpy as np
from ..world import GridWorld as GW
from ..variationalWorld import VariationalWorld as VW
from ..effects import JumpEffect, BlockEffect

inp_path = path.abspath('./gridworld/test/inp')

def test_jumpEffect():

	rewards = {0:0, 2:-3, 5:-3, 6:-3, 9:-2, 12:-2}
	jumpStates = { 2:0, 4:0, 11:13 }

	w = GW((4, 4), rewards=rewards, defaultReward=-1)
	je = JumpEffect(w, jumpStates=jumpStates)
	vw = VW(w, postEffect=je)

	transitionTable = []
	for st in  w.states :
		
		stateTable = []
		for act in w.actions :
			s, r = vw(st, act)
			stateTable.append(s)

		transitionTable.append(stateTable)

	table = np.load( path.join(inp_path, 'JE44.npy') )
	transitionTable = np.array(transitionTable)

	assert np.sum(transitionTable - table ) == 0

	return


def test_blockEffect():
	
	rewards = {0:0, 2:-3, 5:-3, 6:-3, 9:-2, 12:-2}
	blockStates = [4, 2, 11]

	w = GW((4, 4), rewards=rewards, defaultReward=-1)
	be = BlockEffect(w, blockStates=blockStates)
	vw = VW(w, postEffect=be)

	transitionTable = []
	for st in  w.states :
		
		stateTable = []
		for act in w.actions :
			s, r = vw(st, act)
			stateTable.append(s)

		transitionTable.append(stateTable)

	transitionTable = np.array(transitionTable)
	test = np.load( path.join(inp_path,'BE44.npy') )

	assert np.sum(test - transitionTable) == 0

	return


def test_edgeEffect():
	
	pass


if __name__ == '__main__':
	pass