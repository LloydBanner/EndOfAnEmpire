import backend
import sys
import os

class commandLineInterface:
    def __init__(self):
        self.table = backend.PlayingTable()

    def begin(self):
        choice = self.newGameOrLoad()
        if choice == "new":
            side = self.chooseSide()
            self.table.createGame(side)
            self.turnSequence()
        elif choice == "load":
            notSelected = True
            while notSelected:
                r = raw_input("load: ")
                filesInSaves = os.listdir("saves/")
                filename = r + ".pkl"
                if filename in filesInSaves:
                    self.table = self.table.loadState(r)
                    notSelected = False
                else:
                    print("No save called: " + filename)
            self.resumeGame()

            
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

    def resumeGame(self):
        currentMap = self.table.returnGalaxyMap() 
        self.displayUserFriendlyMap(currentMap)
        currentPlayer = self.table.getCurrentPlayer()
        endOfTurn = False
        while not endOfTurn:
            position = raw_input("Select a sector where you would like to perform an action or end your turn (end): ")
            if position == "end":
                endOfTurn = True
            elif position == "save":
                r = raw_input("Save as: ")
                self.table.saveState(r)
                print("Save successful!")
            elif position == "load":
                notSelected = True
                while notSelected:
                    r = raw_input("load: ")
                    filesInSaves = os.listdir("saves/")
                    filename = r + ".pkl"
                    if filename in filesInSaves:
                        self.table = self.table.loadState(r)
                        notSelected = False
                    else:
                        print("No save called: " + filename)
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

        self.turnSequence()
    
    def turnSequence(self):
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
                    elif position == "save":
                        r = raw_input("Save as: ")
                        self.table.saveState(r)
                        print("Save successful!")
                    elif position == "load":
                        notSelected = True
                        while notSelected:
                            r = raw_input("load: ")
                            filesInSaves = os.listdir("saves/")
                            filename = r + ".pkl"
                            if filename in filesInSaves:
                                self.table = self.table.loadState(r)
                                notSelected = False
                            else:
                                print("No save called: " + filename)
                    elif position == "quit":
                        endOfTurn = True
                        playing = False
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
                print("AI turn: " + currentPlayer.side)
                while not endOfTurn:
                    self.doAIMove(currentPlayer, currentMap)
                    endOfTurn = True

    def doAIMove(self, currentPlayer, galaxyMap):
        for planet in self.table.galaxy.planets:
            if planet.owner == currentPlayer.side:
                planetSector = galaxyMap[planet.xPos][planet.yPos]
                noBattalions = True
                for galacticObject in planetSector:
                    print(galacticObject)
                    if "Fleet" == galacticObject[0:5]:
                        fleet = self.table.getFleet(galacticObject)
                        if fleet.side == currentPlayer.side:
                            print("Fleet has battalions; " + str(fleet.numBattalions))
                            if int(fleet.numBattalions) > 0:
                                print("already battalion")
                                noBattalions = False
                print(noBattalions)
                if noBattalions:
                    result = self.table.purchaseBattalion(currentPlayer, (planet.xPos, planet.yPos))
                    if result == True:
                        print("The " + currentPlayer.side + " purchased a battalion on " + planet.name)
           
        for planet in self.table.galaxy.planets:
            if planet.owner == currentPlayer.side:
                planetSector = galaxyMap[planet.xPos][planet.yPos]
                noSquadrons = True
                for galacticObject in planetSector:
                    if "Fleet" == galacticObject[0:5]:
                        fleet = self.table.getFleet(galacticObject)
                        if fleet.side == currentPlayer.side:
                            if int(fleet.numSquadrons) > 0:
                                noSquadrons = False
                if noSquadrons:
                    result = self.table.purchaseSquadron(currentPlayer, (planet.xPos, planet.yPos))
                    if result == True:
                        print("The " + currentPlayer.side + " purchased a squadron on " + planet.name)
                        self.checkForConflict(planet.xPos, planet.yPos, (planet.xPos, planet.yPos))

        tryMove = False
        initialFleets = currentPlayer.fleets
        for fleet in initialFleets:
            fleetSector = galaxyMap[fleet.xPos][fleet.yPos]
            possiblePlanet = fleetSector[0]
            if possiblePlanet[0:6] == "Planet":
                if self.table.getPlanetOwner(possiblePlanet) == fleet.side:
                    if self.isPlanetSafe(possiblePlanet):
                        if fleet.moved == False:
                            tryMove = True
            else:
                if fleet.moved == False:
                    tryMove = True

            if tryMove:
                moved = self.attackUndefened(fleet)
                if not moved:
                    moved = self.moveToUnclaimedPlanet(fleet)
                if not moved:
                    moved = self.moveToEnemyPlanet(fleet)


        initialFleets = currentPlayer.fleets
        for fleet in initialFleets:
            self.combineWithFleetsInSector(fleet)
                        
    def isPlanetSafe(self, planetName):
        planet = self.table.galaxy.getPlanet(planetName)
        xPos = planet.xPos
        yPos = planet.yPos
        threats = self.getEnemyFleetsThatCanReach(planet.owner, xPos, yPos)
        if threats == []:
            return True
        else:
            for fleetName in threats:
                fleet = self.table.getFleet(fleetName)
                if fleet.numBattalions > 0:
                    return False
                elif fleet.numSquadrons > 0:
                    return False
            return True

    def attackUndefened(self, fleet):
        if fleet.numSquadrons > 0:
            enemyFleets = getEnemyFleetsThatCanReach(fleet.side, fleet.xPos, fleet,yPos)
            for enemy in enemyFleets:
                content = self.table.getFleet(enemy)
                if content.numSquadrons == 0:
                    if content.numBattalions > 0:
                        self.table.updateFleetPosition(fleet.idVal, content.xPos, content.yPos)
                        print(fleet.side + "moved fleet")
                        self.checkForConflict(content.xPos, content.yPos (content.xPos, content.yPos))
                        return True
        return False
                    
    def moveToUnclaimedPlanet(self, fleet):
        unclaimedPlanets = []
        for planet in self.table.galaxy.planets:
            if planet.owner == "none":
                unclaimedPlanets = unclaimedPlanets + [planet]
        
        lowestDiff = 10000
        targetPlanet = "none"
        for planet in unclaimedPlanets:
                xDiff = abs(planet.xPos-fleet.xPos)
                yDiff = abs(planet.yPos-fleet.yPos)
                totalDiff = xDiff + yDiff
                if totalDiff < lowestDiff:
                    targetPlanet = planet
                    lowestDiff = totalDiff
        if targetPlanet != "none":
            return self.moveToward(fleet, targetPlanet.xPos, targetPlanet.yPos)
        else:
            return False
        
    def moveToEnemyPlanet(self, fleet):
        enemyPlanets = []
        for planet in self.table.galaxy.planets:
            if planet.owner != "none":
                if planet.owner != fleet.side:
                    enemyPlanets = enemyPlanets + [planet]

        lowestDiff = 10000
        targetPlanet = "none"
        for planet in enemyPlanets:
                xDiff = abs(planet.xPos-fleet.xPos)
                yDiff = abs(planet.yPos-fleet.yPos)
                totalDiff = xDiff + yDiff
                if totalDiff < lowestDiff:
                    targetPlanet = planet
                    lowestDiff = totalDiff

        if targetPlanet != "none":
            return self.moveToward(fleet, targetPlanet.xPos, targetPlanet.yPos)
        else:
            return False
                    
    def moveToward(self, fleet, xPos, yPos):
        newXPos = fleet.xPos
        newYPos = fleet.yPos
        
        xDiff = abs(xPos-fleet.xPos)
        yDiff = abs(yPos-fleet.yPos)
        totalDiff = xDiff + yDiff
        if totalDiff <= fleet.moveRange:
            self.table.updateFleetPosition(fleet.idVal, xPos, yPos)
            self.checkForConflict(xPos, yPos, (xPos, yPos))
            return True
        else:
            for i in range(fleet.moveRange):
                xDiff = fleet.xPos-xPos
                yDiff = fleet.yPos-yPos
                if abs(xDiff) >= abs(yDiff):
                    if xDiff > 0:
                        newXPos = newXPos - 1
                    elif xDiff < 0:
                        newXPos = newXPos + 1
                else:
                    if yDiff > 0:
                        newYPos = newYPos - 1
                    elif yDiff < 0:
                        newYPos = newYPos + 1
            dontMove = False
            if fleet.numSquadrons == 0:
                threats = self.getEnemyFleetsThatCanReach(fleet.side, newXPos, newYPos)
                for enemy in threats:
                    enemyFleet = self.table.getFleet(enemy)
                    if enemyFleet.numSquadrons > 0:
                        if fleet.numBattalions > 0:
                            dontMove = True

            if dontMove == False:
                self.table.updateFleetPosition(fleet.idVal, newXPos, newYPos)
                self.checkForConflict(newXPos, newYPos, (newXPos, newYPos))
                return True
        return False

    def combineWithFleetsInSector(self, fleet):
        sector = self.findSector((fleet.xPos, fleet.yPos))
        for galacticObject in sector:
            if galacticObject[0:5] == "Fleet":
                if self.table.getFleet(galacticObject).side == fleet.side:
                    if galacticObject != fleet.idVal:
                        self.table.combineFleets(fleet.idVal, galacticObject)
                

    def getEnemyFleetsThatCanReach(self, side, xPos, yPos):
        galaxyMap = self.table.returnGalaxyMap()
        threats = []
        for x in range(xPos-5, xPos+5):
            if x >= 0 and x < len(galaxyMap):
                for y in range(yPos-5, yPos+5):
                    if y >= 0 and y < len(galaxyMap):
                        xDiff = abs(xPos-x)
                        yDiff = abs(yPos-y)
                        totalDiff = xDiff + yDiff
                        if totalDiff <= 5:
                            sector = galaxyMap[x][y]
                            for galacticObject in sector:
                                if galacticObject[0:5] == "Fleet":
                                    if self.table.getFleet(galacticObject).side != side:
                                        threats = threats + [galacticObject]
        return threats
                
                  
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

            ownedByPlayer = False
            if fleet.side == currentPlayer.side:
                ownedByPlayer = True
                
            selection = ownedByPlayer
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

            selection = ownedByPlayer
            while selection:
                r = raw_input("Split this fleet in to smaller fleets? (yes/no): ")
                if r == "yes":
                    self.splitFleet(galacticObject)
                elif r == "no":
                    selection = False
                else:
                    print("Invalid selection")

            if fleet.moved == False and ownedByPlayer:
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
                    conflict = self.checkForConflict(newXPos, newYPos, position)
                    selecting = False
                else:
                    print("That's too far away")
                        

    def checkForConflict(self, newXPos, newYPos, position):
        contentSector = self.findSector(position)
        planetSide = "NOPLANET"
        conflictedPlanet = "NOPLANET" 
        firstSide = "none"
        conflictingSides = False
        for galacticObject in contentSector:
            if "Planet" == galacticObject[0:6]:
                planetSide = self.table.getPlanetOwner(galacticObject)
                conflictedPlanet = galacticObject
            elif "Fleet" == galacticObject[0:5]:
                if firstSide == "none":
                    firstSide = self.table.getFleet(galacticObject).side
                elif firstSide != self.table.getFleet(galacticObject).side:
                    conflictingSides = True

        if conflictingSides:
            side1Battalions = 0
            side1Squadrons = 0
            side1Heros = 0
            side1Infiltration = 0
            side2Battalions = 0
            side2Squadrons = 0
            side2Heros = 0
            side2Infiltration = 0
            side1 = "NOSIDE"
            side2 = "NOSIDE"
            conflictProgress = False
            for galacticObject in contentSector:
                if "Fleet" == galacticObject[0:5]:
                    fleetContent = self.table.getFleet(galacticObject)
                    if side1 == "NOSIDE":
                        side1 = fleetContent.side
                    elif side2 == "NOSIDE":
                        if fleetContent.side != side1:
                            side2 = fleetContent.side

                    if side1 == fleetContent.side:
                        side1Battalions = side1Battalions + fleetContent.numBattalions
                        side1Squadrons = side1Squadrons + fleetContent.numSquadrons
                        side1Heros = side1Heros + fleetContent.numHeros
                        side1Infiltration = side1Infiltration + fleetContent.numInfiltration
                    else:
                        side2Battalions = side2Battalions + fleetContent.numBattalions
                        side2Squadrons = side2Squadrons + fleetContent.numSquadrons
                        side2Heros = side2Heros + fleetContent.numHeros
                        side2Infiltration = side2Infiltration + fleetContent.numInfiltration

            if side1Squadrons > 0:
                if side2Squadrons > 0:
                    victor = self.comenceSpaceBattle(side1, side2)
                    if victor == side1:
                        self.table.reduceSquadronsInSector(side2, newXPos, newYPos, 1)
                        print(side2 + " lost a squadron")
                    else:
                        self.table.reduceSquadronsInSector(side1, newXPos, newYPos, 1)
                        print(side1 + " lost a squadron")
                    conflictProgress = True
                elif planetSide != side2:
                    self.table.removeBattalionsInSector(side2, newXPos, newYPos)
                    print(side2 + " lost " + str(side2Battalions) + " Battalions due to lack of squadron support")
                    side2Battalions = 0
                    conflictProgress = True
            elif side2Squadrons > 0:
                if planetSide != side1:
                    self.table.removeBattalionsInSector(side1, newXPos, newYPos)
                    print(side1 + " lost " + str(side1Battalions) + " Battalions due to lack of squadron support")
                    side1Battalions = 0
                    conflictProgress = True

            if conflictedPlanet != "NOPLANET":
                if side1Battalions > 0:
                    if side2Battalions > 0:
                        if planetSide == side1:
                            if side1Squadrons == 0:
                                victor = self.comenceLandBattle(conflictedPlanet, side1, side2)
                                if victor == side1:
                                    self.table.reduceBattalionsInSector(side2, newXPos, newYPos, 1)
                                    print(side2 + " lost a battalion")
                                    conflictProgress = True
                                else:
                                    self.table.reduceBattalionsInSector(side1, newXPos, newYPos, 1)
                                    print(side1 + " lost a battalion")
                                    conflictProgress = True
                        elif planetSide == side2:
                            if side2Squadrons == 0:
                                victor = self.comenceLandBattle(conflictedPlanet, side1, side2)
                                if victor == side1:
                                    self.table.reduceBattalionsInSector(side2, newXPos, newYPos, 1)
                                    print(side2 + " lost a battalion")
                                    conflictProgress = True
                                else:
                                    self.table.reduceBattalionsInSector(side1, newXPos, newYPos, 1)
                                    print(side1 + " lost a battalion")
                                    conflictProgress = True
            
                        
            if conflictProgress:
                self.checkForConflict(newXPos, newYPos, position)
                    
                    
        elif planetSide != "NOPLANET":
            convertTo = self.table.getFleet(contentSector[1]).side
            if planetSide != convertTo:
                self.table.convertPlanet(conflictedPlanet, convertTo)
                print("Captured " + conflictedPlanet + " for the " + convertTo)
            
            
    def comenceSpaceBattle(self, side1, side2):
        #gamemode, map, game
        mapToPlay = self.table.returnSpaceBattle()
        print("Play " + mapToPlay[1] + " on " + mapToPlay[0] + " in " + mapToPlay[-1])
        selecting = True
        while selecting:
            r = raw_input("Which side won? ")
            if r == side1:
                return side1
            elif r == side2:
                return side2
            else:
                print("That side was not in the conflict")

    def comenceLandBattle(self, planet, side1, side2):
        #gamemode, map, game
        mapToPlay = self.table.returnLandBattle(planet)
        print("Play " + mapToPlay[1] + " on " + mapToPlay[0] + " in " + mapToPlay[-1])
        selecting = True
        while selecting:
            r = raw_input("Which side won? ")
            if r == side1:
                return side1
            elif r == side2:
                return side2
            else:
                print("That side was not in the conflict")
        
        
            
                
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
        if isinstance(userInput, basestring) == False:
            return currentMap[userInput[0]][userInput[1]]
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        num = 0
        if userInput[1:] != '' and userInput[1:].isdigit():
            num = int(userInput[1:])
        else:
            return "notASector"
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
            
        
            
        
