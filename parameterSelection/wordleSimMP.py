from random import sample
import multiprocessing as mp
import sys
import os
sys.path.append(os.pardir)
from solve import lettercount, normalise, maxIndex, knownFilter # type: ignore

LETTERS = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
LETTERS_DICT = {}
WORDS = []

with open("..\possibleWords.txt", "r") as guessesFile:
    for li in guessesFile.readlines():
        WORDS.append(li.replace("\n", ""))

for i in range(26):
    LETTERS_DICT[LETTERS[i]] = i

def bestGuess(greenWeight, yellowWeight, wordLst = WORDS):
    if len(wordLst) == 0:
        return ""
    elif len(wordLst) == 1:
        return wordLst[0]
    else:
        yellowCounts = [0 for i in range(26)]
        greenCounts = [[0 for i in range(26)] for i in range(5)]
        for word in wordLst:
            for lPos in range(5):
                yellowCounts[LETTERS_DICT[word[lPos]]] += 1
                greenCounts[lPos][LETTERS_DICT[word[lPos]]] += 1

        yellowMin = min(yellowCounts)
        yellowMax = max(yellowCounts)
        greenMin = min([min(row) for row in greenCounts])
        greenMax = max([max(row) for row in greenCounts])

        yellowScores = [normalise(value, yellowMin, yellowMax) for value in yellowCounts]
        greenScores = [[normalise(value, greenMin, greenMax) for value in row] for row in greenCounts]

        scores = []
        for word in wordLst:
            scores.append(0)
            foundLetter = []
            for lPos in range(5):
                scores[-1] += greenWeight * greenScores[lPos][LETTERS_DICT[word[lPos]]]
                if word[lPos] not in foundLetter:
                    scores[-1] += yellowWeight * yellowScores[LETTERS_DICT[word[lPos]]]
                    foundLetter.append(word[lPos])

        return wordLst[maxIndex(scores)]

def makeGuess(answer, guess):
    green = ""
    yellow = ""
    grey = ""
    for i in range(5):
        if answer[i] == guess[i]:
            green += answer[i]
        else:
            green += "."
        if guess[i] not in answer:
            grey += guess[i]
    lettersToFind = [answer[i] for i in range(5) if green[i] == "."]
    for i in range(5):
        if green[i] == "." and guess[i] in lettersToFind:
            yellow += guess[i]
            lettersToFind.remove(guess[i])
        else:
            yellow += "."
    return green, yellow, grey

def wordleRun(answer, params):
    guessCount = 0
    success = False
    green = "....."
    yellow = "....."
    grey = ""
    wordlst = WORDS
    while success == False and len(wordlst) > 0:
        guessCount += 1
        guess = bestGuess(*params, wordlst)
        green, yellow, grey = makeGuess(answer, guess)

        if "." not in green:
            success = True
        else:
            wordlst = [word for word in wordlst if word != guess and knownFilter(word, green, yellow, grey)]
    if success == False:
        print("Oh shit: params = " + repr(params) + ", answer = " + repr(answer))
    return guessCount if success == True else 12

def tupleSum(t1, t2):
    return tuple((t1[0] + t2[0], t1[1] + t2[1]))

def runTests(segment, param):
    results = []
    for word in segment:
        val = wordleRun(word, param)
        guessSums[word] = val
        results.append(val)
    
    return results

guessSums = {}
def averageRun(greenWeight, yellowWeight, noOfTrials = -1):
    if noOfTrials < 1:
        sampleWords = WORDS
        denom = 1
    else:
        sampleWords = sample(WORDS, noOfTrials)
        denom = noOfTrials
    
    n = len(sampleWords)
    segments = [sampleWords[0        : n//4    ],
                sampleWords[n//4     : n//2    ],
                sampleWords[n//2     : 3 * n//4],
                sampleWords[3 * n//4 : n       ]]
    
    param = (greenWeight, yellowWeight)
    totalGuesses = 0
    with mp.Pool(4) as p:
        results = p.starmap(runTests, [(seg, param) for seg in segments])
    # for i in range(len(sampleWords)):
    #     guessSums[sampleWords[i]] = tupleSum(guessSums.get(sampleWords[i], (0, 0)), (results[i], 1))
    for i in range(4):
        totalGuesses += sum([score for score in results[i]])
    # for word in sampleWords:
    #     guessNo = wordleRun(word, (greenWeight, yellowWeight))
    #     guessSums[word] = tupleSum(guessSums.get(word, (0, 0)), (guessNo, 1))
    #     totalGuesses += guessNo
    
    return totalGuesses / denom

def tupleDiv(t):
    return t[0] / t[1]

def hardestWord():
    return max(guessSums.keys(), key=lambda word : tupleDiv(guessSums[word]))

def easisestWord():
    return min(guessSums.keys(), key=lambda word : tupleDiv(guessSums[word]))