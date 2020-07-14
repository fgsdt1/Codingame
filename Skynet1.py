import sys
import math


class Skynet:

    def __init__(self, numnodes, numlinks, numgateways):

        self.size = numnodes
        self.numlinks = numlinks
        self.numgateways = numgateways
        self.gateways = []
        self.nodes = {_: Node(_) for _ in range(1,self.size+1)}

    def addLink(self, pair):

        # We assign a weight to the link. For this Skynet scenario it will always be 1
        self.nodes[pair[0]].links[pair[1]] = [pair[1], 1]
        self.nodes[pair[1]].links[pair[0]] = [pair[0], 1]
        return

    def addGateway(self, gate):

        self.gateways.append(gate)
        return

    def shortestPaths(self, gate):

        # We create a dictionay of nodes (tablenodes) with a double value:
        #       - The size of the path (initialized to infinit) and the optimal path ("" to start with)
        # We also create a dictionary of visited nodes (visitednodes) where we keep the nodes not visited yet

        tablenodes = {}
        visitednodes = {}

        for node in self.nodes.keys():
            tablenodes[node] = [math.inf, ""]
            visitednodes[node] = False

        # We apply initial values to the gateway node
        tablenodes[gate] = [0, str(gate) + ";"]

        # We repeat the process while there are nodes in the visited dictionary
        while len(visitednodes) > 0:

            # We set the pointer to the next node with shorter path and that is still on the visited dict
            # We go through the dict. The first time it will select the gate node since it is the only one with value
            minnode = ""

            for node in visitednodes.keys():
                if minnode == "":
                    minnode = node
                else:
                    if tablenodes[node][0] < tablenodes[minnode][0]:
                        minnode = node

            # We delete the selected node from the visited dict
            del visitednodes[minnode]

            # We analyse all the links associated to the minimum distance node
            for link in self.nodes[minnode].links.keys():

                # We process only those nodes that have not been visited yet
                if link in visitednodes.keys():

                    # We calculate the distance: current distance to the node + the value of the link
                    # Note: Node class has been design so that it it can get different weights for the links.
                    # In this case it is always one but anyway we use the value from the object node.link
                    distance = tablenodes[minnode][0] + self.nodes[minnode].links[link][1]

                    # If the difference is lower than the one registered on the nodes table we update it.
                    if distance < tablenodes[link][0]:
                        tablenodes[link][0] = distance
                        # and update the path
                        tablenodes[link][1] = tablenodes[minnode][1] + str(link) + ";"

        # We exit the while loop if all the nodes have been visited. The table of nodes is now updated with all the
        # possible minimum paths. We return the node table.
        return tablenodes

    # Method to call the generic shortestpaths method and returns only the one we are interested in
    # In this case the path from the gate to the virus
    def shortestPath(self, gate, virus):

        tablenodes = self.shortestPaths(gate)
        return tablenodes[virus]

    def __str__(self):

        string = "Skynet size:" + str(self.size) + "\n\n"
        for node in self.nodes.values():
            string = string + str(node) + "\n"

        string = string + "\nSkynet Gateways: " + str(self.numgateways) + " => " + str(self.gateways)
        return string


class Node:

    def __init__(self, key):

        self.key = key
        self.links = {}

    def __str__(self):

        string = str(self.key) + " linked to: "
        for i in self.links:
            string = string + str(i) + ","

        return (string[:-1])




mySky = Skynet(4,4,1)

thelinks = [[1,2], [1,3], [2,4], [3,4]]
thegateways = [4]

for pair in thelinks:
    mySky.addLink(pair)

for gate in thegateways:
    mySky.addGateway(gate)

Virus = 1

print(mySky)

path = mySky.shortestPath(4,1)[1].split(";")[:-1]
print (path)
print (path[0]+" "+path[1])
