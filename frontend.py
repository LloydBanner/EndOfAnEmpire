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
        playing = True
        while playing:
            currentMap = self.table.returnGalaxyMap() 
            self.displayUserFriendlyMap(currentMap)
            currentPlayer = self.table.getNextPlayer()
            endOfTurn = False
            if currentPlayer.isHuman == True:
                while not endOfTurn:
                    position = raw_input("Select a sector where you would like to perform an action or end your turn (end): ")
                    if position == "end":
                        endOfTurn = True
                    else:
                        contentSector = self.findSector(position)
                        if contentSector == "notASector":
                            print("Invalid Selection, please try again")
                        else:
                            sectorSelection = True
                            while sectorSelection:
                                contentSector = self.findSector(position)
                                print(contentSector)
                                r = raw_input("Type a number to select the thing in the sector or exit (0): ")
                                if unicode(r, "utf-8").isdecimal():
                                    num = int(r)
                                    if num != 0:
                                        if num-1 < len(contentSector):
                                            self.activate(contentSector[num-1], currentPlayer, position)
                                    else:
                                        sectorSelection = False
                                else:
                                    print("Invalid selection")
            else:
                print("AI turn")

    def activate(self, galacticObject, currentPlayer, position):
        if galacticObject[0:6] == "Planet":
            planet = self.table.galaxy.getPlanet(galacticObject)
            print(planet.name)
            print("Controlled by: " + planet.owner)
            print("Population: " + str(planet.population))
            print("Resource Production: " + str(planet.resources))
            print("Credit Production: " + str(planet.creditProduction))
            if planet.owner == currentPlayer.side:
                r = raw_input("Would you like to create something on this planet? (yes/no): ")
                if r == "yes":
                    stillBuying = True
                    while stillBuying:
                        print("Player credits: " + str(currentPlayer.credits))
                        print("1) Squadron: " + self.table.galaxy.costFleet)
                        print("2) Battalion: " + self.table.galaxy.costBattalion)
                        r = raw_input("Number for your selection (0 exit): ")
                        if r == "1":
                            result = self.table.purchaseSquadron(currentPlayer, self.getNumPos(position))
                            if result:
                                print("Purchase successful!")
                            else:
                                print("Insufficient funds!")
                        elif r == "2":
                            result = self.table.purchaseBattalion(currentPlayer, self.getNumPos(position))
                            if result:
                                print("Purchase successful!")
                            else:
                                print("Insufficient funds!")
                        elif r == "0":
                            stillBuying = False
                        
                        
        else:
            fleet = self.table.getFleet(galacticObject)
            print(fleet.idVal)
            print("Owned by: " + fleet.side)
            print("Number of battalions: " + str(fleet.numBattalions))
            print("Number of squadrons: " + str(fleet.numSquadrons))
            print("Number of heros: " + str(fleet.numHeros))
            print("Number of infiltration teams: " + str(fleet.numInfiltration))
            print("Moved this turn: " + str(fleet.moved))
            selection = True
            while selection:
                r = raw_input("Combine this fleet with another in the sector? (yes/no): ")
                if r == "yes":
                    fleetSelection = self.selectOtherFleets(galacticObject, currentPlayer, position)
                    if fleetSelection != "none":
                        self.table.combineFleets(galacticObject, fleetSelection)
                        print("Fleets combined")
                elif r == "no":
                    selection = False
                else:
                    print("Invalid selection")

            selection = True
            while selection:
                r = raw_input("Split this fleet in to smaller fleets? (yes/no): ")
                if r == "yes":
                    self.splitFleet(galacticObject)
                elif r == "no":
                    selection = False
                else:
                    print("Invalid selection")

            if fleet.moved == False:
                selection = True
                while selection:
                    r = raw_input("Move this fleet? (yes/no): ")
                    if r == "yes":
                        self.moveFleet(galacticObject)
                        selection = False
                    elif r == "no":
                        selection = False
                    else:
                        print("Invalid selection")
            

    def selectOtherFleets(self, dontShow, player, pos):
        selectionList = []
        for galacticObject in self.findSector(pos):
            if "Fleet" == galacticObject[0:5]:
                if self.table.getFleet(galacticObject).side == player.side:
                    if galacticObject != dontShow:
                        selectionList += [galacticObject]
        print(selectionList)
        selecting = True
        while selecting:
            r = raw_input("Type a number to select the fleet you wish to combine with (0 to exit): ")
            if r == "0":
                print("Combination cancelled")
                selecting = False
                return "none"
            elif int(r)-1 < len(selectionList):
                return selectionList[int(r)-1]
            else:
                print("Invalid selection!")

    def splitFleet(self, fleet):
        fleetContent = self.table.getFleet(fleet)
        battalions = 0
        squadrons = 0
        heros = 0
        infiltration = 0
        select = True
        while select:
            print("Battalions in current fleet = " + str(fleetContent.numBattalions))
            r = raw_input("How many battalions would you like to move to the new fleet? ")
            if int(r) <= fleetContent.numBattalions:
                battalions = int(r)
                select = False
            else:
                print("Invalid selection")

        select = True
        while select:
            print("Squadrons in current fleet = " + str(fleetContent.numSquadrons))
            r = raw_input("How many squadrons would you like to move to the new fleet? ")
            if int(r) <= fleetContent.numSquadrons:
                squadrons = int(r)
                select = False
            else:
                print("Invalid selection")

        select = True
        while select:
            print("Heros in current fleet = " + str(fleetContent.numHeros))
            r = raw_input("How many heros would you like to move to the new fleet? ")
            if int(r) <= fleetContent.numHeros:
                heros = int(r)
                select = False
            else:
                print("Invalid selection")

        select = True
        while select:
            print("Infiltration teams in current fleet = " + str(fleetContent.numInfiltration))
            r = raw_input("How many Infiltration teams would you like to move to the new fleet? ")
            if int(r) <= fleetContent.numInfiltration:
                infiltration = int(r)
                select = False
            else:
                print("Invalid selection")

        dontMake = False
        if infiltration == fleetContent.numInfiltration:
            if heros == fleetContent.numHeros:
                if squadrons == fleetContent.numSquadrons:
                    if battalions == fleetContent.numBattalions:
                        dontMake = True
                        print("No new fleet created, can't move all content of old fleet")

        if dontMake != True:
            fleetContent.numBattalions = fleetContent.numBattalions - battalions
            fleetContent.numSquadrons = fleetContent.numSquadrons - squadrons
            fleetContent.numInfiltration = fleetContent.numInfiltration - infiltration
            fleetContent.numHeros = fleetContent.numHeros - heros
            self.table.addPlayerFleet(fleetContent.side, fleetContent.xPos, fleetContent.yPos, battalions, squadrons, heros, infiltration)   
            print("Fleet Split")
            
    def moveFleet(self, fleetName):
        print("Fleet can move up to 5 sectors")
        selecting = True
        while selecting:
            position = raw_input("Select a sector to move to: ")
            contentSector = self.findSector(position)
            if contentSector == "notASector":
                print("Invalid Selection, please try again")
            else:
                newXYPos = self.getNumPos(position)
                newXPos = newXYPos[0]
                newYPos = newXYPos[1]
                fleet = self.table.getFleet(fleetName)
                xDiff = abs(newXPos-fleet.xPos)
                yDiff = abs(newYPos-fleet.yPos)
                totalDiff = xDiff + yDiff
                if totalDiff == 0:
                    print("Fleet holding same position")
                    selecting = False
                if totalDiff <= 5:
                    self.table.updateFleetPosition(fleetName, newXPos, newYPos)
                    print("Fleet moved")
                    selecting = False
                else:
                    print("That's too far away")
                        
                
            
                
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
                                elif firstOwner != fleet.side:
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

    def findSector(self, userInput):
        currentMap = self.table.returnGalaxyMap() 
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = int(userInput[1:])
        letter = userInput[0]
        if num <= len(currentMap):
            width = len(currentMap[0])
            if letter in alphabet[:width]:
                numLetter = 0
                for char in alphabet:
                    if char == letter:
                        break
                    else:
                        numLetter += 1
                return currentMap[num-1][numLetter]
        return "notASector"

    def getNumPos(self, userInput):
        currentMap = self.table.returnGalaxyMap() 
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = int(userInput[1:])
        letter = userInput[0]
        if num <= len(currentMap):
            width = len(currentMap[0])
            if letter in alphabet[:width]:
                numLetter = 0
                for char in alphabet:
                    if char == letter:
                        break
                    else:
                        numLetter += 1
                return (num-1, numLetter)
        return "notASector"
        
    

start = commandLineInterface()
start.begin()
            
        
            
        
