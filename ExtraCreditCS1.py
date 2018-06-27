from BackTrackingAlgo import Backtrack_Search
import random

#extra credit CS1 class that solves the TA student problems
class ExtraCreditCS1_CSP():


    def __init__(self, filename):

        #list of people who say they do not like each other
        self.dislikes = []

        #reads in the names from a file
        self.list = self.readInFile(filename)

        #list of varialbes
        self.variables = self.createVariables(self.list)
        #list of domains
        self.domain = self.createDomain(self.list)
        #lists of Tas and students to seperate them
        self.TA = []
        self.Students = []

        #constraints
        self.constraints = self.createConstraints(self.list)
        #count bcz needed
        self.count = 0


    #Reads in the schedule file to make the schedule
    def readInFile(self, filename):
        file = open(filename, "r") #open file

        #put the file into the correct file data structure needd
        finalList = []


        #string manipulation through the file
        for line in file:
            mylist = line.split(",") #split times by comma
            name = mylist[0]
            mylist.remove(name)
            times = {""}
            for w in mylist:
                if "|" in w:
                    removebar= w.split("|")
                    self.dislikes.append((name, removebar[1].strip()))
                    times.add(removebar[0].strip())
                else:
                    times.add(w.strip())  #add all the words to the times set
            times.remove("")

            finalList.append((name, times)) #add name of person and the times into a list of tuples

        return finalList

    #create the constraints which are between people and the values they could be
    def createConstraints(self, list):

        #dictionary that matches each person to the right times that they are availible
        nameToTime = {}
        for person in list:
            nameToTime[person[0]] = person[1]

        #create the TA and students list
        TAs = []
        students = []
        for name in nameToTime:
            if "*" in name: #if there is a * it is a TA
                TAs.append(name)
            else: #othewise a student
                students.append(name)

        constraint = {} #going to be the constraint

        #loop through every combination of TAs and Students
        for ta in TAs:
            for student in students:
                #create the set from merging both of them as constraints
                constraint[(student, ta)] = self.mergeListToSet(nameToTime[student], nameToTime[ta])

        #set these for instance varialbes
        self.TA = TAs
        self.Students = students

        return constraint

    #combines the student times and ta Times and sees when they are in common
    def mergeListToSet(self, studentTimeList, taTimeList):
        returnSet = {""}
        for studentTime in studentTimeList:
            for taTime in taTimeList:
                if taTime == studentTime and taTime not in returnSet: #if they are equal and do not already exist than it is a good time
                    returnSet.add((taTime, studentTime))
        returnSet.remove("")
        return returnSet

    #lopp through lsit created reading in files nad add all the poeple to a list
    def createVariables(self, list):
        l = []
        for person in list:
            l.append(person[0])
        return l

    #loops thorugh all the specific person's times adds them to the domain test
    def createDomain(self, list):
        times = {""}
        for person in list: #each person
            for time in person[1]: #each time
                if time not in times: #if the time isnt already there add it
                    times.add(time)
        times.remove("")
        return times

    #checks if all the variavles have been assigned
    def assignment_complete(self ,assignment, CSP):
        return len(assignment) == len(self.variables)

    # returns the domain which recreates it
    def getdomain(self):
        return self.createDomain(self.list)

    # checks if the var/value is consistance with the assignment so far
    def is_consistant(self, name, time, assignment, CSP):

        #go through each person
        for person in self.list:
            #if the current person name who was there is in the person
            if name in person:
                #if the current time is not one of the options
                if time not in person[1]:
                    return False

        #checks to make sure that there are no dislikes between people
        for dislikepair in self.dislikes:
            #if the curr name is someone who dislikes someone else
            if name in dislikepair:

                #find other value who dislikes that person
                if dislikepair[0] == name:
                    other = dislikepair[1]
                else:
                    other = dislikepair[0]

                #if that other person has been asigned already
                if other in assignment:
                    if time == assignment[other]:
                        return False #return false, cant have the people together

        bool = False
        #if name isnt TA
        if name not in self.TA:
            #make sure there is a TA preset in the potential place it will be inserted
            for person in assignment:
                if person in self.TA: #if there is
                    if assignment[person] == time:
                        bool = True #all okay
            return bool
        return True

    #just prints everything out in a better order
    def print_nice(self):
        result = Backtrack_Search(self) #call the main method
        time_ta = []
        for name in result: #get list of TA and sections
            if "*" in name:
                time_ta.append((name, result[name]))

        for section in time_ta:
            print(str(section)) #print the TA and time
            for name in result:
                if result[name] == section[1]:
                    print(name) #print all the popel in that section





ExtraCreditCS1_CSP("sectionData").print_nice()
