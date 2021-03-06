import pickle
import uuid
import os
import random

class PlayingTable:
    def __init__(self):
        self.whoseTurn = ""
        self.galaxy = loadGalaxy("Resources/planets.txt")
        loadMaps(self.galaxy, "Resources/Games")
        self.galaxy.readCosts("Resources")
        self.galaxy.readSides("Resources")
        
        self.galaxy.updateGalaxyMap()

    def saveState(self, filename):
        filename = "saves/" + filename + ".pkl"
        output = open(filename, "wb")
        pickle.dump(self, output)
        output.close()

    @classmethod
    def loadState(self, filename):
        filename = "saves/" + filename + ".pkl"
        inputFile = open(filename, "rb")
        newState = pickle.load(inputFile)
        inputFile.close()
        return newState

    def returnSideOptions(self):
        return self.galaxy.sides

    def createGame(self, playerSide):
        person = Player(playerSide, True)
        self.galaxy.players.append(person)
        self.whoseTurn = playerSide

        aiSide = "none"
        for side in self.galaxy.sides:
            if side != playerSide:
                aiSide = side
                computer = Player(side, False)
                self.galaxy.players.append(computer)

        self.galaxy.convertNonePlayerPlanetsToAi(playerSide, aiSide)

    
    def returnGalaxyMap(self):
        self.galaxy.updateGalaxyMap()
        return self.galaxy.galaxyMap

    def getPlanetOwner(self, planetName):
        for planet in self.galaxy.planets:
            if planet.name == planetName:
                return planet.owner
        return "error"

    def getFleet(self, fleetName):
        players = self.galaxy.players
        for player in players:
            for fleet in player.fleets:
                if fleet.idVal == fleetName:
                    return fleet
        return "error"

    def addPlayerFleet(self, side, xPos, yPos, numBattalions, numSquadrons, numHeros, numInfiltration):
        players = self.galaxy.players
        for player in players:
            if side == player.side:
                player.addFleet(xPos, yPos, numBattalions, numSquadrons, numHeros, numInfiltration)

    def getNextPlayer(self):
        returnSide = self.whoseTurn
        nextTurn = 0
        for side in self.galaxy.sides:
            nextTurn += 1
            if side == self.whoseTurn:
                break
        if nextTurn < len(self.galaxy.sides):
            self.whoseTurn = self.galaxy.sides[nextTurn]
        else:
            self.whoseTurn = self.galaxy.sides[0]

        player = self.galaxy.getPlayer(returnSide)
        for fleet in player.fleets:
            fleet.moved = False

        for planet in self.galaxy.planets:
            if planet.owner == player.side:
                if planet.creditProduction == "high":
                    player.credits = int(player.credits) + 500
                elif planet.creditProduction == "medium":
                    player.credits = int(player.credits) + 250
                elif planet.creditProduction == "low":
                    player.credits = int(player.credits) + 125
                    
        
        return player

    def getCurrentPlayer(self):
        returnSide = ""
        
        nextSide = self.whoseTurn
        currentTurn = 0
        for side in self.galaxy.sides:
            currentTurn += 1
            if side == self.whoseTurn:
                break
        if currentTurn < len(self.galaxy.sides):
            returnSide = self.galaxy.sides[currentTurn]
        else:
            returnSide = self.galaxy.sides[0]

        return self.galaxy.getPlayer(returnSide)

    def purchaseSquadron(self, player, position):
        if int(player.credits) >= int(self.galaxy.costFleet.strip("c")):
            player.credits = int(player.credits) - int(self.galaxy.costFleet.strip("c"))
            self.addPlayerFleet(player.side, position[0], position[1], 0, 1, 0, 0)
            return True
        else:
            return False

    def purchaseBattalion(self, player, position):
        if int(player.credits) >= int(self.galaxy.costFleet.strip("c")):
            player.credits = int(player.credits) - int(self.galaxy.costFleet.strip("c"))
            self.addPlayerFleet(player.side, position[0], position[1], 1, 0, 0, 0)
            return True
        else:
            return False

    def combineFleets(self, fleet1, fleet2):
        fleet1Content = self.getFleet(fleet1)
        fleet2Content = self.getFleet(fleet2)
        fleet1Content.numBattalions += fleet2Content.numBattalions
        fleet1Content.numSquadrons += fleet2Content.numSquadrons
        fleet1Content.numHeros += fleet2Content.numHeros
        fleet1Content.numInfiltration += fleet2Content.numInfiltration
        fleet1Content.moved = True
        self.removeFleet(fleet2)

    def removeFleet(self, fleetName):
        players = self.galaxy.players
        for player in players:
            for fleet in player.fleets:
                if fleet.idVal == fleetName:
                    player.fleets.remove(fleet)

    def updateFleetPosition(self, fleetName, newXPos, newYPos):
        fleet = self.getFleet(fleetName)
        fleet.xPos = newXPos
        fleet.yPos = newYPos
        fleet.moved = True

    def convertPlanet(self, planetName, newSide):
        for planet in self.galaxy.planets:
            if planet.name == planetName:
                planet.owner = newSide
                break

    def reduceSquadronsInSector(self, side, xPos, yPos, reduceBy):
        for player in self.galaxy.players:
            if player.side == side:
                for fleet in player.fleets:
                    if fleet.xPos == xPos:
                        if fleet.yPos == yPos:
                            initialNum = fleet.numSquadrons
                            for reduction in range(initialNum):
                                if reduceBy > 0:
                                    fleet.numSquadrons = fleet.numSquadrons - 1
                                    reduceBy = reduceBy - 1
                            if fleet.numSquadrons == 0:
                                if fleet.numBattalions == 0:
                                    if fleet.numHeros == 0:
                                        if fleet.numInfiltration == 0:
                                            self.removeFleet(fleet.idVal)
                            if reduceBy == 0:
                                return

    def reduceBattalionsInSector(self, side, xPos, yPos, reduceBy):
        for player in self.galaxy.players:
            if player.side == side:
                for fleet in player.fleets:
                    if fleet.xPos == xPos:
                        if fleet.yPos == yPos:
                            initialNum = fleet.numBattalions
                            for reduction in range(initialNum):
                                if reduceBy > 0:
                                    fleet.numBattalions = fleet.numBattalions - 1
                                    reduceBy = reduceBy - 1
                            if fleet.numSquadrons == 0:
                                if fleet.numBattalions == 0:
                                    if fleet.numHeros == 0:
                                        if fleet.numInfiltration == 0:
                                            self.removeFleet(fleet.idVal)
                            if reduceBy == 0:
                                return

    def getBattalionsEnemyInSector(self, side, xPos, yPos):
        total = 0
        for player in self.galaxy.players:
            if player.side != side:
                for fleet in player.fleets:
                    if fleet.xPos == xPos:
                        if fleet.yPos == yPos:
                            total = total + fleet.numBattalions
        return total
        

    def removeBattalionsInSector(self, side, xPos, yPos):
        for player in self.galaxy.players:
            if player.side == side:
                for fleet in player.fleets:
                    if fleet.xPos == xPos:
                        if fleet.yPos == yPos:
                            fleet.numBattalions = 0
                            if fleet.numSquadrons == 0:
                                if fleet.numBattalions == 0:
                                    if fleet.numHeros == 0:
                                        if fleet.numInfiltration == 0:
                                            self.removeFleet(fleet.idVal)

    def getSquadronsEnemyInSector(self, side, xPos, yPos):
        total = 0
        for player in self.galaxy.players:
            if player.side != side:
                for fleet in player.fleets:
                    if fleet.xPos == xPos:
                        if fleet.yPos == yPos:
                            total = total + fleet.numSquadrons
        return total

    def returnSpaceBattle(self):
        for climate in self.galaxy.climates:
            if climate.name == "ClimateShip":
                selector = random.SystemRandom()
                mapToPlay = selector.choice(climate.mapsSpace)
                return [mapToPlay[0], mapToPlay[1][0], mapToPlay[-1]]

    def returnLandBattle(self, planetName):
        planetClimate = "none"
        mapsToSelectFrom = []
        for planet in self.galaxy.planets:
            if planet.name == planetName:
                mapsToSelectFrom = planet.mapsLand
                planetClimate = planet.climate

        for climate in self.galaxy.climates:
            if climate.name == planetClimate:
                mapsToSelectFrom = mapsToSelectFrom + climate.mapsLand

        selector = random.SystemRandom()
        mapToPlay = selector.choice(mapsToSelectFrom)

        gamemodes = mapToPlay[1]
        gamemode = selector.choice(gamemodes)    
        
        return (mapToPlay[0], gamemode, mapToPlay[-1])
                
        
        
        
        
        

            

class Galaxy:
    def __init__(self):
        self.planets = []
        self.climates = []
        self.costBattalion = ""
        self.costFleet = ""
        self.costInfiltrationTeam = ""
        self.costUpgradeScanner = ""
        self.costUnitTier = ""
        self.costNewHero = ""
        self.sides = []
        self.size = 600
        self.galaxyMap = [[]]
        self.players = []

    def convertNonePlayerPlanetsToAi(self, playerSide, aiSide):
        for planet in self.planets:
            if planet.owner != playerSide:
                planet.owner = aiSide

    def hasPlanet(self, planetName):
        for planet in self.planets:
            if planet.name == planetName:
                return True
        return False

    def getPlanet(self, planetName):
        for planet in self.planets:
            if planet.name == planetName:
                return planet
        return False

    def updatePlanet(self, newPlanet):
        for planet in self.planets:
            if planet.name == newPlanet.name:
                planet = newPlanet
        

    def hasClimate(self, climateName):
        for climate in self.climates:
            if climate.name == climateName:
                return True
        return False

    def addClimate(self, climate):
        self.climates.append(climate)

    def getClimate(self, climateName):
        for climate in self.climates:
            if climate.name == climateName:
                return climate
        return False

    def updateClimate(self, newClimate):
        for climate in self.climates:
            if climate.name == newClimate.name:
                climate = newClimate

    def readCosts(self, fileLocation):
        f = fileLocation + "/costConfig.txt"
        if os.path.isfile(f):
            confFile = open(f, "r")
            for line in confFile.readlines():
                if line[0].isupper():
                    return
                elif line[0:9] == "battalion":
                    self.costBattalion = line.split(": ")[1].strip(" ").strip("\n");
                elif line[0:5] == "fleet":
                    self.costFleet = line.split(": ")[1].strip(" ").strip("\n");
                elif line[0:16] == "infiltrationTeam":
                    self.costInfiltrationTeam = line.split(": ")[1].strip(" ").strip("\n");
                elif line[0:14] == "upgradeScanner":
                    self.costUpgradeScanner = line.split(": ")[1].strip(" ").strip("\n");
                elif line[0:8] == "unitTier":
                    self.costUnitTier = line.split(": ")[1].strip(" ").strip("\n");
                elif line[0:7] == "newHero":
                    self.costNewHero = line.split(": ")[1].strip(" ").strip("\n");
        
    def readSides(self, fileLocation):
        f = fileLocation + "/sides.txt"
        if os.path.isfile(f):
            sidesFile = open(f, "r")
            for line in sidesFile.readlines():
                self.sides.append(line.strip(" ").strip("\n"))

    def updateGalaxyMap(self):
        widthHeight = (self.size*2)/50
        row = [];
        galaxyMap = []
        for i in range(widthHeight):
            for j in range(widthHeight):
                row.append([])
            galaxyMap += [row]
            row = []
        
        for planet in self.planets:
            ##pos = planet.position.strip(" ").strip("(").strip(")")
            ##xPos, yPos = pos.split(",")

            ##newYPos = (int(xPos) + self.size)/50
            ##newXPos = ((self.size*2) - (int(yPos) + self.size))/50
            galaxyMap[planet.xPos][planet.yPos].append(planet.name)

        for player in self.players:
            for fleet in player.fleets:
                galaxyMap[fleet.xPos][fleet.yPos].append(fleet.idVal)
    
        self.galaxyMap = galaxyMap

    def getPlayer(self, side):
        for player in self.players:
            if player.side == side:
                return player
            

class Planet:
    def __init__(self, name, position, population, resources, owner, force, forceSide, support, creditProduction, climate):
        self.name = name
        self.position = position
        self.population = population
        self.resources = resources
        self.owner = owner
        self.force = force
        self.forceSide = forceSide
        self.support = support
        self.creditProduction = creditProduction
        self.climate = climate
        self.mapsLand = []
        self.mapsInfiltrate = []

        self.galaxySize = 600

        
        pos = self.position.strip(" ").strip("(").strip(")")
        xPos, yPos = pos.split(",")

        newYPos = (int(xPos) + self.galaxySize)/50
        newXPos = ((self.galaxySize*2) - (int(yPos) + self.galaxySize))/50

        self.xPos = newXPos
        self.yPos = newYPos

        

    def addMapsLand(self, maps):
        for newMap in maps:
            self.mapsLand.append(newMap)

    def addMapsInfiltrate(self, maps):
        for newMap in maps:
            self.mapsInfiltrate.append(newMap)

class Climate:
    def __init__(self, name):
        self.name = name
        self.mapsLand = []
        self.mapsInfiltrate = []
        self.mapsSpace = []
        self.mapsSpaceInfiltrate = []

    def addMapsLand(self, maps):
        for newMap in maps:
            self.mapsLand.append(newMap)

    def addMapsInfiltrate(self, maps):
        for newMap in maps:
            self.mapsInfiltrate.append(newMap)

    def addMapsSpace(self, maps):
        for newMap in maps:
            self.mapsSpace.append(newMap)

    def addMapsSpaceInfiltrate(self, maps):
        for newMap in maps:
            self.mapsSpaceInfiltrate.append(newMap)

class Map:
    def __init__(self, name, modes, game):
        self.name = name
        self.modes = modes
        self.game = game
        self.modesDescription = []

    def addModeDescription(self, description):
        self.modesDescription = description

class Player:
    def __init__(self, side, isHuman):
        self.side = side
        self.isHuman = isHuman
        self.fleets = []
        self.credits = 2000
        self.resources = 1000

    def getFleet(self, fleetId):
        for fleet in self.fleets:
            if fleet.id == fleetId:
                return fleet

    def addFleet(self, xPos, yPos, numBattalions, numSquadrons, numHeros, numInfiltration):
        newFleet = Fleet(numBattalions, numSquadrons, numHeros, numInfiltration, self.side, xPos, yPos)
        self.fleets.append(newFleet)

class Fleet:
    def __init__(self, numBattalions, numSquadrons, numHeros, numInfiltration, side, xPos, yPos):
        self.idVal = "Fleet" + str(uuid.uuid4())
        self.numBattalions = numBattalions
        self.numSquadrons = numSquadrons
        self.numHeros = numHeros
        self.numInfiltration = numInfiltration
        self.side = side
        self.xPos = xPos
        self.yPos = yPos
        self.moved = True
        self.moveRange = 5
 

#list of list of planet, each planet list is (planetName[0], position (x, y)[1], population[2], resources[3], owner[4], force[5], forceSide[6], support[7], creditProduction[8], climate[9])
def loadGalaxy(fileLocation):
    planetsFile = open(fileLocation, "r")
    planets = []
    planetList = []
    firstLoop = True;
    for line in planetsFile.readlines():
        if line.strip() == "":
            x = 0
        elif firstLoop:
            firstLoop = False
            planetList = [line.strip(":\n")]
        elif line[0].isupper():
            newPlanet = Planet(planetList[0], planetList[1], planetList[2], planetList[3], planetList[4], planetList[5], planetList[6], planetList[7], planetList[8], planetList[9])
            planets.append(newPlanet)
            planetList = [line.strip(":\n")]
        else:
            planetList += [line.split(":")[1].strip()]
    galaxy = Galaxy()
    galaxy.planets = planets
    return galaxy
    

def loadMaps(galaxy, mapDirectory):
    # iterate over files in
    for filename in os.listdir(mapDirectory):
        f = os.path.join(mapDirectory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            gameFile = open(f, "r")
            firstLoop = True;

            #vars
            planetOrClimateName = ""
            mapsLand = []
            mapsInfiltrate = []
            mapsSpace = []
            mapsSpaceInfiltrate = []
            
            for line in gameFile.readlines():
                if line.strip() != "":
                    if firstLoop:
                        firstLoop = False
                        planetOrClimateName = line.strip(":\n")
                    elif line[0].isupper():
                        if "Planet" == planetOrClimateName[0:6]:
                            if galaxy.hasPlanet(planetOrClimateName):
                                planet = galaxy.getPlanet(planetOrClimateName)
                                planet.addMapsLand(mapsLand)
                                planet.addMapsInfiltrate(mapsInfiltrate)
                                galaxy.updatePlanet(planet)
                        else:
                            if galaxy.hasClimate(planetOrClimateName) == False:
                                climate = Climate(planetOrClimateName)
                                climate.addMapsLand(mapsLand)
                                climate.addMapsInfiltrate(mapsInfiltrate)
                                climate.addMapsSpace(mapsSpace)
                                climate.addMapsSpaceInfiltrate(mapsSpaceInfiltrate)
                                galaxy.addClimate(climate)
                            else:
                                climate = galaxy.getClimate(planetOrClimateName)
                                climate.addMapsLand(mapsLand)
                                climate.addMapsInfiltrate(mapsInfiltrate)
                                climate.addMapsSpace(mapsSpace)
                                climate.addMapsSpaceInfiltrate(mapsSpaceInfiltrate)
                                galaxy.updateClimate(climate)
                        planetOrClimateName = line.strip(":\n")
                        mapsLand = []
                        mapsInfiltrate = []
                        mapsSpace = []
                        mapsSpaceInfiltrate = []
                    elif "mapsLand: " == line[0:10]:
                        maps = line.split(": ")[1]
                        mapsList = maps.split("), (")
                        mapsList[0] = mapsList[0].strip(" ").strip("(")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")\n")
                        for battleMap in mapsList:
                            mapElements = battleMap.split(", ")
                            newMap = [mapElements[0], mapElements[1:], filename.split(".")[0]]
                            mapsLand.append(newMap)
                    elif "mapsInfiltrate: " == line[0:16]:
                        maps = line.split(": ")[1]
                        mapsList = maps.split("), (")
                        mapsList[0] = mapsList[0].strip(" ").strip("(")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")\n")
                        for battleMap in mapsList:
                            mapElements = battleMap.split(", ")
                            newMap = [mapElements[0], mapElements[1:], filename.split(".")[0]]
                            mapsInfiltrate.append(newMap)
                    elif "mapsSpaceInfiltrate: " == line[0:22]:
                        maps = line.split(": ")[1]
                        mapsList = maps.split("), (")
                        mapsList[0] = mapsList[0].strip(" ").strip("(")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")\n")
                        for battleMap in mapsList:
                            mapElements = battleMap.split(", ")
                            newMap = [mapElements[0], mapElements[1:], filename.split(".")[0]]
                            mapsSpaceInfiltrate.append(newMap)
                    elif "mapsSpace: " == line[0:11]:
                        maps = line.split(": ")[1]
                        mapsList = maps.split("), (")
                        mapsList[0] = mapsList[0].strip(" ").strip("(")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")\n")
                        for battleMap in mapsList:
                            mapElements = battleMap.split(", ")
                            newMap = [mapElements[0], mapElements[1:], filename.split(".")[0]]
                            mapsSpace.append(newMap)
                            
                        
                        
                        
                        




