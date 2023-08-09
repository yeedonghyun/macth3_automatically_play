import random
import copy
import numpy as np

from matplotlib import pyplot
from enum import Enum
from collections import namedtuple

class Map():
    class CellType(Enum):
        OBSTACLE = -1
        EMPTY = 0
        APPLE = 1
        BANANA = 2
        ORANGE = 3
        #GRAPE = 4
        #WATERMELON = 5
        #STRAWBERRY = 6
        #mango = 7
        #pineapple = 8
        #kiwi = 9

    diretion = {}
    pos = namedtuple('pos', ['x', 'y'])

    diretion['up'] = pos(0, -1)
    diretion['down'] = pos(0, 1)
    diretion['left'] = pos(-1, 0)
    diretion['right'] = pos(1, 0)

    def __init__(self, max_x, max_y, n_target, target_type, n_move, board):
        self.ismatched = [[False for _ in range(max_x)] for _ in range(max_y)]
        self.empty_cell = []
        self.max_x = max_x
        self.max_y = max_y
        self.n_target = n_target
        self.target_type = target_type
        self.n_move = n_move
        self.board = board
        self.destroy_target = 0
        self.matching_target = []
        self.matching_block = []

    def play(self):
        self.block_layout()
        for cnt_move in range(self.n_move):
            if self.find_Possible_matching_block():
                self.select_and_swap()

                while self.mark_matched_block():
                    self.destroy_target += self.destroy()
                    self.drop()
                    self.fill()
                
                cnt_move += 1

            else:
                self.shuffle()

            if self.destroy_target >= self.n_target:
                return True

        return False
    
    def find_Possible_matching_block(self):
        isFind = False
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.isout_of_range(self.board, x, y):
                    continue
            
                if self.find_block(x, y):
                    isFind = True

        return isFind

    def find_block(self, x, y):
        isFind = False
        for key in self.diretion:
            dir = self.diretion[str(key)]    
            if self.isout_of_range(self.board, x + dir.x, y + dir.y):
                continue

            board = self.swap(x, y, dir)            
            cnt_matched = self.cnt_matched_block(board, x, y)
            cnt_moved_matched = self.cnt_matched_block(board, x + dir.x, y + dir.y)

            if cnt_matched > 3 or cnt_moved_matched > 3:
                if board[y][x] == self.target_type or board[y + dir.y][x + dir.x] == self.target_type:
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

        while not self.isout_of_range(board, x, y) and block_type == board[y][x]:
            cnt += 1
            x += dir.x
            y += dir.y

        return cnt

    def block_layout(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[y][x] != self.CellType.OBSTACLE:
                    self.board[y][x] = random.choice(list(self.CellType)[2:])

        while self.mark_matched_block():
            self.destroy()
            self.fill()

    def mark_matched_block(self):
        ismarked = False
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.isout_of_range(self.board, x, y):
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

            self.board = self.swap(x, y, self.diretion[dir])
        
        else:
            random_element = random.choice(self.matching_block)
            x = random_element['x']
            y = random_element['y']
            dir = random_element['dir']

            self.board = self.swap(x, y, self.diretion[dir])
        
        self.matching_target.clear
        self.matching_block.clear

    def swap(self, x, y, dir):

        board = copy.deepcopy(self.board)
        temp = board[y][x]
        board[y][x] = board[y + dir.y][x + dir.x]
        board[y + dir.y][x + dir.x] = temp
        
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
        return n_destroy_target

    def shuffle(self):
        flat_list = [self.board[y][x] for x in range(self.max_x) for y in range(self.max_y) if self.board[y][x] != self.CellType.EMPTY]
        random.shuffle(flat_list)

        index = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
                self.board[y][x] = flat_list[index]
                index += 1

        while self.mark_matched_block():
            self.destroy()
            self.fill()

    def drop(self):
        temp_list_size = len(self.empty_cell) + 1
        while not self.empty_cell and temp_list_size != len(self.empty_cell):
            for cell_pos in self.empty_block:

                if self.ispeak(cell_pos.y):
                    self.board[cell_pos.y][cell_pos.x] = random.choice(list(self.CellType)[2:])

                elif self.isempty_or_obstacle(cell_pos.x, cell_pos.y, self.pos(0, -1)): #up
                    success, self.board = self.swap(cell_pos.x, cell_pos.y, self.pos(0, -1))
                    self.empty_block.append(self.pos(cell_pos.x, cell_pos.y - 1))
                    self.empty_block.remove(cell_pos)

                elif self.isempty_or_obstacle(cell_pos.x, cell_pos.y, self.pos(1, -1)): #right up
                    success, self.board = self.swap(cell_pos.x, cell_pos.y, self.pos(1, -1))
                    self.empty_block.append(self.pos(cell_pos.x + 1, cell_pos.y - 1))
                    self.empty_block.remove(cell_pos)

                elif self.isempty_or_obstacle(cell_pos.x, cell_pos.y, self.pos(-1, -1)): #left up
                    success, self.board = self.swap(cell_pos.x, cell_pos.y, self.pos(-1, -1))
                    self.empty_block.append(self.pos(cell_pos.x - 1, cell_pos.y - 1))
                    self.empty_block.remove(cell_pos)

                elif self.isempty_or_obstacle(cell_pos.x, cell_pos.y, self.pos(1, 0)): #right
                    success, self.board = self.swap(cell_pos.x, cell_pos.y, self.pos(1, 0))
                    self.empty_block.append(self.pos(cell_pos.x + 1, cell_pos.y))
                    self.empty_block.remove(cell_pos)

                elif self.isempty_or_obstacle(cell_pos.x, cell_pos.y, self.pos(-1, 0)): #left
                    success, self.board = self.swap(cell_pos.x, cell_pos.y, self.pos(1, 0))
                    self.empty_block.append(self.pos(cell_pos.x - 1, cell_pos.y))
                    self.empty_block.remove(cell_pos)

            temp_list_size = len(self.empty_cell)

    def fill(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[y][x] == self.CellType.EMPTY:
                    self.board[y][x] = random.choice(list(self.CellType)[2:])

    def clear_mark(self):
        self.ismatched = [[False for _ in range(self.max_x)] for _ in range(self.max_y)]

    def isout_of_range(self, board, x, y):
        if x >= self.max_x or y >= self.max_y or  x < 0 or y < 0:
            return True
        
        if board[y][x] == self.CellType.OBSTACLE:
            return True
        
        return False
    
    def ispeak(self, y):
        if(y == 0): return True
        return False
    
    def isempty_or_obstacle(self, x, y, dir):
        if self.board[y + dir.y][x + dir.x] == self.CellType.EMPTY:
            return True
        if self.board[y + dir.y][x + dir.x] == self.CellType.OBSTACLE:
            return True
        
        return False
    
    def render_board(self, board):
        temp_board = np.full((self.max_x, self.max_y), 0)
        
        for x in range(self.max_x):
            for y in range(self.max_y):
                temp_board[y][x] = board[y][x].value

        float_array = temp_board.astype(float)
        pyplot.figure(figsize=(self.max_y, self.max_x))
        pyplot.imshow(float_array)
        pyplot.xticks([])
        pyplot.show()