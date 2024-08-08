from file import readF

class Program:
    def __init__(self, file):
        self.size = 10
        self.mapWumpus = [[False for _ in range(10)] for _ in range(10)] # 100
        self.mapPit = [[False for _ in range(10)] for _ in range(10)] # 200
        self.mapPGas = [[False for _ in range(10)] for _ in range(10)] # 300
        self.mapHPotion = [[False for _ in range(10)] for _ in range(10)] # 400
        self.mapGold = [[False for _ in range(10)] for _ in range(10)] # 500
        ###
        # Save cell:     1 -> 100
        # Wumpus:      101 -> 200
        # Pit:         201 -> 300
        # Potion Gas:  301 -> 400
        # Heal Potion: 401 -> 500
        # Gold:        501 -> 600
        # Stench:      601 -> 700
        # Breeze:      701 -> 800
        # Whiff:       801 -> 900
        # Glow:        901 -> 1000
        # Save cell:  1001 -> 1100
        # Visited:    1101 -> 1200
        # Reliable:   1201 -> 1300
        ###
        self.getMap(file)
        
        self.x = 0
        self.y = 0
        self.direction = 0 # 0: Up, 1: Right, 2: Down, 3: Left
        self.agentHealth = 100
        self.numPotion = 0
        
        self.isGameOver = False
        self.isGameWin = False
        self.gameScore = 0
    
    def getMap(self, file):
        caveMap = readF(file)
        mapDict = {
            'W': self.mapWumpus,
            'P_G': self.mapPGas,
            'H_P': self.mapHPotion,
            'G': self.mapGold,
            'P': self.mapPit
        }
        
        n = len(caveMap)
        for i in range(n):
            for j in range(n):
                if caveMap[i][j] is None or caveMap[i][j] == 'A':
                    continue
                
                listEntities = caveMap[i][j].split()
                for letter in listEntities:
                    mapDict[letter][i][j] = True
                    
    def getPercept(self):
        percept = []
        mapList = [self.mapWumpus, self.mapPit, self.mapPGas, self.mapHPotion, self.mapGold]
        for index, curMap in enumerate(mapList):
            if curMap[self.x][self.y] == True:
                percept.append([(index + 1) * 100 + self.x * 10 + self.y + 1])
                
        mapList = [self.mapWumpus, self.mapPit, self.mapPGas, self.mapHPotion]
        coorDict = [[self.x, self.y - 1] if self.y != 0 else None, 
                    [self.x + 1, self.y] if self.x != 9 else None, 
                    [self.x, self.y + 1] if self.y != 9 else None, 
                    [self.x - 1, self.y] if self.x != 0 else None]

        for pairCoor in coorDict:
            if pairCoor is None:
                continue
            for index, curMap in enumerate(mapList):
                if curMap[pairCoor[0]][pairCoor[1]] == True:
                    percept.append([(index + 6) * 100 + self.x * 10 + self.y + 1])
                    
        return percept
    
    def handleAction(self, action):
        dictAction = {
            "move forward": lambda: self.handleMoveForward(),
            "turn left": lambda: self.handleTurn(False),
            "turn right": lambda: self.handleTurn(True),
            "grab": lambda: self.handleGrab(),
            "shoot": lambda: self.handleShoot(),
            "climb": lambda: self.handleClimb(),
            "heal": lambda: self.handleHeal()
        }
        self.gameScore -= 10
        
        temp = dictAction[action]
        return
    
    def handleMoveForward(self):
        coorDictNext = [[self.x, self.y - 1] if self.y != 0 else None, 
                        [self.x + 1, self.y] if self.x != 9 else None, 
                        [self.x, self.y + 1] if self.y != 9 else None, 
                        [self.x - 1, self.y] if self.x != 0 else None]
        coorXY = coorDictNext[self.direction] 
        if coorXY is not None:
            self.x, self.y = coorXY[0], coorXY[1]
    
    def handleTurn(self, isAdd = True):
        self.direction = (self.direction + 1) % 4 if isAdd else (self.direction - 1) % 4
        
    def handleGrab(self):
        if self.mapHPotion[self.x][self.y] == True:
            self.mapHPotion[self.x][self.y] = False
            self.numPotion += 1
            
    def handleShoot(self):
        self.gameScore -= 100
        coorDictNext = [[self.x, self.y - 1] if self.y != 0 else None, 
                        [self.x + 1, self.y] if self.x != 9 else None, 
                        [self.x, self.y + 1] if self.y != 9 else None, 
                        [self.x - 1, self.y] if self.x != 0 else None]
        coorXY = coorDictNext[self.direction] 
        if coorXY is not None and self.mapWumpus[coorXY[0], coorXY[1]] == True:
            self.mapWumpus[coorXY[0], coorXY[1]] = False
        return True ### Alert sound
    
    def handleClimb(self):
        if self.x == 9 and self.y == 0:
            self.isGameWin = True
    
    def handleHeal(self):
        if self.numPotion > 0:
            self.numPotion -= 1
            self.agentHealth = (self.agentHealth + 25) % 100
    
    def printPrg(self):
        print("Gold", self.mapGold)
        print("HP", self.mapHPotion)
        print("PG", self.mapPGas)
        print("Pit", self.mapPit)
        print("Wumpus", self.mapWumpus)
        
if __name__ == "__main__":
    ABC = Program('test.txt')
    print(ABC.getPercept())