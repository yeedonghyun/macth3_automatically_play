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
    drop_diretion['right'] = pos(1, 0)

    def __init__(self, max_x, max_y, n_target, target_type, n_move, board):
        self.ismatched = [[False for _ in range(max_x)] for _ in range(max_y)]
        self.matching_target = []
        self.matching_block = []
        self.empty_cell = []
        self.max_x = max_x
        self.max_y = max_y
        self.n_target = n_target
        self.target_type = target_type
        self.n_move = n_move
        self.board = board
        self.destroy_target = 0

    def play(self):
        self.block_layout()
        self.render_board(self.board)
        for cnt_move in range(self.n_move):
            if self.find_Possible_matching_block():
                self.select_and_swap()
                self.render_board(self.board)   

                while self.mark_matched_block():
                    self.destroy_target += self.destroy()
                    self.render_board(self.board)  
                    self.drop_and_fill()
                    self.render_board(self.board)
                
                cnt_move += 1

            else:
                self.shuffle()
                self.render_board(self.board)  

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
            move_pos = self.pos(x + dir.x, y + dir.y)
            if self.isout_of_range(self.board, move_pos.x, move_pos.y):
                continue
            
            board = self.swap(self.pos(x, y), self.pos(x + dir.x, y + dir.y))

            cnt_matched = self.cnt_matched_block(board, x, y)
            cnt_moved_matched = self.cnt_matched_block(board, move_pos.x, move_pos.y)

            if cnt_matched > 3 and cnt_moved_matched > 3:
                if board[y][x] == self.target_type or board[move_pos.y][move_pos.x] == self.target_type:
                    self.matching_target.append({'x' : x, 'y' : y, 'dir': key})
                else :
                    self.matching_block.append({'x' : x, 'y' : y, 'dir': key})

            elif cnt_matched > 3:
                if board[y][x] == self.target_type:
                    self.matching_target.append({'x' : x, 'y' : y, 'dir': key})
                else :
                    self.matching_block.append({'x' : x, 'y' : y, 'dir': key})
                isFind = True

            elif cnt_moved_matched > 3:
                if board[move_pos.y][move_pos.x] == self.target_type == self.target_type:
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

        self.empty_cell.clear()

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

            self.board = self.swap(self.pos(x, y), self.pos(x + self.diretion[dir].x, y + self.diretion[dir].y))
        
        else:
            random_element = random.choice(self.matching_block)
            x = random_element['x']
            y = random_element['y']
            dir = random_element['dir']

            self.board = self.swap(self.pos(x, y), self.pos(x + self.diretion[dir].x, y + self.diretion[dir].y))
        
        self.matching_target.clear
        self.matching_block.clear

    def swap(self, pos_1, pos_2):
        board = copy.deepcopy(self.board)
        temp = board[pos_1.y][pos_1.x]
        board[pos_1.y][pos_1.x] = board[pos_2.y][pos_2.x]
        board[pos_2.y][pos_2.x] = temp
        
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

    def drop_and_fill(self):
        has_child = [[False for y in range(self.max_x)] for x in range(self.max_y)]
                
        while len(self.empty_cell) != 0:
            remove_list = []
            elected_list = []
            isfill_peak = False
            for cell_pos in self.empty_cell:

                if self.ispeak(cell_pos.y):
                    self.board[cell_pos.y][cell_pos.x] = random.choice(list(self.CellType)[2:])
                    self.empty_cell.remove(cell_pos)
                    isfill_peak = True

                else :
                    for key in self.drop_diretion:
                        dir = self.drop_diretion[key]
                        candidate_pos = self.pos(cell_pos.x + dir.x, cell_pos.y + dir.y)

                        if self.board[candidate_pos.y][candidate_pos.x] == self.CellType.EMPTY or has_child[candidate_pos.y][candidate_pos.x] == True:
                            break
                        
                        if self.board[candidate_pos.y][candidate_pos.x] != self.CellType.OBSTACLE:
                            elected_list.append(candidate_pos)
                            remove_list.append(cell_pos)
                            has_child[candidate_pos.y][candidate_pos.x] = True
                            break
            
            if len(remove_list) == 0 and not isfill_peak:
                break
            
            for remove, elected in zip(remove_list, elected_list):
                self.empty_cell.remove(remove)
                self.empty_cell.append(elected)
                self.board = self.swap(elected, remove)
                has_child[elected.y][elected.x] = False

    def fill(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[y][x] == self.CellType.EMPTY:
                    self.board[y][x] = random.choice(list(self.CellType)[2:])

    def shuffle(self):
        flat_list = [self.board[y][x] for x in range(self.max_x) for y in range(self.max_y) if self.board[y][x] != self.CellType.OBSTACLE]
        random.shuffle(flat_list)

        index = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[y][x] != self.CellType.OBSTACLE:
                    self.board[y][x] = flat_list[index]
                    index += 1

        while self.mark_matched_block():
            self.destroy()
            self.fill()

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
        
    def render_board(self, board):
        temp_board = np.full((self.max_y, self.max_x), 0)
        
        for x in range(self.max_x):
            for y in range(self.max_y):
                temp_board[y][x] = board[y][x].value

        float_array = temp_board.astype(float)
        pyplot.figure(figsize=(self.max_y, self.max_x))
        pyplot.imshow(float_array)
        pyplot.xticks([])
        pyplot.show()