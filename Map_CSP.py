# 10/15/17
# Morgan Sorbaro
# Map CSP Class. Which allows us to solve the Australia Map Problem

from BackTrackingAlgo import Backtrack_Search
import random

# This is the main class which contrains the Map CSP data and methods needed by the class for back tracking
class Map_CSP():

    #The map class holds:
    #  the domain (potential colors)
    #  the variables (potential countries)
    #  the constraints (the neighbor pairs and their potential values)
    def __init__(self):
        #Color: r= 0 g = 1 = b = 2
        self.domain= {0, 1, 2}

        #count for nodes to see efficiency of heuristics
        self.count = 0

        #Variables aka countries: wa = 0, nt = 1 , SA = 2, Q = 3 NSW =4  V=5 T = 6
        self.variables = [0, 1, 2, 3, 4, 5, 6]

        #Constraints first anitialized with an empty set.
        #all the constraints are pairs that are neightbors and then their potential values
        self.constraints = {(0, 1): {}, (0, 2): {}, (2, 1): {}, (1, 3): {}, (2, 3): {}, (3, 4): {}, (2, 4): {}, (2, 5): {}, (4, 5): {}}

        #Add all the potential values to the constraint. Every combination of rgb to start
        for constraint in self.constraints:
            self.constraints[constraint] = {(0, 1), (0, 2), (2, 1), (2, 0), (1, 0), (1, 2),}

    #determines if the assignment is complete
    #the assignment is complete if the length of the assignment is the length of variables
    #return this statement to return whether true or false
    def assignment_complete(self ,assignment, CSP):
        return len(assignment) == len(self.variables)

    #Select var is my dumb heuristic.
    #randomly chooses a variable from the CSP
    def select_var(self, CSP):
        return random.choice(self.variables)

    #returns the domain which are the colors aka {0, 1, 2}
    def getdomain(self):
        return {0, 1, 2}

    #checks if the var/value is consistance with the assignment so far
    def is_consistant(self, var, value, assignment, CSP):
        #Go through all things assigned already
        for a in assignment:
            #if that assignment is in the constraints with the current variable
            if (a, var) in self.constraints:
                #Check if the color combination is a potential for this pair
                if ((assignment[a], value) not in self.constraints[(a, var)]):
                    return False #if not reutrn false

            #must reverse pair and do the same thing here to make sure border wasnt initialized other way
            if (var, a) in CSP.constraints:
                if (value, assignment[a]) not in self.constraints[(var, a)]:
                    return False

        return True #no false, so much be ok

    #changes the 1 and 0s back into lettesr
    def print_nice(self):
        result = Backtrack_Search(self)
        countries = ["wa", "nt" , "sa", "Q", "NSW", "V",  "T"]
        colors = ["r", "g", "b"]

        dic = {}
        for r in result:
            #uses the mpas above and the indexs to redo dictionary as lettesr
            dic[countries[r]] = colors[result[r]]
        print(dic)


#This is the line to get the result from backtracking and then print it

Map_CSP().print_nice()
