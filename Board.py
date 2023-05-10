
import random


class Game:
    def __init__(self):
        self.w = 7
        self.h = 6
        self.field = None
        self.moves = []
        self.winner = None
        self.reset()

    def is_over(self):
        if self.winner != None:
            return True
        if (self.w*self.h) == len(self.moves):
            return True
        return False

    def reset(self):
        self.field = []
        for y in range(self.h):
            tmp = []
            for x in range(self.w):
                tmp.append(0)
            self.field.append(tmp)
        self.moves = []
        self.winner = None

    def init0(self):
        self.place_move(2, 1)
        self.place_move(3, 2)
        self.place_move(3, 1)
        self.place_move(4, 2)
        #
        #
        #    x
        #   xoo
        # 0123456

    def __str__(self):
        res = " 0 1 2 3 4 5 6\n"
        for y in range(self.h):
            for x in range(self.w):
                tmp = self.field[y][x]
                if tmp == 0:
                    chr = " ."
                elif tmp == 1:
                    chr = " O"
                elif tmp == 2:
                    chr = " X"
                else:
                    raise Exception("bad value for field", tmp)
                res += chr
            res += "\n"
        return res

    # helper function for function below
    def is_same_symbol(self, symb, row, column):
        if 0 <= row < self.h and 0 <= column < self.w:
            return symb == self.field[row][column]
        return False

    def detect_win_at(self, row, column):
        # detect win con in column
        symb = self.field[row][column]
        count_same = 0
        for k in range(-3,4):
            if self.is_same_symbol(symb, row+k, column):
                count_same += 1
            else:
                count_same = 0
            if count_same == 4:
                return symb

        # detect win con in row
        count_same = 0
        for k in range(-3,4):
            if self.is_same_symbol(symb, row, column+k):
                count_same += 1
            else:
                count_same = 0
            if count_same == 4:
                return symb

        # detect win con in diagonal
        count_same = 0
        for k in range(-3,4):
            if self.is_same_symbol(symb, row+k, column+k):
                count_same += 1
            else:
                count_same = 0
            if count_same == 4:
                return symb

        # detect win con in other diagonal
        count_same = 0
        for k in range(-3,4):
            if self.is_same_symbol(symb, row+k, column-k):
                count_same += 1
            else:
                count_same = 0
            if count_same == 4:
                return symb
        return 0

    def place_move(self, column, s):
        if self.winner != None:
            raise Exception('game is over')
        row = self.find_next_free_row(column)
        self.field[row][column] = s
        win = self.detect_win_at(row, column)
        if win != 0:
            self.winner = win
        self.moves.append({'column':column, 
                           'symb':s,
                           'row':row,
                           'win':win})

    def undo_move(self):
        last_move = self.moves.pop()
        self.field[last_move['row']][last_move['column']] = 0
        self.winner = None

    def find_next_free_row(self, column):
        if self.field[-1][column] != 0:
            raise Exception("this column is already full")
        if self.field[0][column] == 0:
            return 0
        else:
            for y in range(self.h-1,-1,-1):
                if self.field[y-1][column] != 0:
                    return y

    def get_valid_moves(self):
        valid_ones = []
        for k in range(self.w):
            if self.field[-1][k] == 0:
                valid_ones.append(k)
        return valid_ones

    def do_random_move(self, symb):
        possible_moves = self.get_valid_moves()
        if len(possible_moves) == 0:
            raise Exception('no moves possible')
        idx = int(len(possible_moves) * random.random())
        move = possible_moves[idx]
        self.place_move(move, symb)

    def _do_depth_search(self, symb, num=1):
        win_stats = {1:0, 2:0, None:0}
        num_moves = len(self.moves)
        for k in range(num):
            cur_symb = symb
            while True:
                valid_moves = self.get_valid_moves()
                if self.winner != None:
                    win_stats[self.winner] += 1
                    break
                if len(valid_moves) == 0:
                    win_stats[None] += 1
                    break
                self.do_random_move(cur_symb)
                cur_symb = (cur_symb%2)+1
            while len(self.moves) > num_moves:
                self.undo_move()
        for k,v in win_stats.items():
            win_stats[k] = v/num
        return win_stats

    # get the win rate for each possible move
    def _do_depth_analysis(self, symb, num_depth_runs):
        win_rate_per_move = {}
        valid_moves = self.get_valid_moves()
        for move in valid_moves:
            self.place_move(move, symb)
            if self.winner == symb:
                win_rate_per_move[move] = 1.0
            else:
                stats = self._do_depth_search((symb%2)+1, num_depth_runs)
                win_rate_per_move[move] = stats[symb]
            self.undo_move()
        return win_rate_per_move

    # do a breadth search across all valid moves until
    # a certain depth is reached. then follow with
    # random moves until game over
    def _do_suboptimal_search(self, symb, full_search_depth, num_depth_runs):
        if full_search_depth == 0:
            win_rate = self._do_depth_search(symb, num_depth_runs)
            return None, win_rate
        else:
            valid_moves = self.get_valid_moves()
            move_stats = {}
            for move in valid_moves:
                self.place_move(move, symb)
                if self.winner == symb:
                    stats = {1:0, 2:0, None:0}
                    stats[symb] = 1.0
                    self.undo_move()
                    return move, stats
                else:
                    _, stats = self._do_suboptimal_search((symb%2)+1, full_search_depth-1, num_depth_runs)
                move_stats[move] = stats
                self.undo_move()
            # else minimize score of adversary
            # print(move_stats)
            adv_symb = (symb%2)+1
            min_score = 1.0
            mv = None
            scr = None
            for move, score in move_stats.items():
                #print(move, score)
                if score[adv_symb] <= min_score:
                    mv = move
                    scr = score
                    min_score = score[adv_symb]
            #print("ret", mv, scr)
            return mv, scr


def test0():
    g = Game()
    g.place_move(4, 1)
    g.place_move(4, 2)
    g.place_move(4, 2)
    g.place_move(4, 2)
    g.undo_move()
    for k in range(g.h):
        g.place_move(3, (k%2)+1)
    g.do_random_move(2)
    print(g)
    print(g.moves)
    print(g.winner)
    print(g.get_valid_moves())

def test1():
    g = Game()
    g.init0()
    print(g)
    stats = g._do_depth_search(1, num=200)
    print(stats)

def test2():
    g = Game()
    stats = g._do_suboptimal_search(1, 2, 20)
    print(stats)

def test3():
    g = Game()
    g.init0()
    print(g)
    g._do_depth_analysis(1,100)
    g._do_depth_analysis(2,100)

if __name__ == "__main__":
    test2()
