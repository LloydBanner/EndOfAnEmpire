import backend
import sys

class commandLineInterface:
    def __init__(self):
        self.table = backend.PlayingTable()

    def begin(self):
        choice = self.newGameOrLoad()
        if choice == "new":
            side = self.chooseSide()
            self.table.createGame(side)

        self.turnSequence()
            
    def newGameOrLoad(self):
        answered = False
        while True != answered:
            r = raw_input("Would you like to start a new Campaign (new) or load a Campaign (load)? ")
            if r == "new":
                answered = True
                return "new"
            elif r == "load":
                answered = True
                return "load"

    def chooseSide(self):
        sides = self.table.returnSideOptions()
        toPrint = "Select a side from: "
        for side in sides:
            if side != sides[-1]:
                toPrint += side + ", "
            else:
                toPrint = toPrint[0:-2]
                toPrint += " and " + side + ": "
        
        answered = False
        while True != answered:
            r = raw_input(toPrint)
            if r in sides:
                answered = True
                return r

    def turnSequence(self):
        currentMap = self.table.returnGalaxyMap()
        self.displayUserFriendlyMap(currentMap)

    def displayUserFriendlyMap(self, aMap):
        for row in aMap:
            toPrint = ""
            for sector in row:
                if not sector:
                    toPrint += " "
                elif len(sector) > 1:
                    for idVal in sector:
                        if idVal[0:6] == "Planet":
                            owner = self.table.getPlanetOwner(idVal)
                            if owner != "none":
                                toPrint += owner[0].upper()
                            else:
                                toPrint += "U"
                        else:
                            ownersEqual = True
                            firstOwner = ""
                            for thing in sector:
                                if firstOwner == "":
                                    firstOwner = thing.side
                                elif firstOwner != thing.side:
                                    ownersEqual = False

                            if ownersEqual:
                                toPrint += firstOwner[0].lower()
                            else:
                                toPrint += "x"
                else:
                    if sector[0][0:6] == "Planet":
                        owner = self.table.getPlanetOwner(sector[0])
                        if owner != "none":
                            toPrint += owner[0].upper()
                        else:
                            toPrint += "U"
                    else:
                        owner = sector[0].side()
                        toPrint += owner[0].lower()
                        
            print(toPrint)
    

start = commandLineInterface()
start.begin()
            
        
            
        
