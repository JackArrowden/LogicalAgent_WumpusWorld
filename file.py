def readF(file):
    try:
        caveMap = []
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
        
        return caveMap
            
    finally:
        curFile.close()

def writeF(file, arrData):
    curFile = open(file, 'w')
    
    n = len(arrData)
    for i in range(n):
        curFile.write(str(arrData[i][0]) + ": " + arrData[i][1])
        if i != n - 1:
            curFile.write('\n')
    return

if __name__ == "__main__":
    # print(readF('test.txt'))
    writeF('test2.txt', [[(1,1), "move forward"], [(1,2), "turn right"], [(1,2), "shoot"]])