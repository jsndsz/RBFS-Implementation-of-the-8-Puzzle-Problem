
"""
A board is automatically generated and solved in this problem.
Custom boards can also be built.

 |A|D|G|
 |B|E|H|
 |C|F|I|
 
The arrangement of the board looks like this. Changing the value of the alphabets, changed the numbers.

The problem uses the RBFS alogirthm to solve this.
Graph search is used and repeatitive states are tracked

""" 

import numpy as np
import numpy.random as rand
import time
import sys


"""Generates a valid board to solve"""
class problemGenerator(object):
    def __init__ (self):
        self.maxrow = 3
        self.maxcol = 3
        
    def makeBoard(self):
        self.board = np.zeros((self.maxrow,self.maxcol))
        check = False
        num = rand.randint(9)
        while check == False:
            self.linear = []
            for row in range (self.maxrow):
                for col in range (self.maxcol): 
                    while num in self.linear:
                        num = rand.randint(9)
                    self.board[row][col] = num
                    self.linear.append(num)
            check = self.checkSolve()
        return self.board
        
    def checkSolve(self):
        n=0
        count = 0
        index = self.linear.index(0)
        del self.linear[index]
        for x in range(n,len(self.linear)):
            for y in range(n+1,len(self.linear)):
                if self.linear[x] > self.linear[y]:
                    count+=1
            n=n+1
        if count % 2 ==0:
            return True
        else:
            return False
 
    def getBoard(self):
        return self.board  
    

"""Creates a map of the board, which is used to solve the problem"""
class Graph(object):
    def __init__(self):
        self.edges = {'A':['B','D'], 
                      'B':['A','C','E'],
                      'C':['B','F'],
                      'D':['A','G','E'],
                      'E':['B','D','F','H'],
                      'F':['C','E','I'],
                      'G':['D','H'],
                      'H':['E','I','G'],
                      'I':['F','H']
                      }
        self.nodeList = ['A','B','C','D','E','F','G','H','I']
        self.weightNodes = {}
        self.pathCost = {'A':0,'B':0,'C':0,'D':0,'E':0,'F':0,'G':0,'H':0,'I':0}
        self.gl = [[1,2,3],[4,5,6],[7,8,0]]
 
        
    def setPathCost (self,element):
        self.e = element
        self.pathCost[self.e] +=1
    
    def getPathCost (self,element):
        self.r = element
        return self.pathCost[self.r]
        
    def getNeighbors (self,id):
        return self.edges[id]
    
    def checkGoalState (self,cState):
        self.cState = cState
        masterPlan = ('A','D','G','B','E','H','C','F','I')
        gls = []
        for a in masterPlan:
            gls.append(self.cState[a])
        glsl = [gls[:3],gls[3:6],gls[6:9]]   
        if self.gl == glsl:
            print("Success! Achieved Goal State")
            return True
        else:
            return False
        
    def initialWeights(self):
        self.initialWeight = {}
        pg = problemGenerator()
        self.board = pg.makeBoard()
        count = 0
        for col in range(3):
            for row in range(3):
                self.weightNodes[self.nodeList[count]] = self.board[row][col]
                count+=1
        self.initialWeight = self.weightNodes.copy()
        return self.weightNodes
    
    def getWeightNodes(self):
        return self.weightNodes
        
    def zeroLocator(self,bor):
        self.bor = bor
        for x in self.nodeList:
            if self.bor[x] == 0:
                return x
    
    def heuristics(self,nodeinfo):
        self.nodeInfo = nodeinfo
        masterPlan = ('A','D','G','B','E','H','C','F','I')
        l = []
        h = 0
        for a in masterPlan:
            l.append(nodeinfo[a])
        hl = [l[:3],l[3:6],l[6:9]]
        
        for aa in range(3):
            for bb in range(3):
                find = hl[aa][bb]
                if find != 0:
                    for x in range(3):
                        for y in range(3):
                            if self.gl[x][y] == find:
                                i = x
                                j = y
                    h = h +abs(aa-i)+abs(bb-j)
        return h
        
        
    def nCopies(self,neigh,bb):
        copyDict = {}
        self.bb = bb
        self.neigh = neigh
        for n in neigh:
            copyDict[n] = self.bb.copy()
        return copyDict   
    
    def swap(self,boardSwap,zeroval,valswap):
        self.swapBoard = boardSwap
        self.zeroval = zeroval
        self.valswap = valswap
        valueToSwap = self.swapBoard[self.valswap]
        self.swapBoard[self.valswap] = 0
        self.swapBoard[self.zeroval] = valueToSwap
        return self.swapBoard
            
    
""" RBFS algorithm used to solve the problem"""
class RBFS(Graph):
     
    def findNeighbors(self,name):
        self.name = name
        neighborList = Graph.getNeighbors(self,self.name)
        return neighborList
    
    def printer(self,d):
        self.d = d
        nodeList = ['A','D','G','B','E','H','C','F','I']
        L = []
        for item in nodeList:
            L.append(self.d[item])
        p = [L[:3],L[3:6],L[6:9]]
        pp = np.array(p)
        print(pp)
    
    def checkRepeat(self,di):
        self.di = di
        masterPlan = ('A','D','G','B','E','H','C','F','I')
        cl = []
        for a in masterPlan:
            cl.append(self.di[a])
 
        if cl not in self.closedList :
            self.closedList.append(cl)
            return True
        else:   
            return False
        
        
    def solve(self):
        g = 0
        openList = []
        self.closedList =[]
        sBh =[99999,('A',{})]
        self.borGen = Graph.initialWeights(self)
        """Use the below line to enter data manually and comment out the above line"""
        #self.borGen = {'A':6,'B':3,'C':4,'D':7,'E':2,'F':1,'G':0,'H':5,'I':8}

        print("Board before: ")
        self.printer(self.borGen)
        print("\n Solution to Board: ")
        
        
        while Graph.checkGoalState(self,self.borGen) == False:
            potentialState ={}
            locateZero = Graph.zeroLocator(self,self.borGen)  #Letter where Zero exists in the initital board (weightNodes)()
            neighbors = self.findNeighbors(locateZero) #finds the neighbor of alphabet which is zero
            copyDic = Graph.nCopies(self,neighbors,self.borGen) #returns a copy for each alphabet in neighbors and its values
            for i in neighbors:
               
                potentialSwap = copyDic[i]  #Name and copy of the current swap
                potentialState[i] = Graph.swap(self,potentialSwap,locateZero,i)
                
            hue = 0    
            
            for h in neighbors:
                hue = Graph.heuristics(self,potentialState[h]) #calculating heurisitc cost for each potential state
                hueExtra = hue
                openList.append((hueExtra,h))
    
            
            state = False
            openList.sort()
            
             #sBh stand for second best element, this is tracked throughtout the problem
            while state == False:
                if len(openList) == 0:
                    leastElementState = sBh[1][1]
                    state = True

                else:
                    num = openList[0]
                    leastElementState = potentialState[num[1]]
                    state = self.checkRepeat(leastElementState)
                    del openList[0]
            
            if len(openList) >= 1:
                if openList[0][0] < sBh[0]:
                    sBh= [openList[0][0] ,(openList[0][1], potentialState[openList[0][1]])]  #formulating the second best hue
                
           
            if sBh[0] < num[0]:
                dummy = num[:]
                
                num = [sBh[0],sBh[1][0]]
                leastElementState = sBh[1][1]
                sBh = [dummy[0],(dummy[1] , potentialState[dummy[1]])]
            
            self.borGen = leastElementState.copy()
            openList = []

            
            g+=1
            self.printer(self.borGen)
            print("")
            if(g>10000): #Bailing out if the number of states generated is too high
                print("Taking too long, too many nodes, try again")
                sys.exit()
            
        print("Total states: ",g)

        
 
def main():
    start = time.time()
    algorithm = RBFS() 
    algorithm.solve()
    end = time.time()
    print("Time measure: %.2f sec"  %(end-start))

if __name__ == "__main__":
    print("This is the solution to the 8 puzzle using A* method using graoh data structure")
    main()  
              