import random

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
    dir = namedtuple('dir', ['x', 'y'])

    diretion['up'] = dir(0, -1)
    diretion['down'] = dir(0, 1)
    diretion['left'] = dir(-1, 0)
    diretion['right'] = dir(1, 0)

    def __init__(self, max_x, max_y, n_target, target_type, n_move, board):
        self.ismatched = [[False for _ in range(max_x)] for _ in range(max_y)]
        self.max_x = max_x
        self.max_y = max_y
        self.n_target = n_target
        self.target_type = target_type    
        self.n_move = n_move
        self.board = board
        self.destroy_target = 0

    def play(self):
        self.block_layout()
        for cnt_move in range(self.n_move):
            if self.find_matching_block():
                self.swap()

                while self.isfind_matched_block():
                    self.destroy_target += self.destroy()
                    self.drop()
                    self.fill()
                
                cnt_move += 1

            else:
                self.shuffle()

            if self.destroy_target >= self.n_target:
                return True

        return False

    def block_layout(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[x][y] != self.CellType.OBSTACLE:
                    self.board[x][y] = random.choice(list(self.CellType)[2:])

        #while self.isfind_matched_block():
        #    self.destroy()
        #    self.fill()

    def find_matching_block(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.isout_of_range(x, y): 
                    continue
                
                for key in self.diretion:
                    self.find_block(x, y, key)

    def find_block(self, x, y, dir_key):
        x += self.diretion[dir_key].x
        y += self.diretion[dir_key].y
        if self.isout_of_range(x, y):            
            return
        
        self.board_print()
        count = self.cnt_matched_block(x, y) 

        if count >= 3: 
            if self.board[x][y] == self.target_type:
                self.matching_target.append({'x' : x, 'y' : y, 'dir': dir_key, 'count' : count})
            else :
                self.matching_block.append({'x' : x, 'y' : y, 'dir': dir_key, 'count' : count})        

    def mark_matched_block(self):
        ismarked = False
        for x in range(self.max_x):
            for y in range(self.max_y):
                cnt_up = self.matched_in_direction(x, y, self.diretion['up'])
                cnt_down = self.matched_in_direction(x, y, self.diretion['down'])
                cnt_left = self.matched_in_direction(x, y, self.diretion['left'])
                cnt_right = self.matched_in_direction(x, y, self.diretion['right'])

                if cnt_up + cnt_down + 1 >= 3:
                    ismarked = True
                    for match_y in cnt_up:
                        self.ismatched[x][y - match_y] = True
                    
                    for match_y in cnt_down:
                        self.ismatched[x][y + match_y] = True
                        
                if cnt_left + cnt_right + 1 >= 3:
                    ismarked = True
                    for match_x in cnt_left:
                        self.ismatched[x - match_x][y] = True
                    
                    for match_x in cnt_right:
                        self.ismatched[x + match_x][y] = True

        return ismarked

    def cnt_matched_block(self, x, y):
        cnt_Vertical = self.matched_in_direction(x, y, self.diretion['up']) + self.matched_in_direction(x, y, self.diretion['down']) + 1
        cnt_Landscape = self.matched_in_direction(x, y, self.diretion['left']) + self.matched_in_direction(x, y, self.diretion['right']) + 1
        
        return max(cnt_Vertical, cnt_Landscape)    

    def matched_in_direction(self, x, y, dx, dy):
        block_type = self.board[x][y]
        cnt = 0

        while block_type == self.board[x + dx][y + dy]:
            cnt += 1

        return cnt
    
    def isout_of_range(self, x, y):
        if self.board[x][y] == self.CellType.OBSTACLE or x > self.max_x or y > self.max_y or  x < 0 or y < 0:
            return True
        
        return False
    
    #def swap(self):

        #temp = self.board[x_1][y_1]
        #self.board[x_1][y_1] = self.board[x_2][y_2]
        #self.board[x_2][y_2] = temp
        
    def destroy(self):
        for x in self.max_x:
            for y in self.max_y:
                if self.ismatched[x][y] == True:
                    self.board[x][y] = self.CellType.EMPTY

    def shuffle(self):


        while self.isfind_matched_block():
            self.destroy()
            self.fill()

    #def drop(self):

    #def fill(self):

    def board_print(self):
        for row in self.board:
            for cell in row:
                print(cell.value, end=' ')
            print() 