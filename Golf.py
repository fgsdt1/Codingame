import random as rd
import copy as copy

class Game():

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols
        self.course = []
        self.balls = []
        self.holes = []

    def __str__(self):

        return str(self.rows)+str(self.cols)+str(b for b in self.balls)+str(h for h in self.holes)

    def findAllPaths(self):

        for b in self.balls:
            b.findPaths(self.course)


class Ball():

    def __init__(self, row, col, nmoves):

        self.row = row
        self.col = col
        self.nmoves = nmoves
        self.paths = []
    
    def findPaths(self, course):


        if self.row + 1 < len(course):
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 1, 0, self.row+1, self.col, self.nmoves)
            self.paths.pop()

        if self.row - 1 >= 0:
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, -1, 0, self.row-1, self.col, self.nmoves)
            self.paths.pop()

        if self.col + 1 < len(course[0]):
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 0, 1, self.row, self.col+1, self.nmoves)
            self.paths.pop()

        if self.col -1 >= 0:
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 0, -1, self.row, self.col-1, self.nmoves)
            self.paths.pop()

    def _findPaths(self, course, dirrow, dircol, posrow, poscol, nmoves):

        if nmoves == 0:
            return False

#        pathnumber = len(self.paths)-1

        # if it is ".", it means we can continue
        if course[posrow][poscol] == ".":
            # we add the coordinate to the path
            self.paths[-1].append([posrow, poscol])

            # it will be in the same path adding dirs to the position
            newposrow = posrow + dirrow
            newposcol = poscol + dircol
            # if it is out of range we stop
            if 0 <= newposrow < len(course) and 0 <= newposcol < len(course[0]):
                self._findPaths(course, dirrow, dircol, newposrow, newposcol, nmoves)
                self.paths[-1].pop()

            # If the direction changes
            if dirrow == 0 and posrow + 1 < len(course):
                nmoves -= 1
                # we create a new element of the dictionary with a copy until this moment of the path
                result = self._findPaths(course, 1, 0, posrow + 1, poscol, nmoves)
                self.paths[-1].pop()
                nmoves += 1

            if dirrow == 0 and posrow -1 >= 0:
                nmoves -= 1

                result = self._findPaths(course, -1, 0, posrow - 1, poscol, nmoves)
                self.paths[-1].pop()
                nmoves += 1

            if dircol == 0 and poscol + 1 < len(course[0]):
                nmoves -= 1
                # we create a new element of the dictionary with a copy until this moment of the path
                result = self._findPaths(course, 0, +1, posrow, poscol+1, nmoves)
                self.paths[-1].pop()
                nmoves += 1

            if dircol == 0 and poscol -1 >= 0:
                nmoves -= 1
                # we create a new element of the dictionary with a copy until this moment of the path
                result = self._findPaths(course, 0, -1, posrow, poscol - 1, nmoves)
                self.paths[-1].pop()
                nmoves += 1

        # if it is a hole, we finish the search
        elif course[posrow][poscol] == "H":
            # we add the coordinate to the path
            self.paths[-1].append([posrow, poscol])
            self.paths.append(copy.deepcopy(self.paths[-1]))
            return True

        elif course[posrow][poscol].isdigit():

            self.paths[-1].append([posrow, poscol])
            return False

        else:

            return False

    def __str__(self):

        paths = ""
        for n in self.paths:
            print (n)
            paths += str(n)
        return "Ball: " + str(self.row) + str(self.col) + str(self.nmoves) + paths


class Hole():

    def __init__(self, row, col):

        self.row = row
        self.col = col

    def __str__(self):

        return "Hole:" + str(self.row) + str(self.col)

'''
3 3
2.X
X.H
.H1
'''
'''
mg.course.append(["2", ".", "X"])
mg.course.append(["X", ".", "H"])
mg.course.append([".", "H", "1"])
'''

mg = Game(5,3)

mg.course.append(["2", ".", "."])
mg.course.append([".", ".", "H"])
mg.course.append([".", "H", "."])
mg.course.append([".", "H", "."])
mg.course.append(["2", ".", "."])

for r in range(mg.rows):
    for c in range(mg.cols):
        if mg.course[r][c].isdigit():
            mg.balls.append(Ball(r, c, int(mg.course[r][c])))
        elif mg.course[r][c] == "H":
            mg.holes.append(Hole(r,c))

for i in mg.balls:
    print (i)

for i in mg.holes:
    print (i)

mg.findAllPaths()

for i in mg.balls:
    print (i)

