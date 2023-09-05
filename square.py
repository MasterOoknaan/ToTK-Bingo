import numpy as np


class Square:
    x = 0
    y = 0
    diff = 0
    text = 'bingo spot'
    in_diag1 = False
    in_diag2 = False

    def __init__(self, x, y, d, t):
        self.x = x
        self.y = y
        self.diff = d
        self.text = t
        if x == y:
            self.in_diag1 = True
        if x * -1 + 4 == y:
            self.in_diag2 = True

    def __str__(self):
        return f"({self.x},{self.y}): {self.text}, {self.diff}"

    def set(self, d, t):
        self.diff = d
        self.text = t


class Five:
    name = ''
    remaining = 5
    current_diff = 0
    min_diff = 13
    max_diff = 18

    def __init__(self, n):
        name = n

    def check(self):
        # recommend lower bound
        if self.min_diff > self.current_diff:
            tmp = (self.min_diff - self.current_diff) / self.remaining
            if tmp > 1:
                return 0, np.trunc(tmp)
            else:
                return -1, 0
        # recommend upper bound
        else:
            if self.current_diff >= self.max_diff:
                return 1, 1

            tmp = (self.max_diff - self.current_diff) / self.remaining
            if tmp < 2:
                return 1, np.trunc(tmp)
            else:
                return -1, 0

    def update(self, d):
        self.remaining = self.remaining - 1
        self.current_diff = self.current_diff + d


class Grid:
    squares = []
    fives = []

    def __init__(self, s):
        self.slots = s

        for i in range(5):
            for j in range(5):
                self.squares.append(Square(i, j, 0, 'bingo spot'))

        for i in range(5):
            self.fives.append(Five(f'row{i}'))

        for i in range(5):
            self.fives.append(Five(f'col{i}'))

        self.fives.append(Five('diag1'))
        self.fives.append(Five('diag2'))

    def __str__(self):
        res = ''
        for s in self.squares:
            if s.y == 4:
                res = res + str(s) + '\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n'
            else:
                res = res + str(s) + '|\t|'
        return res

    def fill(self):
        order = np.arange(25)
        np.random.shuffle(order)
        for o in order:
            self.add(o)

    def add(self, pos):
        square = self.squares[pos]
        lower = 1
        upper = 5

        # row
        c = self.fives[square.x].check()
        if c[0] == 0:
            if lower < c[1]:
                lower = c[1]
        elif c[0] == 1:
            if upper > c[1]:
                upper = c[1]

        # col
        c = self.fives[square.y + 5].check()
        if c[0] == 0:
            if lower < c[1]:
                lower = c[1]
        elif c[0] == 1:
            if upper > c[1]:
                upper = c[1]

        # diag1
        if square.in_diag1:
            c = self.fives[10].check()
            if c[0] == 0:
                if lower < c[1]:
                    lower = c[1]
            elif c[0] == 1:
                if upper > c[1]:
                    upper = c[1]

        # diag2
        if square.in_diag2:
            c = self.fives[11].check()
            if c[0] == 0:
                if lower < c[1]:
                    lower = c[1]
            elif c[0] == 1:
                if upper > c[1]:
                    upper = c[1]

        #select square
        if lower > upper:
            upper = lower
        r = np.arange(lower, upper+1)
        success = False
        counter = 0
        while not success:
            index = np.random.randint(len(self.slots))
            counter = counter + 1
            if self.slots[index][0] in r or counter == 1000:
                success = True

        #update grid and fives, remove square from slots
        x = self.slots.pop(index)
        new_diff = x[0]
        new_text = x[1]
        square.set(new_diff, new_text)
        self.fives[square.x].update(new_diff)
        self.fives[square.y+5].update(new_diff)
        if square.in_diag1:
            self.fives[10].update(new_diff)
        if square.in_diag2:
            self.fives[11].update(new_diff)
