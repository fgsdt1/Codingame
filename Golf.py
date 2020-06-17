import random as rd
import copy as copy

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
            self.balls[b].findPaths(self.course)



class Ball():

    def __init__(self, row, col, nmoves):

        self.row = row
        self.col = col
        self.nmoves = nmoves
        self.paths = []
    
    def findPaths(self, course):

        if self.row + 1 < len(course):
            self.paths[len(self.paths)] = [self.row, self.col]
            self._findPaths(course, 1, 0, self.row+1, self.col)

        if self.row - 1 >= 0:
            self.paths[len(self.paths)] = [self.row, self.col]
            self._findPaths(course, -1, 0, self.row-1, self.col)

        if self.col + 1 < len(course[0]):
            self.paths[len(self.paths)] = [self.row, self.col]
            self._findPaths(course, 0, 1, self.row, self.col+1)

        if self.col -1 >= 0:
            self.paths[len(self.paths)] = [self.row, self.col]
            self._findPaths(course, 0, -1, self.row, self.col-1)


    def _findPaths(self, course, dirrow, dircol, posrow, poscol):

        # if it is ".", it means we can continue
        if course[posrow][poscol] == ".":
            # we add the coordinate to the path
            self.paths[len(self.paths)-1].append([posrow, poscol])

            # it will be in the same path adding dirs to the position
            newposrow = posrow + dirrow
            newposcol = poscol + dircol
            # if it is out of range we stop
            if 0 <= newposrow <= len(course) and 0 <= newposcol <= len(course[0]):
                self._findPaths(self, course, dirrow, dircol, newposrow, newposcol)
                oldpath = []
            else:
                oldpath=self.paths.pop(len(self.paths)-1)

            if dirrow != 1 and self.row + 1 < len(course):
                # we create a new element of the dictionary with a copy until this moment of the path
                if len(oldpath) != 0:
                    self.paths[len(self.paths)] = copy.deepcopy(self.paths[len(self.paths)-1])
                else:
                    self.paths[len(self.paths)] = copy.deepcopy(oldpath)
                    _findPaths(self, course, 1, 0, self.row+1, self.col)

            if dirrow != -1 and self.row -1 >= 0:
                # we create a new element of the dictionary with a copy until this moment of the path
                if len(oldpath) != 0:
                    self.paths[len(self.paths)] = copy.deepcopy(self.paths[len(self.paths)-1])
                else:
                    self.paths[len(self.paths)] = copy.deepcopy(oldpath)
                    _findPaths(self, course, -1, 0, self.row-1, self.col)

            if dircol != 1 and self.col + 1 < len(course[0]):
                # we create a new element of the dictionary with a copy until this moment of the path
                if len(oldpath) != 0:
                    self.paths[len(self.paths)] = copy.deepcopy(self.paths[len(self.paths)-1])
                else:
                    self.paths[len(self.paths)] = copy.deepcopy(oldpath)
                    _findPaths(self, course, 0, +1, self.row, self.col+1)

            if dircol != -1 and self.col -1 >= 0:
                # we create a new element of the dictionary with a copy until this moment of the path
                if len(oldpath) != 0:
                    self.paths[len(self.paths)] = copy.deepcopy(self.paths[len(self.paths)-1])
                else:
                    self.paths[len(self.paths)] = copy.deepcopy(oldpath)
                    _findPaths(self, course, 0, -1, self.row, self.col-1)

         
    
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



