from math import inf
from particleSwarm import Swarm
from wordleSimMP import averageRun, hardestWord, easisestWord
import multiprocessing as mp
import csv

if __name__=="__main__":
    n = 10
    w = 0.85
    c1 = 1
    c2 = 1
    iterNo = 200
    noOfTrials = 1000
    swarm = Swarm(n, lambda p1, p2 : averageRun(p1, p2, noOfTrials), w, c1, c2, (0, 1), (0, 1), False)
    with open("particlePositions.csv", "w") as posFile:
        writer = csv.writer(posFile)
        data = []
        for p in swarm.particles:
            data.extend([p.px, p.py, p.f])
        writer.writerow(data)
    # bestAchieved = inf
    # bestGen = 0
    try:
        for i in range(iterNo):
            print("i = " + str(i))
            swarm.iterate()
            with open("particlePositions.csv", "a") as posFile:
                writer = csv.writer(posFile)
                data = []
                for p in swarm.particles:
                    data.extend([p.px, p.py, p.f])
                writer.writerow(data)
            # with mp.Pool(4) as pool:
            #     pool.map(swarm.iterate(), [])
            # swarm.findGlobablBest()
            # processes = [mp.Process(target=swarm.particles[i].iterate) for i in range(swarm.particleNo)]
            # for process in processes:
            #     process.start()
            # for process in processes:
            #     process.join()
            # swarm.findGlobablBest()
            # if swarm.gbestF < bestAchieved:
            #     bestAchieved = swarm.gbestF
            #     bestGen = i
            # elif i - bestGen > 25:
            #     break
    except KeyboardInterrupt:
        pass
    
    swarm.findGlobablBest()
    print("Optimal parameters: " + repr(swarm.gbest))
    print("Hardest word: " + hardestWord())
    print("Easiest word: " + easisestWord())