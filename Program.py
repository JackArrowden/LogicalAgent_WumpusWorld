from file import readF

class Program:
    def __init__(self, file):
        self.size = 10
        self.mapWumpus = [[False for _ in range(10)] for _ in range(10)] # 100
        self.mapPit = [[False for _ in range(10)] for _ in range(10)] # 200
        self.mapPGas = [[False for _ in range(10)] for _ in range(10)] # 300
        self.mapHPotion = [[False for _ in range(10)] for _ in range(10)] # 400
        self.mapGold = [[False for _ in range(10)] for _ in range(10)] # 500
        self.dictNumWumpus = {}
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
        # Safe cell:  1001 -> 1100
        # Visited:    1101 -> 1200
        # Reliable:   1201 -> 1300
        # Sound:      1301
        ###
        self.getMap(file)
        
        self.x = 0
        self.y = 0
        self.direction = 0 # 0: Up, 1: Right, 2: Down, 3: Left
        self.agentHealth = 100
        self.numPotion = 0
        self.isSound = False
        
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
                numwumpus = listEntities.count('W')
                if numwumpus > 0:
                    self.dictNumWumpus[(9 - i, j)] = numwumpus
                    
        for i in mapDict:
            mapDict[i].reverse()
                    
    def getPercept(self):
        percept = []
        mapList = [self.mapWumpus, self.mapPit, self.mapPGas, self.mapHPotion, self.mapGold]
        for index, curMap in enumerate(mapList):
            if curMap[self.x][self.y] == True:
                percept.append([(index + 1) * 100 + self.x * 10 + self.y + 1])
            else:
                percept.append([-(index + 1) * 100 - self.x * 10 - self.y - 1])
                
        mapList = [self.mapWumpus, self.mapPit, self.mapPGas, self.mapHPotion]
        coorDict = [[self.x, self.y - 1] if self.y != 0 else None, 
                    [self.x + 1, self.y] if self.x != 9 else None, 
                    [self.x, self.y + 1] if self.y != 9 else None, 
                    [self.x - 1, self.y] if self.x != 0 else None]

        for pairCoor in coorDict:
            if pairCoor is None:
                continue
            for index, curMap in enumerate(mapList):
                curPercept = (index + 6) * 100 + self.x * 10 + self.y + 1
                if curMap[pairCoor[0]][pairCoor[1]] == True:
                    percept.append([curPercept])
        
        for i in range(4):
            curPercept = (i + 6) * 100 + self.x * 10 + self.y + 1
            if [curPercept] not in percept:
                percept.append([-curPercept])
                    
        return percept
    
    def handleAction(self, action):
        self.isSound = False
        dictAction = {
            "move forward": lambda: self.handleMoveForward(),
            "turn left": lambda: self.handleTurn(False),
            "turn right": lambda: self.handleTurn(True),
            "grab": lambda: self.handleGrab(),
            "shoot": lambda: self.handleShoot(),
            "climb": lambda: self.handleClimb(),
            "heal": lambda: self.handleHeal()
        }
        _ = dictAction[action]()
    
    def handleMoveForward(self):
        self.gameScore -= 10
        coorDictNext = [[self.x + 1, self.y] if self.x != 9 else None, 
                        [self.x, self.y + 1] if self.y != 9 else None, 
                        [self.x - 1, self.y] if self.x != 0 else None, 
                        [self.x, self.y - 1] if self.y != 0 else None]
        coorXY = coorDictNext[self.direction] 
        if coorXY is not None:
            self.x, self.y = coorXY[0], coorXY[1]
            if self.mapPGas[self.x][self.y] == True:
                self.agentHealth = (self.agentHealth - 25) % 100
    
    def handleTurn(self, isAdd = True):
        self.gameScore -= 10
        self.direction = (self.direction + 1) % 4 if isAdd else (self.direction - 1) % 4
        
    def handleGrab(self):
        self.gameScore -= 10
        if self.mapHPotion[self.x][self.y] == True:
            self.mapHPotion[self.x][self.y] = False
            self.numPotion += 1
        elif self.mapGold[self.x][self.y] == True:
            self.mapGold[self.x][self.y] = False
            self.gameScore += 5000
            
    def handleShoot(self):
        self.gameScore -= 100
        coorDictNext = [[self.x + 1, self.y] if self.x != 9 else None, 
                        [self.x, self.y + 1] if self.y != 9 else None, 
                        [self.x - 1, self.y] if self.x != 0 else None, 
                        [self.x, self.y - 1] if self.y != 0 else None]
        coorXY = coorDictNext[self.direction] 
        if coorXY is not None and self.mapWumpus[coorXY[0]][coorXY[1]] == True:
            self.dictNumWumpus[(coorXY[0], coorXY[1])] -= 1
            if self.dictNumWumpus[(coorXY[0], coorXY[1])] == 0:
                self.mapWumpus[coorXY[0]][coorXY[1]] = False
            self.isSound = True
    
    def handleClimb(self):
        self.gameScore += 10
        if self.x == 0 and self.y == 0:
            self.isGameWin = True
    
    def handleHeal(self):
        self.gameScore -= 10
        if self.numPotion > 0:
            self.numPotion -= 1
            self.agentHealth = (self.agentHealth + 25) if self.agentHealth != 100 else 100
    
    def printPrg(self):
        print("Gold", self.mapGold)
        print("HP", self.mapHPotion)
        print("PG", self.mapPGas)
        print("Pit", self.mapPit)
        print("Wumpus", self.mapWumpus)
        
class GUIProgram:
    def __init__(self):
        self.size = 10
        self.mapWumpus = [[False for _ in range(10)] for _ in range(10)] # 100
        self.mapPit = [[False for _ in range(10)] for _ in range(10)] # 200
        self.mapPGas = [[False for _ in range(10)] for _ in range(10)] # 300
        self.mapHPotion = [[False for _ in range(10)] for _ in range(10)] # 400
        self.mapGold = [[False for _ in range(10)] for _ in range(10)] # 500
        
        self.x = 9
        self.y = 0
        self.direction = 0 # 0: Up, 1: Right, 2: Down, 3: Left
        self.agentHealth = 100
        self.numPotion = 0
        self.isSound = False
        self.totalWumpus = 0
        self.totalGold = 0
        
        self.isGameWin = False
        self.gameScore = 0
        self.curStep = 0
        
        self.listKilledWumpus = {}
        self.listPickedHPotion = {}
        self.listHealth = {}
        self.listGold = {}
        self.listLostBlood = {}
        self.dictNumWumpus = {}
    
    def getMap(self, file):
        self.mapWumpus = [[False for _ in range(10)] for _ in range(10)] # 100
        self.mapPit = [[False for _ in range(10)] for _ in range(10)] # 200
        self.mapPGas = [[False for _ in range(10)] for _ in range(10)] # 300
        self.mapHPotion = [[False for _ in range(10)] for _ in range(10)] # 400
        self.mapGold = [[False for _ in range(10)] for _ in range(10)] # 500
        
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
                numwumpus = listEntities.count('W')
                if numwumpus > 0:
                    self.dictNumWumpus[(i, j)] = numwumpus
                    
        self.x = 9
        self.y = 0
        self.direction = 0 # 0: Up, 1: Right, 2: Down, 3: Left
        self.agentHealth = 100
        self.numPotion = 0
        self.isSound = False
        self.totalWumpus = sum(self.dictNumWumpus[num] for num in self.dictNumWumpus)
        self.totalGold = sum(curList.count(True) for curList in self.mapGold)
        
        self.isGameWin = False
        self.gameScore = 0
        self.curStep = 0
        
        self.listKilledWumpus = {}
        self.listPickedHPotion = {}
        self.listHealth = {}
        self.listGold = {}
        self.listLostBlood = {}
        self.isNewCell = False
            
    def handlePrevAction(self, action, pos):
        self.x = pos[0]
        self.y = pos[1]
        
        self.curStep -= 1 if self.curStep > 0 else 0
        self.isSound = False
        dictAction = {
            "grab": lambda: self.handlePrevGrab(),
            "shoot": lambda: self.handlePrevShoot(),
            "climb": lambda: self.handlePrevClimb(),
            "heal": lambda: self.handlePrevHeal(),
            "move forward": None,
            "turn left": lambda: self.handlePrevTurn(False),
            "turn right": lambda: self.handlePrevTurn(True)
        }
        # print('prevdir', self.direction, 'coor', self.x, self.y, action)
        if dictAction[action] != None:
            dictAction[action]()
        else:
            self.gameScore += 10
            nextStep = self.curStep + 1
            if nextStep in self.listLostBlood:
                self.agentHealth += 25
    
    def handleNextAction(self, action, pos):
        if not (self.x == pos[0] and self.y == pos[1]):
            self.isNewCell = True 
        self.x = pos[0]
        self.y = pos[1]
        self.curStep += 1
        self.isSound = False
        dictAction = {
            "grab": lambda: self.handleNextGrab(),
            "shoot": lambda: self.handleNextShoot(),
            "climb": lambda: self.handleNextClimb(),
            "heal": lambda: self.handleNextHeal(),
            "move forward": None,
            "turn left": lambda: self.handleNextTurn(False),
            "turn right": lambda: self.handleNextTurn(True)
        }
        # print('nextdir', self.direction, 'coor', self.x, self.y, action)
        if dictAction[action] != None:
            dictAction[action]()
        else:
            self.gameScore -= 10
        if self.mapPGas[self.x][self.y] == True and self.isNewCell:
            self.isNewCell = False
            self.agentHealth = (self.agentHealth - 25) % 100
            self.listLostBlood[self.curStep] = [self.x, self.y]
        
    def handlePrevTurn(self, isAdd = True):
        self.gameScore += 10
        self.direction = (self.direction - 1) % 4 if isAdd else (self.direction + 1) % 4
        
    def handleNextTurn(self, isAdd = True):
        self.gameScore -= 10
        self.direction = (self.direction + 1) % 4 if isAdd else (self.direction - 1) % 4
        
    def handlePrevGrab(self):
        self.gameScore += 10
        nextStep = self.curStep + 1
        if nextStep in self.listPickedHPotion:
            self.mapHPotion[self.x][self.y] = True
            self.numPotion -= 1
        elif nextStep in self.listGold:
            self.mapGold[self.x][self.y] = True
            self.gameScore -= 5000
        
    def handleNextGrab(self):
        self.gameScore -= 10
        if self.mapHPotion[self.x][self.y] == True:
            self.mapHPotion[self.x][self.y] = False
            self.numPotion += 1
            self.listPickedHPotion[self.curStep] = [self.x, self.y]  
        elif self.mapGold[self.x][self.y] == True:
            self.mapGold[self.x][self.y] = False
            self.gameScore += 5000
            self.listGold[self.curStep] = [self.x, self.y]
            
    def handlePrevShoot(self):
        self.gameScore += 100
        coorDictNext = [[self.x - 1, self.y] if self.x != 9 else None, 
                        [self.x, self.y + 1] if self.y != 9 else None, 
                        [self.x + 1, self.y] if self.x != 0 else None, 
                        [self.x, self.y - 1] if self.y != 0 else None]
        coorXY = coorDictNext[self.direction] 
        nextStep = self.curStep + 1
        if nextStep in self.listKilledWumpus:
            # print('dirrev', self.direction)
            # print(self.dictNumWumpus)
            # print(coorXY[0], coorXY[1])
            self.dictNumWumpus[(coorXY[0], coorXY[1])] += 1
            self.mapWumpus[coorXY[0]][coorXY[1]] = True
            
    def handleNextShoot(self):
        self.gameScore -= 100
        coorDictNext = [[self.x - 1, self.y] if self.x != 9 else None, 
                        [self.x, self.y + 1] if self.y != 9 else None, 
                        [self.x + 1, self.y] if self.x != 0 else None, 
                        [self.x, self.y - 1] if self.y != 0 else None]
        coorXY = coorDictNext[self.direction] 
        if coorXY is not None and self.mapWumpus[coorXY[0]][coorXY[1]] == True:
            # print('dir', self.direction)
            # print('next', self.dictNumWumpus)
            self.dictNumWumpus[(coorXY[0], coorXY[1])] -= 1
            self.listKilledWumpus[self.curStep] = [coorXY[0], coorXY[1]]
            
            if self.dictNumWumpus[(coorXY[0], coorXY[1])] == 0:
                self.mapWumpus[coorXY[0]][coorXY[1]] = False
            self.isSound = True

    def handlePrevClimb(self):
        self.gameScore -= 10
        if self.x == 9 and self.y == 0:
            self.isGameWin = False
    
    def handleNextClimb(self):
        self.gameScore += 10
        if self.x == 9 and self.y == 0:
            self.isGameWin = True
    
    def handlePrevHeal(self):
        nextStep = self.curStep + 1
        self.gameScore += 10
        if nextStep in self.listHealth:
            self.numPotion += 1
            self.agentHealth = self.agentHealth - 25
    
    def handleNextHeal(self):
        self.gameScore -= 10
        if self.numPotion > 0:
            self.numPotion -= 1
            self.agentHealth = (self.agentHealth + 25) if self.agentHealth != 100 else 100
            self.listHealth[self.curStep] = [self.x, self.y]
        
def getAllPercepts(program):
    result = [[[False for _ in range(4)] for _ in range(10)] for _ in range(10)]
    mapDict = {
        0: program.mapWumpus,
        1: program.mapPit,
        2: program.mapPGas,
        3: program.mapHPotion
    }
        
    for i in range(10):
        for j in range(10):
            for k in mapDict:
                if mapDict[k][i][j]:
                    if i != 9:
                        result[i + 1][j][k] = True
                    if i != 0:
                        result[i - 1][j][k] = True
                    if j != 9:
                        result[i][j + 1][k] = True
                    if j != 0:
                        result[i][j - 1][k] = True
                
    return result

def getAllElements(program):
    result = [[[False for _ in range(5)] for _ in range(10)] for _ in range(10)]
    mapDict = {
        0: program.mapWumpus,
        1: program.mapPit,
        2: program.mapPGas,
        3: program.mapHPotion,
        4: program.mapGold
    }

    for i in range(10):
        for j in range(10):
            for k in range(5):
                result[i][j][k] = mapDict[k][i][j]
                
    return result
        
def getNumDeadWumpus(program):
    return program.totalWumpus - sum(program.dictNumWumpus[num] for num in program.dictNumWumpus)
     
def getNumGold(program):
    return program.totalGold - sum(curList.count(True) for curList in program.mapGold)
        
if __name__ == "__main__":
    ABC = GUIProgram()
    ABC.getMap('test.txt')
    # print(getNumGold(ABC))
    # ABC.handleNextAction('turn right', (0, 0))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('move forward', (0, 0))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('move forward', (0, 1))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('turn left', (0, 2))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('move forward', (0, 2))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('turn right', (1, 2))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('shoot', (1, 2))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('turn left', (1, 2))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('move forward', (1, 2))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    # ABC.handleNextAction('shoot', (2, 2))
    # print(ABC.gameScore, ABC.x, ABC.y, ABC.direction)
    
    
    # print(getAllPercepts(ABC))
    # print(getAllElements(ABC))
    # print(getNextDir(3, [(1, 3), (2, 4), (3, 3), (2, 2)], 2, 3))