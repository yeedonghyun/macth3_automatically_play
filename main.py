from Map import Map
import numpy as np

def main(max_x, max_y, n_target, target_type, n_block_type, n_move, board, debug_mode):    
    test = Map(max_x, max_y, n_target, target_type, n_block_type, n_move, board, debug_mode)
    is_clear = test.play()
    print(is_clear)

############### MAIN ################

MAX_X = 8
MAX_Y = 7
N_TARGET = 15
N_BLOCK_TYPE = 5
TARGET_TYPE = Map.CellType.APPLE
N_MOVE = 30
DEBUG_MODE = Map.DebugMode.RESULT

board = np.full((MAX_Y, MAX_X), Map.CellType.OBSTACLE)
board[1:-1, 1:-1] = Map.CellType.EMPTY
board[0][4] = Map.CellType.EMPTY
board[3][4] = Map.CellType.OBSTACLE
board[3][3] = Map.CellType.OBSTACLE
board[3][5] = Map.CellType.OBSTACLE

if __name__ == '__main__':
    main(MAX_X, MAX_Y, N_TARGET, TARGET_TYPE, N_BLOCK_TYPE, N_MOVE, board, DEBUG_MODE)