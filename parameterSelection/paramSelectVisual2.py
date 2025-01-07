from copy import deepcopy
import csv
from win11toast import toast
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import multiprocessing as mp

# distanceHash = {}
# def dist(x1, y1, x2, y2):
#     if distanceHash.get((x1, y1, x2, y2), None) == None:
#         distanceHash[(x1, y1, x2, y2)] = ((x1-x2)**2 + (y1-y2)**2)**0.5
#     return distanceHash[(x1, y1, x2, y2)]

distanceHash = {}
def dist2(x1, y1, x2, y2):
    if x1 < x2:
        coords = (x1, y1, x2, y2)
    else:
        coords = (x2, y2, x1, y1)
    if distanceHash.get(coords, None) == None:
        distanceHash[coords] = (x1-x2)**2 + (y1-y2)**2
    return distanceHash[coords]
# def dist2(x1, y1, x2, y2):
#     return (x1-x2)**2 + (y1-y2)**2

def manhattan(x1, x2, y1, y2):
    return x1 + y1 - x2 - y2

def nearestValue(x, y):
    return valueDict[min(valueDict.keys(), key=lambda c : dist2(x, y, *c))]

# def voronoi(valueDict):
#     xField, yField = (np.linspace(0.0, 1.0, 50), np.linspace(0.0, 0.1, 50))
#     zField = np.vectorize(lambda x, y : nearestValue(x, y, valueDict))(xField, yField)
#     zField = zField[:-1, :-1]
#     return zField

# def findVoronoi(row):

particlePositions = []
data = []
# rawData = []
valueDictonaries = []
with open("particlePositions.csv", "r") as posFile:
    valueDict = {}
    for row in csv.reader(posFile):
        if row != []:
            # particlePositions.append([(float(row[3 * i]), float(row[3 * i + 1]), float(row[3 * i + 2])) for i in range(len(row) // 3)])

            for i in range(len(row) // 3):
                valueDict[(float(row[3 * i]), float(row[3 * i + 1]))] = float(row[3 * i + 2])
            # rawData.append(deepcopy(valueDict))
            # data.append(voronoi(valueDict)[2])
            # particlePositions.append([float(x) for x in row])

xBounds = [0, 1]
yBounds = [0, 1]
nX = 100
nY = 100


if __name__=="__main__":
    # with mp.Pool(4) as p:
    #     data = p.map(voronoi, rawData)
    x, y = np.meshgrid(np.linspace(*xBounds, nX), np.linspace(*yBounds, nY))
    data = np.vectorize(nearestValue)(x, y)
    toast("Done!")
    input("Press enter to continue...")

    fig, ax = plt.subplots(figsize=(4, 4))
    plot = plt.pcolormesh(x, y, data, cmap='inferno_r')#, vmin = 2, vmax = 10)
    # plot = plt.pcolormesh(xField, yField, data[0], cmap='inferno_r')#, vmin = 2, vmax = 10)
    # plot2, = plt.plot([x for x, y in swarm.particlePositions()],
    #                   [y for x, y in swarm.particlePositions()], 
    #                   "b.", lw=2)
    # # allPlots = (plot1, plot2)
    plt.show()
