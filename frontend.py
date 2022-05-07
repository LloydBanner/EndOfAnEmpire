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
        self.table.addPlayerFleet("empire", 1, 14, 1, 0, 0, 0) 
        self.table.addPlayerFleet("newRepublic", 20, 14, 1, 0, 0, 0) 
        self.table.addPlayerFleet("empire", 12, 12, 1, 0, 0, 0) 
        self.table.addPlayerFleet("empire", 10, 16, 1, 0, 0, 0)
        currentMap = self.table.returnGalaxyMap() 
        self.displayUserFriendlyMap(currentMap)

    def displayUserFriendlyMap(self, aMap):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        toPrint = "  |"
        betweenRows = "--+"
        for i in range(len(aMap[0])):
            toPrint += alphabet[i] + "|"
            betweenRows += "-+"
        print(toPrint)
        print(betweenRows)
        rowNum = 0;
        for row in aMap:
            rowNum += 1
            if len(str(rowNum)) == 1:
                toPrint = str(rowNum) + " |"
            else:
                toPrint = str(rowNum) + "|"
            sectorNum = 0
            for sector in row:
                if not sector:
                    toPrint += " "
                elif len(sector) > 1:
                    if sector[0][0:6] == "Planet":
                            ownersEqual = True
                            firstOwner = ""
                            for fleetName in sector[1:]:
                                fleet = self.table.getFleet(fleetName)
                                if firstOwner == "":
                                    firstOwner = fleet.side
                                elif firstOwner != fleet:
                                    ownersEqual = False

                            if ownersEqual:
                                toPrint += firstOwner[0].lower()
                            else:
                                toPrint += "x"
                    else:
                        ownersEqual = True
                        firstOwner = ""
                        for fleetName in sector:
                            fleet = self.table.getFleet(fleetName)
                            print(fleetName)
                            if firstOwner == "":
                                firstOwner = fleet.side
                            elif firstOwner != fleet:
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
                        fleet = self.table.getFleet(sector[0])
                        owner = fleet.side
                        toPrint += owner[0].lower()

                if row[sectorNum]:
                    currentSectorIsplanet = row[sectorNum][0][0:6]
                else:
                    currentSectorIsplanet = "no"
                if len(row) > sectorNum+1:
                    if row[sectorNum+1]:
                        nextSectorIsPlanet = row[sectorNum+1][0][0:6]
                    else:
                        nextSectorIsPlanet = "no"
                    if nextSectorIsPlanet == "Planet":
                        if currentSectorIsplanet == "Planet":
                            toPrint += "#"
                        else:
                            toPrint += "<"
                    elif currentSectorIsplanet == "Planet":
                        toPrint += ">"
                    else:
                        toPrint += "|"
                elif currentSectorIsplanet == "Planet":
                    toPrint += ">"
                else:        
                    toPrint += "|"
                sectorNum += 1
                        
            print(toPrint)
            print(betweenRows)
    

start = commandLineInterface()
start.begin()
            
        
            
        
