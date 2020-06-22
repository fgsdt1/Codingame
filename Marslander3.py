import sys

# The trajectory will consist of the following phases:
# Phase 1 We go vertically up to the heiht of the top of the cave
# Phase 2 We level the horizontal speed for easy descend
# Phase 3 We descend slowly until the adequate angle to the landing area (45º)
# Phase 4 We follow incline descend towards the border of the landing area 
# Phase 5 We level the horizontal speed for easy descend
# Phase 6 We descend

# funtion to level horizontally the module
def levelmodule():

    power = 4
    if abs(h_speed) < 70:
        if abs(h_speed) < 10:
            if h_speed < 0:
                rot = (h_speed-5)
            else:
                rot = (h_speed+5)
        elif h_speed < 0:
            rot = (h_speed-8)
        else:
            rot = (h_speed+8)
    elif h_speed < 0:
        rot = -90
    else:
        rot = 90

    return (rot, power)

# funtion for vertical descend maintaining appropiate vertical speed
def verticaldescend():

    if abs(v_speed) < 15:
        rot = 0
        power = 3
    else:
        rot = 0
        power = 4

    return (rot, power)

# Analysing the surface
surface = []
surface_n = int(input())  # the number of points used to draw the surface of Mars.

for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    surface.append([land_x, land_y])

# We look for the landing area and the cave orientation
landinix = 0
landendx = 0
opencave = "right"

for i in range(len(surface)-1):

    if landinix != 0:
        if landinix >= surface[i][0] <= landendx:
            opencave = "left" 
    
    if surface[i][1] == surface[i+1][1]:
        landinix, landiniy = surface[i]
        landendx, landendy = surface[i+1]

# We assign the initial descend point in the x axis
if opencave == "right":
    descendpointx = landendx + 1000
else:
    descendpointx = landinix - 1000

# Find top of the cave. We look for the top peak of the cave if it is left
# or the top of the profile if it is right
maxcaveheight = 0  
if opencave == "left":
    for i in range(len(surface)):
        if landinix < surface[i][0] < landendx:
            if surface[i][1] > maxcaveheight:
                maxcaveheight = surface[i][1]
else:
    for i in range(len(surface)-1):
        if surface[i][1] > maxcaveheight:
            maxcaveheight = surface[i][1]

phase = 1

# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]

    # Phase 1 We go vertically up to the heiht of the top of the cave
    if phase == 1:
        if y < maxcaveheight+400:

            if opencave == "left": # Not straight acces to the cave
                if x > landendx:
                    rot = 5
                    power = 4
                elif x < landinix:
                    phase = 2
                else:
                    rot = 0
                    power = 4
            else:
                if x > descendpointx:
                    rot = 5
                    power = 4
                else:
                    phase = 2
        else:
            rot = 0
            power = 3

    # Phase 2 We level the horizontal speed for easy descend
    if phase == 2:

        if abs(h_speed) > 0:
            rot, power = levelmodule()
        else:
            phase = 3

    # Phase 3 We descend slowly until the adequate angle to the landing area (45º)
    if phase == 3:

        tan_angle = (abs(x - (landendx + landinix)//2))/(y-(landiniy))

        if 0.8 < tan_angle < 1:
            phase = 4
        else:
            rot, power = verticaldescend()
    
    # Phase 4 We follow incline descend towards the border of the landing area 
    if phase == 4:

        if opencave == "right":
            direction = 1
            if x <= landendx: phase = 5
        else:
            direction = -1
            if x >= landinix: phase = 5
        
        rot = 10 * direction
        power = 4

    # Phase 5 We level the horizontal speed for easy descend
    if phase == 5:

        if abs(h_speed) > 0:
            rot, power = levelmodule()
        else:
            phase = 6
        
    # Phase 6 We descend
    if phase == 6:

        rot, power = verticaldescend()

    print(phase, file=sys.stderr)
    print (rot, power)
