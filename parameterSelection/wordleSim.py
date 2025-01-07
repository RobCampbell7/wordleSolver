from copy import deepcopy
from random import sample
import sys
import os
sys.path.append(os.pardir)
from solve import lettercount, normalise, maxIndex, knownFilter, WORDS # type: ignore

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
    gray = ""
    for i in range(5):
        if answer[i] == guess[i]:
            green += answer[i]
        else:
            green += "."
        if guess[i] not in answer:
            gray += guess[i]
    lettersToFind = [answer[i] for i in range(5) if green[i] == "."]
    for i in range(5):
        if green[i] == "." and guess[i] in lettersToFind:
            yellow += guess[i]
            lettersToFind.remove(guess[i])
        else:
            yellow += "."
    return green, yellow, gray

def wordleRun(answer, params):
    guessCount = 0
    success = False
    green = "....."
    yellow = "....."
    grey = ""
    wordlst = WORDS
    
    for i in range(6):
        wordlst = [word for word in wordlst if knownFilter(word, green, yellow, grey)]
        guessCount += 1
        guess = bestGuess(*params, wordlst)
        green, yellow, grey = makeGuess(answer, guess)

        if "." not in green:
            success = True
            break
    if success == True:
        return guessCount
    else:
        return 7

def tupleSum(t1, t2):
    return tuple((t1[0] + t2[0], t1[1] + t2[1]))

guessSums = {}
def averageRun(positionWeight, occurenceWeight, noOfTrials = -1):
    if noOfTrials < 1:
        sampleWords = WORDS
        denom = 1
    else:
        sampleWords = sample(WORDS, noOfTrials)
        denom = noOfTrials
        
    totalGuesses = 0
    for word in sampleWords:
        guessNo = wordleRun(word, (positionWeight, occurenceWeight))
        guessSums[word] = tupleSum(guessSums.get(word, (0, 0)), (guessNo, 1))
        totalGuesses += guessNo
    
    return totalGuesses / denom

def tupleDiv(t):
    return t[0] / t[1]

def hardestWord():
    return max(guessSums.keys(), key=lambda word : tupleDiv(guessSums[word]))

def easisestWord():
    return min(guessSums.keys(), key=lambda word : tupleDiv(guessSums[word]))