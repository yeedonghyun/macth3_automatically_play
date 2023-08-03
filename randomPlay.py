class Map():
    def __init__(self, max_x, max_y, target, n_move):
        self.target = target
        self.max_x = max_x
        self.max_y = max_y
        self.n_move = n_move

    def play(self, test_map):
        