import csv
import multiprocessing as mp
from math import inf
from wordleSim import averageRun, hardestWord, easisestWord
import matplotlib.pyplot as plt

def map(x, min1, max1, min2, max2):
    return min2 + (x - min1) * (max2 - min2)/(max1 - min1)

if __name__=="__main__":
    xBounds = (0, 2.5)
    yBounds = (0, 2.5)
    xSize = 25
    ySize = 25
    xStep = (xBounds[1] - xBounds[0]) / xSize
    yStep = (yBounds[1] - xBounds[0]) / ySize
    # rawData = []
    # with mp.Pool() as pool:
    #     for j in range(ySize + 1):
    #         rawData.append(pool.starmap(averageRun, [(i * xStep + xBounds[0], j * yStep + yBounds[0], 2000) for i in range(xSize + 1)]))
    #     print("j = " + repr(j) + " : complete")    
    # rawData = [[averageRun(i * xStep + xBounds[0], j * yStep + yBounds[0], 1000) for i in range(xSize + 1)] for j in range(ySize + 1)]
    # with open('rawData.csv', 'r') as f:
    #     # using csv.writer method from CSV package
    #     write = csv.writer(f)
    #     write.writerows(rawData)
    with open('rawData.csv', "r") as f:
        rawData = list(csv.reader(f))
    # print(*rawData, sep="\n")
    # print("Hardest word: " + hardestWord())
    # print("Easiest word: " + easisestWord())
    # maxVal = -inf
    # minVal = inf
    # for j in range(ySize):
    #     for i in range(xSize):
    #         maxVal = max(rawData[j][i], maxVal)
    #         minVal = min(rawData[j][i], minVal)
    # data = [[map(rawData[i][j], minVal, maxVal, 0, 1) for i in range(xSize + 1)] for j in range(ySize + 1)]
    # print(*data, sep="\n,")
    # plt.xlim(*xBounds)
    # plt.ylim(*yBounds)
    data = []
    for row in rawData:
        if row != []:
            data.append([float(v) for v in row])
    plt.imshow(data, cmap = 'inferno_r' , interpolation = 'nearest', origin="lower", extent=[0, 2, 0, 2])
    plt.show()