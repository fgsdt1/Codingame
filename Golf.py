import random as rd

class Game():

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols
        self.course = []

    def __str__(self):

        return (str(self.rows), "x", str(self.cols))

class Ball():

    def __init__(self, row, col, nmoves):

        
        self.row = row
        self.col = col
        self.nmoves = nmoves
        self.paths = {}
    
    def __str__(self):

        return ("Ball: " + str(self.row) + str(self.col) + str(self.nmoves))


class Hole():

    def __init__(self, row, col)

        self.row = row
        self.col = col

    def __str__(self)

        return ("Hole:", str(self.row), str(self.col))

'''
3 3
2.X
X.H
.H1
'''

myGame = Game(3,3)
myBalls = []
myHoles = []

myGame.course.append(["2", ".", "X"])
myGame.course.append(["X", ".", "H"])
myGame.course.append([".", "H", "1"])

for r in range(myGame.rows):
    for c in range(myGame.cols):
        if myGame.course[r][c].isdigit():
            myBalls.append(Ball(r, c, int(myGame.course[r][c])))
        elif myGame.course[r][c] = "H":
            myHoles.append(Hole(r,c))

for i in mayBalls:
    print i

for i in myHoles:
    print i



