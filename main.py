import randomPlay
import numpy as np

from enum import Enum

class TileType(Enum):
	OBSTACLE = -1
	EMPTY = 0
        
def main(max_x, max_y, target, n_move):

    test_map = -np.ones((MAX_X, MAX_Y, len(TileType)), dtype=int)
    test_map[1:-1, 1:-1] = 0

    test = randomPlay.Map(max_x, max_y, target, n_move, test_map)
    is_clear = test.play(test_map)
    print(is_clear)

############### MAIN ################

MAX_X = 7
MAX_Y = 7
TARGET = 15
N_MOVE = 40

if __name__ == '__main__':
    main(MAX_X, MAX_Y, TARGET, N_MOVE)

