import os
import time
from solve import bestGuess, WORDS
from random import choice, random, sample, shuffle

GREEN_BOX = "🟩"
YELLOW_BOX = "🟨"
GREY_BOX = "  "
LETTERS = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
WORDS = []

GREEN_WEIGHT = 0.396
YELLOW_WEIGHT = 1.0

if __name__=="__main__":
    with open("possibleAnswers.txt", "r") as guessesFile:
        for li in guessesFile.readlines():
            WORDS.append(li.replace("\n", ""))

def knownFilter(word, green=".....", yellow=".....", grey = ""):
    remaining = ""
    letterCount = {}
    for i in range(5):
        if green[i] != ".":
            if green[i] != word[i]:
                return False
            else:
                letterCount[word[i]] += 1
    for i in range(5):
        if yellow[i] != ".":
            if yellow[i] == word[i]:
                return False
            elif letterCount.get(yellow[i], 0) == 0:
                return False
            else:
                letterCount[i] -= 1
    # remaining = [char for char in letterCount.keys() if letterCount[char] > 0]
    for char in letterCount.keys():
        if letterCount[char] > 0:
            if char in grey:
                return False
    return True

def lettercount(word, letter):
    count = 0
    for char in word:
        if char == letter:
            count += 1
    return count

def printResult(green, yellow, guess):
    output = ""
    for i in range(5):
        if green[i] != ".":
            output += GREEN_BOX
        elif yellow[i] != ".":
            output += YELLOW_BOX
        else:
            output += GREY_BOX
    print(output + "    " + guess)

def makeGuess(answer, guess):
    # Taken from ./parameterSelection/wordleSimMP.py
    green = ""
    yellow = ""
    grey = ""
    for i in range(5):
        if answer[i] == guess[i]:
            green += answer[i]
        else:
            green += "."
        # if guess[i] not in answer:
        #     grey += guess[i]
    lettersToFind = [answer[i] for i in range(5) if green[i] == "."]
    for i in range(5):
        if green[i] == "." and guess[i] in lettersToFind:
            yellow += guess[i]
            lettersToFind.remove(guess[i])
        else:
            yellow += "."
    for i in range(5):
        if green[i] == "." and yellow[i] == ".":
            grey += guess[i]
    
    return green, yellow, grey

def runTest(answer):
    guessCount = 0
    success = False
    green = "....."
    yellow = "....."
    grey = ""
    wordlst = WORDS
    guessedWords = []
    os.system("cls")
    while success == False and len(wordlst) > 0 and guessCount < 6:
        guessCount += 1
        guess = bestGuess(wordlst)
        guessedWords.append(guess)
        green, yellow, grey = makeGuess(answer, guess)
        printResult(green, yellow, guess)

        if "." not in green:
            success = True
        else:
            wordlst = [word for word in wordlst if word != guess and knownFilter(word, green, yellow, grey)]
    if success == False:
        print("FAILED : " + repr(answer))
        input()
    # print(*guessedWords, sep=",\n")

def shuffled(lst):
    return sorted(lst, key = lambda x : 0 if x == "bobby" else random())

def filterWordList(wordlst, green, yellow, grey):
    newWordList = []
    for word in wordlst:
        if word == "bobby":
            print("word found")
        if knownFilter(word, green, yellow, grey) == True:
            newWordList.append(word)
        elif word == "bobby":
            print("AGH FUCK")
    return newWordList

if __name__=="__main__":
    answer = "bobby"
    words = ["saner", "pilot", "moody"]
    wordLst = WORDS
    for word in words:
        green, yellow, grey = makeGuess(answer, word)
        wordLst = filterWordList(wordLst, green, yellow, grey)