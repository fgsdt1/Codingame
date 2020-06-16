import random as rd

class Game():

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols
        self.course = []
        self.balls = {}
        self.holes = {}

    def __str__(self):

        return (str(self.rows)+str(self.cols)+str(b for b in self.balls)+str(h for h in self.holes))

    def findAllPaths(self):

        for b in self.balls:
            self.balls[b].findPaths(self)

    #def __str__(self):

     #   return (str(self.rows) + "x" + str(self.cols))


class Ball():

    def __init__(self, row, col, nmoves):

        self.row = row
        self.col = col
        self.nmoves = nmoves
        self.paths = {}
    
    def findPaths(self, course):

        self.paths = _findPaths(self, course, self.row, self.col)

    def _findPaths(self, course, posrow, poscol):


    
    def __str__(self):

        return ("Ball: " + str(self.row) + str(self.col) + str(self.nmoves))


class Hole():

    def __init__(self, row, col):

        self.row = row
        self.col = col

    def __str__(self):

        return ("Hole:" + str(self.row) + str(self.col))

'''
3 3
2.X
X.H
.H1
'''

mg = Game(3,3)

mg.course.append(["2", ".", "X"])
mg.course.append(["X", ".", "H"])
mg.course.append([".", "H", "1"])

for r in range(mg.rows):
    for c in range(mg.cols):
        if mg.course[r][c].isdigit():
            mg.balls[str(r)+"-"+str(c)] = Ball(r, c, int(mg.course[r][c]))
        elif mg.course[r][c] == "H":
            mg.holes[str(r)+"-"+str(c)] = Hole(r,c)

for i in mg.balls:
    print (mg.balls[i])

for i in mg.holes:
    print (mg.holes[i])

mg.findAllPaths()



