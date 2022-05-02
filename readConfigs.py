import os

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
                            newMap = Map(mapElements[0], mapElements[1:], filename.split(".")[0])
                            mapsLand.append(newMap)
                    elif "mapsInfiltrate: " == line[0:16]:
                        maps = line.split(": ")[1]
                        mapsList = maps.split("), (")
                        mapsList[0] = mapsList[0].strip(" ").strip("(")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")\n")
                        for battleMap in mapsList:
                            mapElements = battleMap.split(", ")
                            newMap = Map(mapElements[0], mapElements[1:], filename.split(".")[0])
                            mapsInfiltrate.append(newMap)
                    elif "mapsSpaceInfiltrate: " == line[0:22]:
                        maps = line.split(": ")[1]
                        mapsList = maps.split("), (")
                        mapsList[0] = mapsList[0].strip(" ").strip("(")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")\n")
                        for battleMap in mapsList:
                            mapElements = battleMap.split(", ")
                            newMap = Map(mapElements[0], mapElements[1:], filename.split(".")[0])
                            mapsSpaceInfiltrate.append(newMap)
                    elif "mapsSpace: " == line[0:11]:
                        maps = line.split(": ")[1]
                        mapsList = maps.split("), (")
                        mapsList[0] = mapsList[0].strip(" ").strip("(")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")")
                        mapsList[-1] = mapsList[-1].strip(" ").strip(")\n")
                        for battleMap in mapsList:
                            mapElements = battleMap.split(", ")
                            newMap = Map(mapElements[0], mapElements[1:], filename.split(".")[0])
                            mapsSpace.append(newMap)
                            
                        
                        
                        
                        

#"Resources/Games"
x = loadGalaxy("Resources/planets.txt")
loadMaps(x, "Resources/Games")
x.readCosts("Resources")
print(x.costBattalion, x.costFleet, x.costInfiltrationTeam, x.costUpgradeScanner, x.costUnitTier, x.costNewHero) 
      
for y in x.climates:
    print(y.name);
    for z in y.mapsInfiltrate:
        print(z.name, z.modes, z.game)
    if y.mapsInfiltrate == []:
        print("Oh no!")
