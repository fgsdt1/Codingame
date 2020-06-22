import copy as copy


class Game():

    def __init__(self, rows, cols):

        self.rows = rows
        self.cols = cols
        self.course = []        # Matrix to keep all the positions, individually, of the course (see sample bellow) 
        self.balls = []         # To keep the coordinates of the balls
        self.holes = []         # To keep the coordinates of the holes

    def __str__(self):

        return str(self.rows) + str(self.cols) + str(b for b in self.balls) + str(h for h in self.holes)

    # Method to find all the balls and holes of the course
    def findBallsHoles(self):

        for r in range(self.rows):
            for c in range(self.cols):

                if self.course[r][c].isdigit():
                    self.balls.append(Ball(r, c, int(self.course[r][c])))
                
                elif self.course[r][c] == "H":
                    self.holes.append(Hole(r, c))

    # Method to find all valid paths (from the start to any of the holes) of every ball
    def findAllPaths(self):

        # For every ball we call a ball method to find all its paths
        for b in self.balls:
            b.findPaths(self.course)

    # Method to be called after finding all the paths.
    # It will provide the stack of paths (pathsok) that together comply with the rules
    def findAllShots(self):

        # We start with the first ball and call recursively
        ball = 0
        found = False
        pathsok = []            # Stack that will contain all the right paths

        # for each path of the first ball
        for path in self.balls[ball].paths:
            # We append the path to the list  
            pathsok.append(path)

            # If there are no more balls, we stop, otherwise we call recurseively 
            # the find function for the next ball (ball+1)
            if ball + 1 == len(self.balls):
                found = True
            else:
                found, pathsok = self._findAllShots(ball + 1, pathsok)

            # If found is True means that we found the solution and call the method to 
            # print it as required 
            if found:
                self.drawlines(pathsok)
                return found, pathsok
            else:
                # Otherwise we delete the path appended and look for the next path of this ball
                pathsok.pop()

        return found, pathsok

    # Iterative method called to find the series of paths that together comply with all the rules
    def _findAllShots(self, ball, pathsok):

        found = False

        # for each path of the ball we try to find the one that is compatible 
        # with all previous paths in the pathsok list
        for path in self.balls[ball].paths:

            rightpath = True

            # For each element in the path (coor) we check that it is not comprised in 
            # any other previously appended path (pathsok)
            for coor in path:
                for row in pathsok:
                    if coor in row:
                        rightpath = False
                        break

            # If this path is ok, we append it to the stack 
            if rightpath:

                pathsok.append(path)

                # If there is no more balls, we return True up to the top. Otherwise we call recursively
                if ball + 1 == len(self.balls):
                    found = True
                else:
                    found, pathsok = self._findAllShots(ball + 1, pathsok)

                # If recursively we found a series of paths that comply, we return True and the stack
                # Otherwise we delete the last item of the stack
                if found:
                    return found, pathsok
                else:
                    pathsok.pop()

        return found, pathsok

    # Method to update the course changing the elements of the matrix with the correct paths as required
    def drawlines(self, pathsok):

        for path in pathsok:
            for i in range(len(path)):

                if self.course[path[i][0]][path[i][1]] == "H":
                    self.course[path[i][0]][path[i][1]] = "."
                else:
                    if path[i][0] < path[i + 1][0]:
                        self.course[path[i][0]][path[i][1]] = "v"
                    elif path[i][0] > path[i + 1][0]:
                        self.course[path[i][0]][path[i][1]] = "^"
                    elif path[i][1] < path[i + 1][1]:
                        self.course[path[i][0]][path[i][1]] = ">"
                    elif path[i][1] > path[i + 1][1]:
                        self.course[path[i][0]][path[i][1]] = "<"
                    else:
                        return False

        # Everything else we change to "."
        for row in range(len(self.course)):
            for col in range(len(self.course[0])):
                if self.course[row][col] not in ("v", "^", ">", "<"):
                    self.course[row][col] = "."


# Class to keep the ball information, including possible paths
class Ball():

    def __init__(self, row, col, nmoves):

        self.row = row
        self.col = col
        self.nmoves = nmoves        # Initial number of moves
        self.paths = []             # List of all possible correct paths of the ball (independent of the other balls paths)

    # Method to find recursively the paths of the ball
    # Each path will work as a stack of coordinates recursively appending or deleteng them
    def findPaths(self, course):

        # For each one of the possible movements we call the function recursively
        if self.row + self.nmoves < len(course):
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 1, 0, self.row + self.nmoves, self.col, self.nmoves - 1)
            self.paths.pop()

        if self.row - self.nmoves >= 0:
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, -1, 0, self.row - self.nmoves, self.col, self.nmoves - 1)
            self.paths.pop()

        if self.col + self.nmoves < len(course[0]):
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 0, 1, self.row, self.col + self.nmoves, self.nmoves - 1)
            self.paths.pop()

        if self.col - self.nmoves >= 0:
            self.paths.append([[self.row, self.col]])
            self._findPaths(course, 0, -1, self.row, self.col - self.nmoves, self.nmoves - 1)
            self.paths.pop()

    # Recursive method to find the paths of the ball
    # dirrow and dircol will provide information of the direction we want to move next (1, -1 or 0)
    # posrow and poscol are the current coordinates of the path
    # nomeves has the number of moves remaining
    def _findPaths(self, course, dirrow, dircol, posrow, poscol, nmoves):

        holeballfound = False

        # for the next nmoves and depending on the direction
        # we add the coordinates to the paths. They will be removed later if their are not viable
        for i in range(nmoves + 1, 0, -1):
            self.paths[-1].append([posrow - i * dirrow + 1 * dirrow, poscol - i * dircol + 1 * dircol])
            
            # if crossing a ball or a hole, the paths is not valid, except if the hole is the last position (i==-1)
            if course[posrow - i * dirrow + 1 * dirrow][poscol - i * dircol + 1 * dircol] == "H" and i != 1: 
                holeballfound = True
            if course[posrow - i * dirrow + 1 * dirrow][poscol - i * dircol + 1 * dircol].isdigit():
                holeballfound = True

        # If a ball or hole crossed, this path is not valid
        if holeballfound:
            return False

        # If we have ended in a hole we consider this path valid and create a copy in the stack 
        # to continue searching from this point
        if course[posrow][poscol] == "H":
            self.paths.append(copy.deepcopy(self.paths[-1]))
            return True

        # If no more moves available, this path is not valid
        if nmoves == 0:
            return False

        # if it is ".", it means we can continue
        if course[posrow][poscol] in ("."):
            # First check the next point in the same direction (adding dirs to the position)
            newposrow = posrow + dirrow * nmoves
            newposcol = poscol + dircol * nmoves
            # if it is out of range we stop
            if 0 <= newposrow < len(course) and 0 <= newposcol < len(course[0]):

                self._findPaths(course, dirrow, dircol, newposrow, newposcol, nmoves - 1)

                for i in range(nmoves):
                    self.paths[-1].pop()

            # For each new coordinate, if the direction changes but it is not a lake
            # we call recursively to find paths in the new direction
            if dirrow == 0 and posrow + nmoves < len(course) and course[posrow + nmoves][poscol] != "X":

                possible = True
                for i in range(posrow + 1, posrow + nmoves):
                    if course[i][poscol] == "H" or course[i][poscol].isdigit():
                        possible = False

                # If we did not go through a hole or ball....
                if possible:
                    result = self._findPaths(course, 1, 0, posrow + nmoves, poscol, nmoves - 1)

                    for i in range(nmoves):
                        self.paths[-1].pop()

            if dirrow == 0 and posrow - nmoves >= 0 and course[posrow - nmoves][poscol] != "X":

                possible = True
                for i in range(posrow - 1, posrow - nmoves):
                    if course[i][poscol] == "H" or course[i][poscol].isdigit():
                        possible = False

                # If we did not go through a hole or ball....
                if possible:
                    result = self._findPaths(course, -1, 0, posrow - nmoves, poscol, nmoves - 1)

                    for i in range(nmoves):
                        self.paths[-1].pop()

            if dircol == 0 and poscol + nmoves < len(course[0]) and course[posrow][poscol + nmoves] != "X":

                possible = True
                for i in range(poscol + 1, poscol + nmoves):
                    if course[posrow][i] == "H" or course[posrow][i].isdigit():
                        possible = False

                # If we did not go through a hole or ball....
                if possible:
                    result = self._findPaths(course, 0, 1, posrow, poscol + nmoves, nmoves - 1)

                    for i in range(nmoves):
                        self.paths[-1].pop()

            if dircol == 0 and poscol - nmoves >= 0 and course[posrow][poscol - nmoves] != "X":

                possible = True
                for i in range(poscol - 1, poscol - nmoves):
                    if course[posrow][i] == "H" or course[posrow][i].isdigit():
                        possible = False

                # If we did not go through a hole or ball....
                if possible:
                    result = self._findPaths(course, 0, -1, posrow, poscol - nmoves, nmoves - 1)

                    for i in range(nmoves):
                        self.paths[-1].pop()

        # If we land in a hole, we finish the search
        elif course[posrow][poscol] == "H":
            # we add the path to the paths stack by creating a copy 
            self.paths.append(copy.deepcopy(self.paths[-1]))
            return True

        # If we land in a lake, we finish the search
        elif course[posrow][poscol].isdigit() or course[posrow][poscol] == "X":

            return False

        else:

            return False

    def __str__(self):

        paths = ""
        for n in self.paths:
            paths += (str(n) + "\n")
        return "Ball: " + str(self.row) + str(self.col) + str(self.nmoves) + "\n" + paths

# Class to keep the hole information. Just coordinates
class Hole():

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "Hole:" + str(self.row) + str(self.col)


# ----------------------------------------------------------------------------------
# Program testing (one of the many possible courses)
# ----------------------------------------------------------------------------------

mg = Game(10, 10)
mg.course.append(['.', '.', '.', 'H', '.', '.', '.', '.', '.', '.'])
mg.course.append(['.', 'X', 'X', 'X', 'X', 'X', '.', '.', '.', '.'])
mg.course.append(['.', '.', '.', '.', '.', '.', 'X', '.', '.', '4'])
mg.course.append(['.', '.', 'H', '5', 'X', 'X', '.', '.', '.', '.'])
mg.course.append(['.', '.', '.', 'X', 'X', 'X', 'X', '.', '.', '.'])
mg.course.append(['.', '.', '.', 'X', 'X', 'X', 'X', '.', '.', '.'])
mg.course.append(['.', '.', '.', '.', 'X', 'X', '4', '.', '.', '.'])
mg.course.append(['3', '.', '.', 'X', '.', '.', '.', '.', '.', '.'])
mg.course.append(['.', '.', '.', '.', 'X', 'X', 'X', 'X', 'X', '.'])
mg.course.append(['.', '.', '.', '.', 'H', '.', 'H', '.', '.', '.'])

mg.findBallsHoles()
mg.findAllPaths()

result, pathsok = mg.findAllShots()

for path in pathsok:
    print ("->", path)

for row in mg.course:
    print(row)
