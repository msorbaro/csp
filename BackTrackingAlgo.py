#BACK TRACK ALGORITHM AND HELPER METHODS
#Morgan Sorbaro
#10/15/17


#This is the method that origioanlly gets called
def Backtrack_Search(CSP):
    #calls the other main backtracking method
    return backtrack({}, CSP)

#main back track method like the psuedo code from the book
#takes the assignment and then the CSP
#calls many helper methods from the CSP calsses and also the functions bellow
def backtrack(assignment, CSP):


    #update the count. Need to keep track for nodes just for heuristic evaluation
    CSP.count = CSP.count + 1

    #Check to see if the assigment is complete, if it is, return it! We done :) !
    if CSP.assignment_complete(assignment, CSP):
        return assignment

    #get the next variable.
    ####***** CAN CHANGE HUERISTIC EASILY. DO THAT HERE ********
    var = LCV(CSP, assignment)

    #loop through all the values in the the domain values (which is just the domain)
    for value in domain_values(var, assignment, CSP):

        #Check to see if the var and value for the assignment works with the current assignment
        if CSP.is_consistant(var, value, assignment, CSP):

            #if it works, reassign this value
            assignment[var] = value

            #inference here and if it is good (and returns true) keep going

            inferences = inference(CSP, var, value, assignment)
            if inferences != False:

                #then continue to back track because this path is working well
                result = backtrack(assignment, CSP)
                #if result is doing good, rteturn the result (aka assignment)
                if result != None:
                    return result

                del assignment[var] #delete this for consistency sake

    #return none bcz made it to the end and nothing happned
    return None


# just return the domain
def domain_values(var, assignment, CSP):
    return CSP.domain


#This is the MRV heuristic. Takes the assignment and the CSP and returns the variable with the most constraints
def MRV(CSP, assignment):
    #dictionary going to map the varialbes to theria mount of constraints
    dict = {}

    #loop through all the varaibles
    for var in CSP.variables:
        #if the variable is not in assignment (still could be assigned we are interested)
        if var not in assignment:
            #loop through the constraints again to compare the var above to neighbor
            for constraint in CSP.constraints:

                #if the variable is in constraint
                if var in constraint:
                    #get the other one in the tuple
                    if constraint[0] == var:
                        other = constraint[1]
                    else:
                        other = constraint[0]

                    #if the other one is in the assignment (aka other is something so var has a constraint)
                    if other in assignment:
                        #increment var if it does exist already or add it to dictionary if it does not
                        if var in dict:
                            dict[var] = dict[var] + 1
                        else:
                            dict[var] = 1

    #if the length of the dictionary is 0 becuae nothing was added because they all have no constraints
    if len(dict) == 0:
        #loop through varialbes
        for var in CSP.variables:
            #if variable is not assigned, just return that
            if var not in assignment:
                return var

    #we want to find the smallest value from the dictionary before
    value = -100 #dict score
    move = None #move associated with it

    #loop thorugh dictionary
    for d in dict:
        #if dictoinary of the var value is greater than the current value (has more constraints)
        if dict[d] > value:
            value = dict[d] #reset value
            move = d #keep track of what var gave that result

    return move #greatest value move/variable

#LCV Heuristic
def LCV(CSP, assignment):
    #create dictionary which will match variables to it's score (total amount of options the neighbors have if this move is made)
    dict = {}

    #loop through varaibles
    for var in CSP.variables:
        #also loop through constraints
        for constraint in CSP.constraints:
            #empty set going to be full of the domain (aka colors for map problem)
            colors = {}
            #if the variable is in the constraint
            if var in constraint:
                # we get the neighbor for the varialbe
                if constraint[0] == var:
                    neighbor = constraint[1]
                else:
                    neighbor = constraint[0]

                #loop through the constraints again
                for c in CSP.constraints:
                    #check to see if the neighbor is there
                    if neighbor in c:
                        #find the neighbors other person
                        if c[0] == neighbor:
                            other = c[1]
                        else:
                            other = c[0]
                        #if the neighbor's neighbor is in assigment then we add the color the the color set
                        if other in assignment:
                            colors[assignment[other]] = ""

                #now look at hte domain of the CSP (go through each color)
                for d in CSP.domain:
                    #if the current domain is not in colors
                    if d not in colors:
                        #if the current varaible is also not in the dictionary with variables and the scores, add the this as initial value
                        if var not in dict:
                            dict[var] = len(CSP.domain) - len(colors) - 1
                        #otherwise increment the values
                        else:
                             dict[var] = dict[var] + len(CSP.domain) - len(colors) -1

    #if the dictionary length is 0 - choose a random unchoosen one
    if len(dict) == 0:
        #loop throgh variables
        for var in CSP.variables:
            #if it hasnt been assigned yet just choose that
            if var not in assignment:
                return var

    #want to calculate teh total score because if was always 0 because all asigned, have to find a random one
    total = 0
    #loop through and add whole total of dictionary
    for d in dict:
        total = total + dict[d]
    #if whole total is 0 (need to try a new region)
    if total ==0:
        #loop through variable
        for var in CSP.variables:
            #return the variable if not in assignment
            if var not in assignment:
                return var

    #start the origional value and move as not really values
    value = -100
    move = None

    #loop through dictionary, if the value of a new variavle is greate, store that one
    for d in dict:
        #if the variable vals is greater and not already assigned
        if dict[d] > value and d not in assignment:
            #update storing variables
            value = dict[d]
            move = d
    #return final move
    return move

#method that checks to see if the future path down this branch is going to work out in the future
#like the algo in the book
def inference(CSP, var, value, assignment):
    #starting queue that we will be adding constraints to
    queue=[]

    #loop through CSP
    for constraint in CSP.constraints:
        #add each contraint tuple to the queue
        queue.append(constraint)

    #dictionary for domains
    d = {}

    #loop through
    for var in CSP.variables:
        #if assigned, add that value to domain
        if var in assignment:
            d[var] = {assignment[var]}
        #otherwise add all values
        else:
            d[var] = CSP.getdomain()


    #loop through varibles -> goal to create dictionary of all current domains
    for var in CSP.variables:
        #loop through constraints
        for constraint in CSP.constraints:
            #if constraint ocntains var
            if var in constraint:

                #find which var's neighbor is
                if constraint[0] == var:
                    neighbor = constraint[1]
                else:
                    neighbor = constraint[0]

                #if neighbor assigned
                if neighbor in assignment:
                    #if the color of neighbors is in d[var]
                    if assignment[neighbor] in d[var]:
                        #remove
                        d[var].remove(assignment[neighbor])

    #while size queue > 0
    while len(queue) > 0:

        #remove first tuple from Q
        arc = queue.pop(0)

        #revise and get boolean and new domain
        bool, d = revise(arc[0], arc[1], d)

        #boolean being true means continue down this path
        if bool:
            #if size of d is 0, return false
            if len(d[arc[1]]) <= 0:
                return False

            #loop through constraints
            for constraint in CSP.constraints:
                #if constraint .contains Xi and doesnt contian xj
                if arc[0] in constraint and arc[1] not in constraint:
                    #find neightbore
                    if constraint[0] == var:
                        neighbor = constraint[1]
                    else:
                        neighbor = constraint[0]
                    #add (neighbor, xi) to queue
                    queue.append((neighbor, arc[0]))

    return True #return True all happened well amde it to end

#herlper method that returns true if revised the set adn the domain
#also like psuedo code from book
def revise(curr, neighbor, d):
    revised = False #boolean to be changed and also returned

    #for each color in D[varx1]
    colors_curr_can_be = list(d[curr])


    for color in colors_curr_can_be: #going through each option in the list of color options
        #get the neightbors colors
        colors_neighbor_can_be = d[neighbor]
        #if the first color is there
        if color in colors_neighbor_can_be:
            #remove color from D[var2]
            colors_neighbor_can_be.remove(color)

            #if the length is <= 0
            if len(colors_neighbor_can_be) <= 0:

                # if the side is now 0, remove color from D[varx1]
                if color in d[curr]:
                    d[curr].remove(color)
                    revised = True #change revised

                #add next color
                colors_neighbor_can_be.add(color)

        #revise d
        d[neighbor] = colors_neighbor_can_be

    #return results
    return revised, d