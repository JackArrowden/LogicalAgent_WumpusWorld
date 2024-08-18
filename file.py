def checkOpenFile(file):
    try:
        with open(file, 'r') as _:
            return True
    except:
        return False
    
def readF(file):
    caveMap = []
    try:
        curFile = open(file, 'r')
        n = int(curFile.readline().strip())
        
        for _ in range(n):
            strArray = curFile.readline().strip().split(".")
            curRow = []
            
            for j in range(n):
                letter = strArray[j]
                if letter[0] == '-':
                    curRow.append(None)
                else:
                    curRow.append(letter)
                    
            caveMap.append(curRow)
              
    finally:
        if curFile:
            curFile.close()
    
    return caveMap

def writeF(file, arrData):
    curFile = open(file, 'w')
    
    n = len(arrData)
    for i in range(n):
        curFile.write(str(arrData[i][0]) + ": " + arrData[i][1])
        if i != n - 1:
            curFile.write('\n')
    return

def readOutputFile(file):
    listCells = []
    try:
        direction = 0
        curFile = open(file, 'r')
        
        allSteps = curFile.readlines()
        
        n = len(allSteps)
        for i in range(n):
            cell = []
            cur = allSteps[i].strip().split(':')
            pos = list(cur[0])
            cell.append([int(cur[0].split(',')[0][1:]), int(cur[0].split(',')[1][1:-1])])
            cell.append(cur[1][1:])
            
            if cell[1] == 'turn right':
                direction = (direction + 1) % 4
            elif cell[1] == 'turn left':
                direction = (direction - 1) % 4
                
            cell.append(direction)
            
            listCells.append(cell)
          
    finally:
        if curFile:
            curFile.close()
            
    return listCells

if __name__ == "__main__":
    # print(readF('test.txt'))
    # writeF('test2.txt', [[(1,1), "move forward"], [(1,2), "turn right"], [(1,2), "shoot"]])
    print(readOutputFile('test2.txt'))