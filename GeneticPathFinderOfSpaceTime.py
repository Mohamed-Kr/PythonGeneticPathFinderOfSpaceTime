from math import *
from random import *
from Plot import *

class GeneticPathFinderOfSpaceTime:
    robotPos = [750,500]
    targetPos = [1000,800]
    baseObstacles = [
        [[0, 0], [0, 3000]],
        [[0, 3000], [2000, 3000]],
        [[2000, 3000],[2000, 0]],
        [[0, 0], [2000, 0]],
        [[800, 0], [800, 2000]],
    ]
    minX = minY = maxY = maxX = 0
    variableObstacles = []

    debug = False

    gen = []
    numberOfGens = 0
    gensMade = 0
    numberReplacedPerGen = 0
    numberKeepedPerGen = 0
    divergence = 0
    best = {"pointsNumber": 0, "points": [], "score": 1000000}
    populationLength = 0
    maxPointsNumber = 0

    def __init__(self, populationLength = 10, maxPointsNumber = 5, debug = False, divergence=10, numberOfGens = 100, numberReplacedPerGen = 4, numberKeepedPerGen=2):
        self.populationLength = populationLength
        self.divergence = divergence
        self.numberReplacedPerGen = numberReplacedPerGen
        self.numberKeepedPerGen = numberKeepedPerGen
        self.numberOfGens = numberOfGens
        self.maxPointsNumber = maxPointsNumber
        self.debug = debug
        self.setMaxAndMinXY()

    def makeFirstGen(self):
        self.gen = []
        for i in range(self.populationLength):
            self.gen.append(self.newIndividual())
        self.gensMade = 1
        print("")
        print("")
        print("")
        print("GEN 1:")
        for p in self.gen:
            print(p)
        print("Best of gen 1", self.best)

    def makeNextGen(self, previousGen):
        nextGen = self.replaceBadest(self.sortGenByScore(previousGen), self.numberReplacedPerGen)
        bestsOfPreviousGen = []
        for i in range(self.numberKeepedPerGen):
            bestsOfPreviousGen.append(previousGen[i])
        for i in range(len(nextGen)):
            if not (i < self.numberKeepedPerGen-1 or i > len(nextGen)-self.numberReplacedPerGen+1):
                nextGen[i] = self.getPathFromPrevious(bestsOfPreviousGen)
        self.gensMade += 1
        print("")
        print("")
        print("")
        print("NEW GEN:")
        for p in nextGen:
            print(p)
        self.gen = nextGen
    
    def bestOfGens(self):
        if self.gensMade == 0: 
            self.makeFirstGen()
        while self.gensMade < self.numberOfGens:
            self.makeNextGen(self.gen)
            print("Best of gen " + str(self.gensMade)+":", self.best)
        return self.best

    def getPathFromPrevious(self, bestPrevious):
        new = bestPrevious[choice(range(len(bestPrevious)))]
        for point in range(len(new["points"])):
            for coord in range(2):
                new["points"][point][coord] += uniform(-1, 1) * self.divergence
        new["score"] = self.getPathScore(new["points"])
        return new

    def replaceBadest(self, gen, numberReplacedPerGen):
        g = gen
        for i in range(numberReplacedPerGen):
            g[len(g)-1-i] = self.newIndividual()
        return g

    def sortGenByScore(self, gen):
        g = []
        for path in gen:
            if g == []: g.append(path)
            elif path["score"] > g[-1]["score"]: g.insert(0, path)
            elif path["score"] < g[0]["score"]: g.append(path)
        return g

    def newIndividual(self):
        new = {"pointsNumber": 0, "points": [], "score": 0}
        new["pointsNumber"] = randint(1, self.maxPointsNumber)
        while not self.isPathPossible(new["points"]):
            new["points"] = []
            for p in range(new["pointsNumber"]):
                new["points"].append([randint(self.minX, self.maxX), randint(self.minY, self.maxY)])
        new["score"] = self.getPathScore(new["points"])
        return new

    def getPathScore(self, path):
        score = 0
        for point in range(len(path)):
            if point == 0:
                score += sqrt((self.robotPos[0]-path[point][0])**2+(self.robotPos[1]-path[point][1])**2)
            elif point == len(path):
                score += sqrt((self.targetPos[0]-path[point][0])**2+(self.targetPos[1]-path[point][1])**2)
            else:
                score += sqrt((path[point-1][0]-path[point][0])**2+(path[point-1][1]-path[point][1])**2)
        if score < self.best["score"]:
            self.best["pointsNumber"] = len(path)
            self.best["points"] = path
            self.best["score"] = score
            display("Best of gen " + str(self.gensMade), self.robotPos, self.targetPos, self.baseObstacles, self.best["points"], [self.minX, self.maxX, self.minY, self.maxY])
        return score

    def isPathPossible(self, path):
        if path == []: return False
        for point in range(len(path)):
            if point == 0 and self.isIntersectingObstacles(self.robotPos, path[point]):
                return False
            if point == len(path)-1 and self.isIntersectingObstacles(self.targetPos,  path[point]):
                return False
            if self.isIntersectingObstacles(path[point-1], path[point]):
                return False
        return True

    def setMaxAndMinXY(self):
        for line in self.baseObstacles:
            for point in line:
                i = 0
                for coord in point:
                    if i == 0:
                        if coord > self.maxX:
                            self.maxX = coord
                        elif coord < self.minX:
                            self.minX = coord
                    else:
                        if coord > self.maxY:
                            self.maxY = coord
                        elif coord < self.minY:
                            self.minY = coord
                    i+=1
        
    def P(self, a):
        if self.debug:
            for i in a:
                print(i)

    def ccw(self, A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

    def isIntersecting(self, A, B, C, D):
        return self.ccw(A, C, D) != self.ccw(B, C, D) and self.ccw(A, B, C) != self.ccw(A, B, D)
    
    def isIntersectingObstacles(self, A, B):
        obstacles = self.baseObstacles + self.variableObstacles
        for o in obstacles:
            if self.isIntersecting(A, B, o[0], o[1]): return True
        return False


pf = GeneticPathFinderOfSpaceTime()
pf.bestOfGens()