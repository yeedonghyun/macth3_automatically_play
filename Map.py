import random
import copy
import numpy as np

from matplotlib import pyplot
from matplotlib import pyplot as plt
from enum import Enum
from collections import namedtuple

class Map():
    class CellType(Enum):
        OBSTACLE = -1
        EMPTY = 0
        APPLE = 1
        BANANA = 2
        ORANGE = 3
        GRAPE = 4
        WATERMELON = 5
        STRAWBERRY = 6
        mango = 7
        pineapple = 8
        kiwi = 9

    class RenderingMode(Enum):
        PART = 0
        MOVE = 1
        RESULT = 2

    pos = namedtuple('pos', ['x', 'y'])

    diretion = {}
    diretion['up'] = pos(0, -1)
    diretion['down'] = pos(0, 1)
    diretion['left'] = pos(-1, 0)
    diretion['right'] = pos(1, 0)

    drop_diretion = {}
    drop_diretion['up'] = pos(0, -1)
    drop_diretion['left_up'] = pos(-1, -1)
    drop_diretion['right_up'] = pos(1, -1)
    drop_diretion['left'] = pos(-1, 0)
    #drop_diretion['right'] = pos(1, 0)

    def __init__(self, max_x, max_y, n_target, target_type, n_block_type, n_move, board, rendering_mode):
        self.ismatched = [[False for _ in range(max_x)] for _ in range(max_y)]
        self.matching_target = []
        self.matching_block = []
        self.empty_cell = []
        self.max_x = max_x
        self.max_y = max_y
        self.n_target = n_target
        self.target_type = target_type
        self.n_block_type = n_block_type
        self.n_move = n_move
        self.board = board
        self.destroy_target = 0
        self.peak = []
        self.cnt_move = 0
        self.rendering_mode = rendering_mode

    def play(self):
        assert self.isvalidation_from_board(), "The all top space where the block will be created is blocked by obstacles."  

        self.block_layout()            
        while self.cnt_move < self.n_move:
            if self.find_Possible_matching_block():
                self.select_and_swap()

                while self.mark_matched_block():
                    self.destroy_target += self.destroy()
                    self.drop_and_fill()

                    if self.destroy_target >= self.n_target:
                        self.render_board(self.board, 'success')
                        return True
                
                self.cnt_move += 1

            else:
                self.shuffle()
                while self.mark_matched_block():
                    self.destroy()
                    self.fill()
        
        self.render_board(self.board, 'fail')
        return False
    
    def find_Possible_matching_block(self):
        isFind = False
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.isout_of_range(self.board, self.pos(x, y)):
                    continue
            
                if self.find_block(x, y):
                    isFind = True
        
        if self.rendering_mode == self.rendering_mode.MOVE:
            self.render_board(self.board, 'MOVE')

        return isFind

    def find_block(self, x, y):
        isFind = False
        for key in self.diretion:
            dir = self.diretion[str(key)]
            move_pos = self.pos(x + dir.x, y + dir.y)
            if self.isout_of_range(self.board, move_pos):
                continue
            
            board = self.swap(self.pos(x, y), self.pos(x + dir.x, y + dir.y))

            cnt_matched = self.cnt_matched_block(board, x, y)

            if cnt_matched > 3:
                if board[y][x] == self.target_type:
                    self.matching_target.append({'x' : x, 'y' : y, 'dir': key})
                else :
                    self.matching_block.append({'x' : x, 'y' : y, 'dir': key})
                isFind = True

        return isFind

    def cnt_matched_block(self, board, x, y):
        cnt_up = self.matched_in_direction(board, x, y, self.diretion['up'])
        cnt_down = self.matched_in_direction(board, x, y, self.diretion['down'])
        cnt_left = self.matched_in_direction(board, x, y, self.diretion['left'])
        cnt_right = self.matched_in_direction(board, x, y, self.diretion['right'])

        return max(cnt_up + cnt_down , cnt_left + cnt_right)

    def matched_in_direction(self, board, x, y, dir):
        block_type = board[y][x]
        cnt = 1
        x += dir.x
        y += dir.y

        while not self.isout_of_range(board, self.pos(x, y)) and block_type == board[y][x]:
            cnt += 1
            x += dir.x
            y += dir.y

        return cnt

    def block_layout(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[y][x] != self.CellType.OBSTACLE:
                    self.board[y][x] = random.choice(list(self.CellType)[2 : self.n_block_type + 2])

        while self.mark_matched_block():
            self.destroy()
            self.fill()

        self.empty_cell.clear()

        if self.rendering_mode == self.rendering_mode.PART:
            self.render_board(self.board, 'block_layout')

    def mark_matched_block(self):
        ismarked = False
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.isout_of_range(self.board, self.pos(x, y)):
                    continue
                
                cnt_up = self.matched_in_direction(self.board, x, y, self.diretion['up'])
                cnt_down = self.matched_in_direction(self.board, x, y, self.diretion['down'])
                cnt_left = self.matched_in_direction(self.board, x, y, self.diretion['left'])
                cnt_right = self.matched_in_direction(self.board, x, y, self.diretion['right'])
                
                if cnt_up + cnt_down > 3:
                    ismarked = True
                    self.ismatched[y][x] = True

                    index_y = 1
                    while index_y < cnt_up:
                        self.ismatched[y - index_y][x] = True
                        index_y += 1
                    
                    index_y = 1
                    while index_y < cnt_down:
                        self.ismatched[y + index_y][x] = True
                        index_y += 1
                        
                if cnt_left + cnt_right > 3:
                    ismarked = True
                    self.ismatched[y][x] = True

                    index_x = 1
                    while index_x < cnt_left:
                        self.ismatched[y][x - index_x] = True
                        index_x += 1
                    
                    while index_x < cnt_right:
                        self.ismatched[y][x + index_x] = True
                        index_x += 1

        return ismarked
    
    def select_and_swap(self):
        if len(self.matching_target) != 0:
            random_element = random.choice(self.matching_target)
            x = random_element['x']
            y = random_element['y']
            dir = random_element['dir']

            self.board = self.swap(self.pos(x, y), self.pos(x + self.diretion[dir].x, y + self.diretion[dir].y))
        
        else:
            random_element = random.choice(self.matching_block)
            x = random_element['x']
            y = random_element['y']
            dir = random_element['dir']

            self.board = self.swap(self.pos(x, y), self.pos(x + self.diretion[dir].x, y + self.diretion[dir].y))
        
        self.matching_target.clear()
        self.matching_block.clear()
        
        if self.rendering_mode == self.rendering_mode.PART:
            self.render_board(self.board, 'select_and_swap')

    def swap(self, pos_1, pos_2):
        board = copy.deepcopy(self.board)
        temp = board[pos_1.y][pos_1.x]
        board[pos_1.y][pos_1.x] = board[pos_2.y][pos_2.x]
        board[pos_2.y][pos_2.x] = temp
        
        if self.rendering_mode == self.rendering_mode.PART:
            self.render_board(self.board, 'swap')

        return board
    
    def destroy(self):
        n_destroy_target = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.ismatched[y][x] == True:
                    if self.board[y][x] == self.target_type:
                        n_destroy_target += 1
                    self.board[y][x] = self.CellType.EMPTY
                    self.empty_cell.append(self.pos(x, y))
        
        self.clear_mark()

        if self.rendering_mode == self.RenderingMode.PART:
            self.render_board(self.board, 'destroy')

        return n_destroy_target

    def drop_and_fill(self):
        has_child = [[False for _ in range(self.max_x)] for _ in range(self.max_y)]
        isFill = True

        while isFill:
            isFill = False
            remove_list = []
            elected_list = []
            for cell_pos in self.empty_cell:
                if self.ispeak(cell_pos):
                    self.board[cell_pos.y][cell_pos.x] = random.choice(list(self.CellType)[2 : self.n_block_type + 2])
                    self.empty_cell.remove(cell_pos)
                    isFill = True
                    continue

                for key in self.drop_diretion:
                    dir = self.drop_diretion[key]
                    candidate_pos = self.pos(cell_pos.x + dir.x, cell_pos.y + dir.y)

                    if key == 'left':
                        left = -1
                        right = 1

                        while True:
                            if cell_pos.x + left < 0 and cell_pos.x + right >= self.max_x:
                                break

                            if cell_pos.x + left > -1 and self.board[0][cell_pos.x + left] != self.CellType.OBSTACLE:
                                candidate_pos = self.pos(cell_pos.x + dir.x, cell_pos.y + dir.y)
                                break
                            
                            elif cell_pos.x + right < self.max_x and self.board[0][cell_pos.x + right] != self.CellType.OBSTACLE:
                                candidate_pos = self.pos(cell_pos.x - dir.x, cell_pos.y - dir.y)
                                break

                            left -= 1
                            right += 1

                    if has_child[candidate_pos.y][candidate_pos.x] == True or self.board[candidate_pos.y][candidate_pos.x] == self.CellType.EMPTY:
                        break

                    if self.board[candidate_pos.y][candidate_pos.x] != self.CellType.OBSTACLE:
                        elected_list.append(candidate_pos)
                        remove_list.append(cell_pos)
                        has_child[candidate_pos.y][candidate_pos.x] = True
                        break
            
            for remove, elected in zip(remove_list, elected_list):
                isFill = True
                self.board = self.swap(elected, remove)
                self.empty_cell.remove(remove)
                has_child[elected.y][elected.x] = False
                self.empty_cell.append(elected)
        
        if self.rendering_mode == self.rendering_mode.PART:
            self.render_board(self.board, 'drop_and_fill')

    def fill(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[y][x] == self.CellType.EMPTY:
                    self.board[y][x] = random.choice(list(self.CellType)[2 : self.n_block_type + 2])
        
        if self.rendering_mode == self.rendering_mode.PART:
            self.render_board(self.board, 'fill')

    def shuffle(self):
        flat_list = [self.board[y][x] for x in range(self.max_x) for y in range(self.max_y) if self.board[y][x] != self.CellType.OBSTACLE]
        random.shuffle(flat_list)

        index = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[y][x] != self.CellType.OBSTACLE:
                    self.board[y][x] = flat_list[index]
                    index += 1

        if self.rendering_mode == self.rendering_mode.PART and self.rendering_mode == self.rendering_mode.MOVE:
            self.render_board(self.board, 'shuffle')            

    def clear_mark(self):
        self.ismatched = [[False for _ in range(self.max_x)] for _ in range(self.max_y)]

    def isout_of_range(self, board, pos):
        if pos.x >= self.max_x or pos.y >= self.max_y or pos.x < 0 or pos.y < 0:
            return True
        
        if board[pos.y][pos.x] == self.CellType.OBSTACLE:
            return True
        
        return False
    
    def ispeak(self, pos):
        if(pos.y == 0): return True
        return False
    
    def render_board(self, board, state):
        temp_board = np.full((self.max_y, self.max_x), 0)
        
        for x in range(self.max_x):
            for y in range(self.max_y):
                temp_board[y][x] = board[y][x].value

        float_array = temp_board.astype(float)
        target = 'num of destroy target : ' + str(self.destroy_target)
        n_move = 'number of move : ' + str(self.cnt_move)

        if self.rendering_mode != self.rendering_mode.RESULT:
            state = 'current state : ' + state

        pyplot.figure(figsize=(self.max_y, self.max_x))
        pyplot.imshow(float_array)
        pyplot.xticks([])
        plt.text(2, -1, state, color='red', fontsize=20, ha='center', va='center')
        plt.text(2, -1.5, target, color='red', fontsize=12, ha='center', va='center')
        plt.text(2, -2, n_move, color='red', fontsize=12, ha='center', va='center')
        pyplot.show()

    def isvalidation_from_board(self):
        for x in range(self.max_x):
            self.peak.append(self.pos(x,0))
            if self.board[0][x] == self.CellType.EMPTY:
                return True
            
        return False