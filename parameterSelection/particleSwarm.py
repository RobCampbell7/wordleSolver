import random
import multiprocessing as mp
import numpy as np
from copy import deepcopy
from itertools import repeat
from math import isqrt, sqrt

def neighbourhood(lst, i, l):
    pointer = i - (l//2)
    nh = []
    while len(nh) < l:
        nh.append(lst[pointer])
        pointer += 1
    return nh

def hexagonalDistribution(n, xLimits, yLimits):
    width = xLimits[1] - xLimits[0]
    height = yLimits[1] - yLimits[0]

    # Calculate the number of points in each direction proportional to the dimensions
    cols = int(sqrt(n * (width / height)))  # Proportional to width
    rows = int(sqrt(n * (height / width)))  # Proportional to height

    points = []
    xUnit = width / (cols + 0.5)  # Hexagonal spacing
    yUnit = height / (rows + 0.5)  # Hexagonal spacing

    for row in range(rows):
        for col in range(cols):
            # Hexagonal offset
            x = xLimits[0] + col * xUnit * 1.5
            y = yLimits[0] + row * yUnit * sqrt(3)

            # Offset every other row
            if row % 2 == 1:
                x += xUnit * 0.75

            # Clip points within the limits
            if xLimits[0] <= x <= xLimits[1] and yLimits[0] <= y <= yLimits[1]:
                points.append((x, y))
            
            if len(points) >= n:
                return points[:n]

    return points[:n]

def gridDistribution(n, xLimits, yLimits):
    cols = isqrt(n)
    rows = (n + cols - 1) // cols
    if cols == 0:
        cols = 1
    if rows == 0:
        rows = 1
    
    xCoords = np.linspace(xLimits[0], xLimits[1], cols)
    yCoords = np.linspace(yLimits[0], yLimits[1], rows)
    
    points = [(x, y) for x in xCoords for y in yCoords][:n]
    return points

class Swarm:
    class particle:
        def __init__(self, greaterSwarm, xPos=None, yPos=None, xBound=[-1, 1], yBound=[-1, 1]):
            self.swarm = greaterSwarm
            if xPos == None:
                self.px = random.uniform(xBound[0], xBound[1])
            else:
                self.px = xPos
            if yPos == None:
                self.py = random.uniform(yBound[0], yBound[1])
            else:
                self.py = yPos
            self.neighbours = []
            self.vx = 0
            self.vy = 0
            self.f = self.swarm.fitness(self.px, self.py)
            self.best = deepcopy((self.px, self.py))
            self.bestF = self.f
        
        def iterate(self, nhbest):
        # def iterate(self):
            r1 = random.uniform(0, 1)
            r2 = random.uniform(0, 1)

            self.vx *= self.swarm.W
            self.vx += self.swarm.C1 * r1 * (self.best[0] - self.px)
            self.vx += self.swarm.C2 * r2 * (nhbest[0] - self.px)
            
            self.vy *= self.swarm.W
            self.vy += self.swarm.C1 * r1 * (self.best[1] - self.py)
            self.vy += self.swarm.C2 * r2 * (nhbest[1] - self.py)
            
            self.px += self.vx
            self.py += self.vy
            self.f = self.swarm.fitness(self.px, self.py)
            
            if self.f < self.bestF:
                self.best = deepcopy((self.px, self.py))

    def __init__(self, particleNo, fitnessFunc, W = 1.0, C1 = 1.0, C2 = 1.0, x=(-3, 3), y=(-3, 3), regularDist = False):
        self.particleNo = particleNo
        self.fitness = fitnessFunc
        if regularDist == False:
            self.particles = [self.particle(self, xBound=x, yBound=y) for i in range(self.particleNo)]
        else:
            self.particles = [self.particle(self, xPos=xPos, yPos=yPos) for xPos, yPos in gridDistribution(self.particleNo, x, y)]
        self.gbest = deepcopy(min(self.particles, key = lambda p : p.bestF).best)
        self.gbestF = deepcopy(min(self.particles, key = lambda p : p.bestF).bestF)
        self.W = W
        self.C1 = C1
        self.C2 = C2
        # self.gbest = deepcopy(min(self.particles, key = lambda p : self.fitness(*p.best)).best)

    def findGlobablBest(self):
        self.gbest = deepcopy(min(self.particles, key = lambda p : p.bestF).best)
        self.gbestF = deepcopy(min(self.particles, key = lambda p : p.bestF).bestF)

    def iterate(self):
        # # bests = [p.bestF for p in self.particles]
        # for i in range(self.particleNo):
        #     self.particles[i].iterate(min(neighbourhood(bests, i, self.l)))

        # self.gbest = deepcopy(min(self.particles, key = lambda p : self.fitness(*p.best)).best)
        # processes = [mp.Process(target=self.particles[i].iterate, args=(self.gbest,)) for i in range(self.particleNo)]
        # for process in processes:
        #     process.start()
        # for process in processes:
        #     process.join()
        self.gbest = deepcopy(min(self.particles, key = lambda p : p.bestF).best)
        for i in range(self.particleNo):
            self.particles[i].iterate(self.gbest)
            print("particle " + str(i + 1) + " complete")
    
    def particlePositions(self):
        return [(p.px, p.py) for p in self.particles]