import sys
import re
from anytree import Node

filename = ""
startEl = ''
endFl = -1
endState = -1
validEndEls = list()

floors = -1
states = dict()

def getStates():
            
    # Find number of floors
    def findFloors(lines):

        floor = 0
        line = lines[floor]
        while line != "\n":

            floor += 1
            line = lines[floor]

        return floor

    with open(filename, "r") as file:

        lines = file.readlines()
        global floors
        floors = findFloors(lines)
        
        # Parsing states
        state = 1
        floor = floors
        for line in lines:

            line.strip()

            if floor == 0:

                #All floors have been parsed for this state, move to the next state
                state += 1
                floor = floors

            else:

                # First entry in new state, instantiate the state
                if (floor == floors):
                    states[state] = dict()

                # Check if any elevators are on this floor, if add them to this floor's dict
                elevators = re.findall(r'[A-Z]', line)
                if len(elevators) > 0:
                    states[state][floor] = elevators

                floor -= 1
            

def findElevatorPath():

    # Gets the elevators on a given floor at a give state
    def getElsOnFloor(floor, state):

        return states[state][floor]

    # Gets the floor of a given elevator at a given state
    def getFloorOfEl(elevator, state):

        floors = states[state]
        for floor in floors:

            for el in states[state][floor]:

                if el == elevator:

                    return floor
        
        return -1

    # Invalid End Floor or End State
    if endFl > floors or endFl < 1 or endState > len(states) or endState < 1:
        return

    try:

        if len(states[endState][endFl]) > 0:
            
            validEndEls = getElsOnFloor(endFl, endState)
            state = 1

            # Starting nodes
            parentNodes = list()
            # Variable list of nodes at each state
            # When loop ends, this list will contain all possible end nodes
            currElNodes = list()
            while state <= endState:

                # Add all elevators on starting floor to paths list
                if state == 1:

                    currEls = getElsOnFloor(getFloorOfEl(startEl, state), state)
                    for el in currEls:

                        n = Node(el)
                        parentNodes.append(n)
                        currElNodes.append(n)

                # For each path, check the new floor of the last elevator in that path
                # Add a node for staying on the same elevator
                # If there is another elevator on the same floor, append a new node for that elevator
                else:
                    
                    oldNodes = currElNodes
                    currElNodes = list()
                    for node in oldNodes:

                        el = node.name
                        floor = getFloorOfEl(el, state)
                        els = getElsOnFloor(floor, state)
                        for e in els:

                            n = Node(e, parent = node)
                            currElNodes.append(n)

                state += 1

            # Prints any valid paths
            for node in currElNodes:

                result = ""
                for vn in validEndEls:

                    currNode = node
                    # Check to see if any nodes in the list match a valid elevator for the end floor at the end time
                    # If they do, ascend the tree and append each elevator to the beginning of the result string
                    if node.name == vn:

                        result = currNode.name
                        while len(currNode.ancestors) > 0:
                            currNode = currNode.parent
                            result = currNode.name + result

                        print(result)

    except KeyError:

        # No elevator available on the End Floor and the End State
        return


if __name__ == "__main__":

    # Reading command line variables
    filename = sys.argv[1]
    startEl = sys.argv[2]
    destination = sys.argv[3]
    dashIndex = destination.find('-')
    endFl = int(destination[:dashIndex])
    endState = int(destination[dashIndex + 1])

    getStates()
    findElevatorPath()