from Map import Map
import numpy as np

def main(max_x, max_y, n_target, target_type, n_move, board):
    
    test = Map(max_x, max_y, n_target, target_type, n_move, board)
    is_clear = test.play()
    print(is_clear)

############### MAIN ################

MAX_X = 7
MAX_Y = 7
N_TARGET = 15
TARGET_TYPE = Map.CellType.APPLE
N_MOVE = 40

board = np.full((MAX_X, MAX_Y), Map.CellType.OBSTACLE)
board[1:-1, 1:-1] = Map.CellType.EMPTY

#board = np.array([
#    [   [-1, -1, -1, -1, -1, -1, -1],
#        [-1,  0,  0,  0,  0,  0, -1],
#        [-1,  0,  0,  0,  0,  0, -1],
#        [-1,  0,  0,  0,  0,  0, -1],
#        [-1,  0,  0,  0,  0,  0, -1],
#        [-1,  0,  0,  0,  0,  0, -1],
#        [-1, -1, -1, -1, -1, -1, -1]]
#])

if __name__ == '__main__':
    main(MAX_X, MAX_Y, N_TARGET, TARGET_TYPE, N_MOVE, board)

