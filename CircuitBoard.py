# 10/15/17
# Morgan Sorbaro
# Circuit board CSP Class. Which allows us to solve the Circuit board
import random
from BackTrackingAlgo import Backtrack_Search

# This is the main class which contrains the Corcuit CSP data and methods needed by the class for back tracking
class Circuit_CSP():


    #The circuit class holds:
    #  the domain (potential locations for the piece (its left bottom corner)): (x, y) tuple
    #  the variables (potential peices- letters): ("letter", width_of_piece, height_of_width) tuple
    #  the constraints (the neighbor pairs and their potential values)" ((x1, y1), (x2, y2)) tuple of tuples
    def __init__(self):


        self.CircuitX = 10  #X width of circuit board
        self.CircuitY = 3   #Y width of circuit board

        #domain: (x, y) all coordinates
        self.domain= self.createDomain()

        #each piece and their width and height in a list
        self.variables = [("a", 3, 2), ("b", 5, 2), ("c", 2, 3), ("e", 7, 1)]

        #constraints mappying a peice pair to a set of potential double tuples for location
        self.constraints = self.create_constraints()

        #count ofr nodes to see efficiency of heuristics
        self.count = 0

    #returns the domain of the CSP./ Domain being (x, y) potential coordinates
    def getdomain(self):
       return self.createDomain() #use domain creting function

    #returns a map from tuple or pieces next to each other to set of double touples of where they can be
    def create_constraints(self):

        #empty dictionary which will be full of a variable and the set of all the variables it can be
        letters_to_potentail_locations = {}

        #go through all the varialbes
        for var in self.variables:
            #use the varialbe tuple first part (the letter) and map it to the set of
            # locations it can be with its x, y from the tuple
            letters_to_potentail_locations[var[0]] = self.create_set(var[1], var[2])

        #epty constraint dictionary which will be returned eventually
        constraint = {}

        #loop through varialbes the first time
        for first_var in self.variables:
            #loop through variables a second time
            for second_var in self.variables:
                #check to make sure they are not equal and call method to check that this is not in the constraints already
                if first_var != second_var and self.const(constraint, first_var[0], second_var[0]):
                    #add the constraint of the first and second variables as key to set of poetntial locations between both of the variables
                    constraint[(first_var, second_var)] = self.make_match(letters_to_potentail_locations[first_var[0]], letters_to_potentail_locations[second_var[0]], first_var[1], first_var[2], second_var[1], second_var[2])

        #return answer
        return constraint

    #Helper method to create the constraints that takes the constraints so far and the two variables adding
    def const(self, constraint_so_far, first, second):
        #loops through all the constraints so far
        for constraint in constraint_so_far:
            #if there is a tuple with both first and second already then do not keep going in constrain method, return false
            if first in constraint and second in constraint:
                return False

        return True #otherwise Return True


    #make mathch takes two peices and their set of potential coordiantes and sees where the peices will work together
    #also takes the width (x_tot) and height (y_tot) of each peice (first/second)
    #returns a set of tuple pairs that show the two x y coordinates ex ((x1, y1), (x2,y2))
    def make_match(self, first_var_potential_coordinates, second_var_potential_coordinates, first_x_tot, first_y_tot, second_x_tot, second_y_tot):
        #final list of tuples going to be returned
        returnlist = {()}

        #for the coordinates in the potential first coordiantes
        for a_coordinate in first_var_potential_coordinates:
            #for all the coordiantes in the second list, compare to the A ones and see if they work together
             for b_coordinate in second_var_potential_coordinates:

                #make the conditional shorter with short variables
                #x and y of first(A) and second(B) values
                bx = b_coordinate[0]
                ax = a_coordinate[0]
                by = b_coordinate[1]
                ay= a_coordinate[1]

                #this large conditional checks to see if the coordinates fit either to the left, right or completely above without touching echother and if so adds the coordiantes
                if (bx >= ax + first_x_tot  or ax >= bx + second_x_tot) and (by <= ay + first_y_tot or ay <=by + second_y_tot) or ((by >= ay + first_y_tot or ay >= by + second_y_tot)):
                    returnlist.add(((a_coordinate[0], a_coordinate[1]),(b_coordinate[0], b_coordinate[1])))

        #remove the first empty thing needed to initialize the set
        returnlist.remove(())

        #return the set
        return returnlist


    #metod returns all the possible solutions for the domain
    def createDomain(self):
        #creates the set, starts it empty
        possible_solutions = {()}

        #go through all the x locations in the size of the board
        for x in range(0, 10):
            #go through all the y in the sizes of the board
            for y in range(0, 3):
                #add the x, y as a possible solution
                possible_solutions.add((x,y))

        #remove the empty tuple needed to initalize
        possible_solutions.remove(())

        return possible_solutions #return andwer

    #creates a set of potential solutions with the circuit board size for a particular peice
    #takes the piece width (x_size) and height (y_size)
    def create_set(self, x_size, y_size):
        #list of coordinates
        currgroup = []

        #go through x potentail values taking into account size
        for x in range(0, self.CircuitX - x_size+1):
            #go through y potential values taking into account size
            for y in range(0, self.CircuitY - y_size +1):
                #add the coordinate to the list
                currgroup.append((x,y))

        return currgroup #return the list of potential sets

    #determines if the assignment is complete
    #the assignment is complete if the length of the assignment is the length of variables
    #return this statement to return whether true or false
    def assignment_complete(self,assignment, CSP):
        return len(assignment) == len(CSP.variables)


    #Select var is my dumb heuristic.
    #randomly chooses a variable from the CSP
    def select_var(self, CSP):
        return random.choice(CSP.variables)

    #checks if the var/value is consistance with the assignment so far
    def is_consistant(self, var, value, assignment, CSP):
        #Go through all things assigned already
        for a in assignment:
            #if that assignment is in the constraints with the current variable
            if (a, var) in CSP.constraints:
                #Check if the color combination is a potential for this pair
                if ((assignment[a], value) not in CSP.constraints[(a, var)]):
                    return False

            #must reverse pair and do the same thing here to make sure border wasnt initialized other way
            if (var, a) in CSP.constraints:
                if (value, assignment[a]) not in CSP.constraints[(var, a)]:
                    return False

        return True #false never happened to must be true

    def printCircuit(self):
        #get the result back
        result = Backtrack_Search(self)

        #create empty board
        board = []

        #for the height
        for h in range(0, self.CircuitY):
            row = []
            #and for the width
            for w in range(0, self.CircuitX):
                row.append(".") #add a dot
            board.append(row) #add the row

        #creates a 2D array list this made of lists
        # [
        #[".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        #[".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        #[".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        # ]

        #now look at the results
        for piece in result:

            #create many varaibles to make naming easier
            letter = piece[0] #letter of peice
            width = piece[1]  #width of piece
            height = piece[2] #height of piece

            start_x = result[piece][0] #where result says bottom left corner is in x direction
            start_y = result[piece][1] #where result says bottom left corner is in y direction

            #loop through the board starting at the start location x up to the piece width
            for x in range(start_x, start_x+width):
                #loop through starting at the start y location up till the peice height
                for y in range(start_y, start_y+ height):
                    #add the letter to that location on the board
                    board[y][x] = letter

        #print the amount of nodes
        print("NODES: " + str(self.count))

        #print the results
        print(result)

        #print the board
        for i in range(0, len(board)):
            print(board[i])


#run the code and have the good stuff print
Circuit_CSP().printCircuit()

