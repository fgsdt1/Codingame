
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

    def findBallsHoles(self):

        for r in range(self.rows):
            for c in range(self.cols):
                if self.course[r][c].isdigit():
                    self.balls.append(Ball(r, c, int(self.course[r][c])))
                elif self.course[r][c] == "H":
                    self.holes.append(Hole(r, c))

    def findAllPaths(self):

        for b in self.balls:
            b.findPaths(self.course)

    def  findsolution(self):

        drawn, solution = self.findAllShots()

        if not drawn:
            return False, []
        else:
            # poner los hoyos y los lagos a "."
            for row in range(len(solution)):
                for col in range(len(solution[0])):
                    print(solution[row][col])
                    if solution[row][col] in ("X", "E"):
                        solution[row][col] = "."
                    print(solution[row][col])

            return drawn, solution

    def findAllShots(self):

        ball = 0
        drawn = False
        solution = copy.deepcopy(self.course)

        for path in self.balls[ball].paths:
            drawn, moves = self.drawlines(path, solution)
            if not drawn:    # It cannot be, undo the painting
                for coor in path:
                    solution[coor[0]][coor[1]] = self.course[coor[0]][coor[1]]
            else:
                if ball < len(self.balls)-1:
                    drawn, solution = self._findAllShots(ball+1, solution)
                    if not drawn:
                        for i in range(len(path)):
                            solution[path[i][0]][path[i][1]] = self.course[path[i][0]][path[i][1]]
                else:
                    return drawn, solution

        return drawn, solution

    def _findAllShots(self, ball, solution):

        drawn = False

        for path in self.balls[ball].paths:
            drawn, moves = self.drawlines(path, solution)
            if not drawn:    # It cannot be, undo the painting
                for i in range(moves):
                    solution[path[i][0]][path[i][1]] = self.course[path[i][0]][path[i][1]]
            else:
                if ball < len(self.balls)-1:
                    drawn, solution = self._findAllShots(ball+1, solution)
                    if not drawn:
                        for i in range(moves):
                            solution[path[i][0]][path[i][1]] = self.course[path[i][0]][path[i][1]]
                    else:
                        return drawn, solution
                else:
                    return drawn, solution

        return drawn, solution

    def drawlines(self, path, solution):

        for i in range(len(path)):
            if solution[path[i][0]][path[i][1]] == "H":
                # Hemos llegado al hoyo. Nunca pasará por un H si no es el último
                solution[path[i][0]][path[i][1]] = "E"            # Lo ponemos a X para que no se lo vuelva a pasar
                return True, i + 1

            elif (solution[path[i][0]][path[i][1]].isdigit() and i != 0) or \
                  solution[path[i][0]][path[i][1]] in (["^", "v", "<", ">"]) or \
                  solution[path[i][0]][path[i][1]] == "E":
                return False, i
            else:
                if path[i][0] < path[i+1][0]: solution[path[i][0]][path[i][1]] = "v"
                elif path[i][0] > path[i+1][0]: solution[path[i][0]][path[i][1]] = "^"
                elif path[i][1] < path[i+1][1]: solution[path[i][0]][path[i][1]] = ">"
                elif path[i][1] > path[i+1][1]: solution[path[i][0]][path[i][1]] = "<"
                else: return False, i

        return True, i + 1

class Ball():

    def __init__(self, row, col, nmoves):

        self.row = row
        self.col = col
        self.nmoves = nmoves
        self.paths = []
    
    def findPaths(self, course):


        if self.row + self.nmoves < len(course):
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 1, 0, self.row+self.nmoves, self.col, self.nmoves-1)
            self.paths.pop()

        if self.row - self.nmoves >= 0:
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, -1, 0, self.row-self.nmoves, self.col, self.nmoves-1)
            self.paths.pop()

        if self.col + self.nmoves < len(course[0]):
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 0, 1, self.row, self.col+self.nmoves, self.nmoves-1)
            self.paths.pop()

        if self.col - self.nmoves >= 0:
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 0, -1, self.row, self.col-self.nmoves, self.nmoves-1)
            self.paths.pop()

    def _findPaths(self, course, dirrow, dircol, posrow, poscol, nmoves):

        # we add the coordinate to the path
        for i in range(nmoves+1,0,-1):
            self.paths[-1].append([posrow-i*dirrow+1*dirrow, poscol-i*dircol+1*dircol])

        if course[posrow][poscol] == "H":
            # we add the coordinate to the path
            self.paths.append(copy.deepcopy(self.paths[-1]))
            return True

        if nmoves == 0:
            return False

        # if it is ".", it means we can continue
        if course[posrow][poscol] in ("."):
            # it will be in the same path adding dirs to the position
            newposrow = posrow + dirrow * nmoves
            newposcol = poscol + dircol * nmoves
            # if it is out of range we stop
            if 0 <= newposrow < len(course) and 0 <= newposcol < len(course[0]):

                self._findPaths(course, dirrow, dircol, newposrow, newposcol, nmoves-1)

                for i in range(nmoves):
                    self.paths[-1].pop()

            # If the direction changes but it is not a lake where we cannot change direction
            if dirrow == 0 and posrow + nmoves < len(course) and course[posrow+nmoves][poscol] != "X":

                possible = True
                for i in range(posrow + 1, posrow + nmoves):
                    if course[i][poscol] == "H" or course[i][poscol].isdigit():
                        possible = False

                if possible:
                    # we create a new element of the dictionary with a copy until this moment of the path
                    result = self._findPaths(course, 1, 0, posrow + nmoves, poscol, nmoves-1)

                for i in range(nmoves):
                    self.paths[-1].pop()

            if dirrow == 0 and posrow - nmoves >= 0 and course[posrow-nmoves][poscol] != "X":

                possible = True
                for i in range (posrow-1, posrow-nmoves):
                    if course[i][poscol] == "H" or course[i][poscol].isdigit():
                        possible = False

                if possible:
                    # we create a new element of the dictionary with a copy until this moment of the path
                    result = self._findPaths(course, -1, 0, posrow - nmoves, poscol, nmoves-1)

                for i in range(nmoves):
                    self.paths[-1].pop()

            if dircol == 0 and poscol + nmoves < len(course[0]) and  course[posrow][poscol+nmoves] != "X":

                possible = True
                for i in range(poscol + 1, poscol + nmoves):
                    if course[posrow][i] == "H" or course[posrow][i].isdigit():
                        possible = False

                if possible:
                    # we create a new element of the dictionary with a copy until this moment of the path
                    result = self._findPaths(course, 0, 1, posrow, poscol + nmoves, nmoves-1)

                for i in range(nmoves):
                    self.paths[-1].pop()

            if dircol == 0 and poscol - nmoves >= 0 and course[posrow][poscol-nmoves] != "X":

                possible = True
                for i in range(poscol - 1, poscol - nmoves):
                    if course[posrow][i] == "H" or course[posrow][i].isdigit():
                        possible = False

                if possible:
                    # we create a new element of the dictionary with a copy until this moment of the path
                    result = self._findPaths(course, 0, -1, posrow, poscol - nmoves, nmoves-1)

                for i in range(nmoves):
                    self.paths[-1].pop()

        # if it is a hole, we finish the search
        elif course[posrow][poscol] == "H":
            # we add the coordinate to the path
            self.paths.append(copy.deepcopy(self.paths[-1]))
            return True

        elif course[posrow][poscol].isdigit() or course[posrow][poscol] == "X":

            return False

        else:

            return False

    def __str__(self):

        paths = ""
        for n in self.paths:
            paths += (str(n ) + "\n")
        return "Ball: " + str(self.row) + str(self.col) + str(self.nmoves) + "\n" + paths


class Hole():

    def __init__(self, row, col):

        self.row = row
        self.col = col

    def __str__(self):

        return "Hole:" + str(self.row) + str(self.col)


mg = Game(3,3)

mg.course.append(["2", ".", "X"])
mg.course.append(["X", ".", "H"])
mg.course.append([".", "H", "1"])


mg = Game(5,3)

mg.course.append(["2", ".", "X"])
mg.course.append([".", ".", "H"])
mg.course.append([".", "H", "."])
mg.course.append([".", "H", "X"])
mg.course.append(["3", ".", "."])

mg = Game(5,5)

mg.course.append(["4", ".", ".", "X", "X"])
mg.course.append([".", "H", ".", "H", "."])
mg.course.append([".", ".", ".", "H", "."])
mg.course.append([".", "2", ".", ".", "2"])
mg.course.append([".", ".", ".", ".", "."])


mg = Game(6,6)

mg.course.append(["3", ".", ".", "H", ".", "2"])
mg.course.append([".", "2", ".", ".", "H", "."])
mg.course.append([".", ".", "H", ".", ".", "H"])
mg.course.append([".", "X", ".", "2", ".", "X"])
mg.course.append([".", ".", ".", ".", ".", "."])
mg.course.append(["3", ".", ".", "H", ".", "."])

mg = Game(8,8)

mg.course.append(['.', '.', '.', '.', '.', '.', '.', '4'])
mg.course.append(['.', '.', '.', '.', 'H', 'H', '.', '2'])
mg.course.append(['.', '.', '5', '.', '.', '.', '.', '.'])
mg.course.append(['H', '.', '.', '.', '.', '2', '2', 'X'])
mg.course.append(['.', '3', 'X', 'H', '.', 'H', 'X', 'X'])
mg.course.append(['.', '.', 'X', '3', '.', 'H', '.', 'X'])
mg.course.append(['.', '.', 'X', 'H', '.', '.', '.', '.'])
mg.course.append(['H', '2', 'X', '.', 'H', '.', '.', '3'])


mg = Game(8,8)

mg.course.append(['4', 'H', '5', '.', '.', '.', '.', '.'])
mg.course.append(['.', '.', '.', '.', '.', '.', '3', '.'])
mg.course.append(['.', '.', '.', '.', '.', '.', 'H', '.'])
mg.course.append(['.', '.', '.', '.', '.', 'H', '3', '.'])
mg.course.append(['.', '.', '.', '.', '.', '.', '.', '.'])
mg.course.append(['.', '.', '.', '.', 'H', 'H', '.', '.'])
mg.course.append(['.', '4', '3', '.', '.', '.', '.', '.'])
mg.course.append(['.', '.', 'H', '3', 'H', '.', '.', '.'])



solutionok = [[">", ">", ">", "H", ".", "v"],
              [".", ">", ">", ">", "H", "v"],
              [">", ">", "H", ".", ".", "H"],
              ["^", "X", ".", "v", ".", "X"],
              ["^", ".", ".", "v", ".", "."],
              ["^", ".", ".", "H", ".", "."]]


for row in mg.course:
    print ("x", row)

mg.findBallsHoles()


for i in mg.holes:
    print (i)

mg.findAllPaths()

for i in mg.balls:
    print (i)


drawn, solution = mg.findsolution()

for row in solution:
    print ("-", row)
