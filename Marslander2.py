import sys

MAX_H_SPPED = 5  # accepted horizontal speed

surface = []
# the number of points used to draw the surface of Mars.
surface_n = int(input())  

for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]
    surface.append([land_x, land_y])

# Calculating the landing area
for i in range(len(surface)-1):
    if surface[i][1] == surface[i+1][1]:
        landinix, landiniy = surface[i]
        landendx, landendy = surface[i+1]

# Caluclating X points of interest
landingsize = landendx - landinix   # Size of landing platform
xlanding = (landinix+landendx)//2   # Mean point of landing platform

# game loop
while True:
    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [int(i) for i in input().split()]

   
    # Find approach phase:
    #   Phase 1: Initial approach towards the landing area. Keep module correct h_ and v_speed  
    #   Phase 2: Leveling the module. Change to Phase 2 is defined by a distance to 
    #            the landing point, taking into account the horizontal speed
    #   Phase 3: Touchdown. From intercept
    
    # Calculates distance from landing point to change to Phase 2 depending on h_speed
    distance = (landingsize // 2) + abs(h_speed)*5 
    print("dist="+str(distance), file=sys.stderr)

    if x < xlanding-distance or x > xlanding+distance:
        
        Phase = 1 # Initial approach
        
        if x < xlanding:
            direction = -1
        else:
            direction = 1
       
        if abs(h_speed) < 50:
            rot = direction*21
            power = 4
        elif abs(h_speed) > 70:
            rot = direction*-21
            power = 4
        else:
            if v_speed < -1:
                rot = 0
                power = 4
            else:
                rot = 0
                power = 3
        
    else:
        # now we are over the landing area. We have to control horizontal speed
        if abs(h_speed) > MAX_H_SPPED:
        
            Phase = 2 # Leveling the module

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
            
            power = 4

        else:
        # if over the landing area and horizontal speed is controled.
        # We resume trajectory control

            Phase = 3 # Touchdown

            rot = 0        
            if abs(v_speed) >= 35:
                power = 4
            else:
                power = 3

    print(rot, power)
