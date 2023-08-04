import random

from enum import Enum
from collections import namedtuple

class Map():
    class CellType(Enum):
        OBSTACLE = -1
        EMPTY = 0
        APPLE = 1
        BANANA = 2
        #ORANGE = 3
        #GRAPE = 4
        #WATERMELON = 5
        #STRAWBERRY = 6
        #mango = 7
        #pineapple = 8
        #kiwi = 9

    diretion = {}
    dir = namedtuple('dir', ['x', 'y'])

    diretion['up'] = dir(-1, 0)
    diretion['down'] = dir(1, 0)
    diretion['left'] = dir(0, -1)
    diretion['right'] = dir(0, 1)

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
                if self.board[y][x] != self.CellType.OBSTACLE:
                    self.board[y][x] = random.choice(list(self.CellType)[2:])

        while self.mark_matched_block():
            self.destroy()
            self.fill()

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
            if self.board[y][x] == self.target_type:
                self.matching_target.append({'x' : x, 'y' : y, 'dir': dir_key})
            else :
                self.matching_block.append({'x' : x, 'y' : y, 'dir': dir_key})        

    def mark_matched_block(self):
        ismarked = False
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.isout_of_range(x, y):
                    continue

                cnt_up = self.matched_in_direction(x, y, self.diretion['up'])
                cnt_down = self.matched_in_direction(x, y, self.diretion['down'])
                cnt_left = self.matched_in_direction(x, y, self.diretion['left'])
                cnt_right = self.matched_in_direction(x, y, self.diretion['right'])

                if cnt_up + cnt_down + 1 >= 3:
                    ismarked = True
                    self.ismatched[y][x] = True
                    for match_y in range(cnt_up):
                        self.ismatched[y - match_y][x] = True
                    
                    for match_y in  range(cnt_down):
                        self.ismatched[y + match_y][x] = True
                        
                if cnt_left + cnt_right + 1 >= 3:
                    ismarked = True
                    self.ismatched[y][x] = True
                    for match_x in range(cnt_left):
                        self.ismatched[y][x - match_x] = True
                    
                    for match_x in range(cnt_right):
                        self.ismatched[y][x + match_x] = True

        return ismarked

    def cnt_matched_block(self, x, y):
        cnt_Vertical = self.matched_in_direction(x, y, self.diretion['up']) + self.matched_in_direction(x, y, self.diretion['down']) + 1
        cnt_Landscape = self.matched_in_direction(x, y, self.diretion['left']) + self.matched_in_direction(x, y, self.diretion['right']) + 1
        
        return max(cnt_Vertical, cnt_Landscape)    

    def matched_in_direction(self, x, y, dir):
        block_type = self.board[y][x]
        cnt = 0
        print(x)
        print(y)
        self.board_print()
        x += dir.x
        y += dir.y
        print(x)
        print(y)

        while not self.isout_of_range(x, y) and block_type == self.board[y][x]:
            cnt += 1
            x += dir.x
            y += dir.y

        return cnt
    
    def isout_of_range(self, x, y):
        if self.board[y][x] == self.CellType.OBSTACLE or x > self.max_x or y > self.max_y or  x < 0 or y < 0:
            return True
        
        return False
    
    def swap(self):
        isswap = False
        if len(self.matching_target) != 0:
            isswap = True
            random_element = random.choice(self.matching_target)
            x = self.matching_target['x'] in random_element
            y = self.matching_target['y'] in random_element
            dir = self.matching_target['dir'] in random_element

            temp = self.board[y][x]
            self.board[y][x] = self.board[y + self.diretion[str(dir)].y][x + self.diretion[str(dir)].x]
            self.board[y + self.diretion[str(dir)].y][x + self.diretion[str(dir)].x] = temp

        elif len(self.matching_block) != 0:
            isswap = True
            random_element = random.choice(self.matching_block)
            
            x = self.matching_block['x'] in random_element
            y = self.matching_block['y'] in random_element
            dir = self.matching_block['dir'] in random_element

            temp = self.board[y][x]
            self.board[y][x] = self.board[y + self.diretion[str(dir)].y][x + self.diretion[str(dir)].x]
            self.board[y + self.diretion[str(dir)].y][x + self.diretion[str(dir)].x] = temp
        
        if not isswap:
            print("failed to swap")
    
    def destroy(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.ismatched[y][x] == True:
                    self.board[y][x] = self.CellType.EMPTY

    def shuffle(self):
        flat_list = [self.board[y][x] for x in range(self.max_x) for y in range(self.max_y) if self.board[y][x] != self.CellType.EMPTY]
        random.shuffle(flat_list)

        index = 0
        for x in range(self.max_x):
            for y in range(self.max_y):
                self.board[y][x] = flat_list[index]
                index += 1

        while self.isfind_matched_block():
            self.destroy()
            self.fill()

    #def drop(self):

    def fill(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                if self.board[y][x] == self.CellType.EMPTY:
                    self.board[y][x] = random.choice(list(self.CellType)[2:])

        self.clear_mark()

    def clear_mark(self):
        self.ismatched = [[False for _ in range(self.max_x)] for _ in range(self.max_y)]

    def board_print(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                print(self.board[y][x].value, end=' ')
            print() 