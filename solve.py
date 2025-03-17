LETTERS = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
WORDS = []
with open("possibleWords.txt", "r") as guessesFile:
    for li in guessesFile.readlines():
        WORDS.append(li.replace("\n", ""))

GREEN_WEIGHT = 0.396
GREEN_WEIGHT = 1.0
YELLOW_WEIGHT = 1.0

yellowCounts = [0 for i in range(26)]
greenCounts = [[0 for i in range(26)] for i in range(5)]
for word in WORDS:
    for lPos in range(5):
        yellowCounts[LETTERS.index(word[lPos])] += 1
        greenCounts[lPos][LETTERS.index(word[lPos])] += 1

yellowMin = min(yellowCounts)
yellowMax = max(yellowCounts)
greenMin = min([min(row) for row in greenCounts])
greenMax = max([max(row) for row in greenCounts])

def normalise(x, lowerBound, upperBound):
    return (x - lowerBound) / (upperBound - lowerBound)

YELLOW_SCORES = [normalise(value, yellowMin, yellowMax) for value in yellowCounts]
GREEN_SCORES = [[normalise(value, greenMin, greenMax) for value in row] for row in greenCounts]

def lettercount(word, letter):
    count = 0
    for char in word:
        if char == letter:
            count += 1
    return count

def normalise(x, lowerBound, upperBound):
    return (x - lowerBound) / (upperBound - lowerBound)

def maxIndex(lst, ignoreIndexes=[]):
    """
    Returns the index of the maximum value in the list
    """
    indexLst = [i for i in range(len(lst)) if i not in ignoreIndexes]
    return max(indexLst, key=lst.__getitem__)

def knownFilter(word, green=".....", yellow=".....", grey = ""):
    for i in range(5):
        if green[i] != ".":
            if word[i] == green[i]:
                word = word[:i] + "." + word[i + 1:]
            else:
                return False

    for i in range(5):
        if yellow[i] != ".":
            if word[i] == yellow[i]:
                return False
            else:
               found = False
               for j in range(5):
                   if word[j] == yellow[i]:
                       word = word[:j] + "." + word[j + 1:]
                       found = True
                       break
               if found == False:
                   return False 

    for i in range(5):
        if word[i] != "." and word[i] in grey:
            return False
    return True

def bestGuess(wordLst = WORDS):
    if len(wordLst) == 0:
        return ""
    elif len(wordLst) == 1:
        return wordLst[0]
    else:
        scores = []
        for word in wordLst:
            scores.append(0)
            foundLetter = []
            for lPos in range(5):
                scores[-1] += GREEN_WEIGHT * GREEN_SCORES[lPos][LETTERS.index(word[lPos])]
                if word[lPos] not in foundLetter:
                    scores[-1] += YELLOW_WEIGHT * YELLOW_SCORES[LETTERS.index(word[lPos])]
                    foundLetter.append(word[lPos])

        return wordLst[maxIndex(scores)]
    
def combine(str1, str2):
    newStr = ""
    for i in range(5):
        if str1[i] != ".":
            newStr += str1[i]
        elif str2[i] != ".":
            newStr += str2[i]
        else:
            newStr += "."
    return newStr

def maintainSet(setStr, newStr):
    return setStr.extend([char for char in newStr if char not in setStr])

def remove(string, char):
    newString = ""
    for i in range(len(string)):
        if string[i] == char:
            break
        else:
            newString += string[i]
    return newString + string[i + 1:]

if __name__=="__main__":
    wordlst = WORDS
    guess = bestGuess()
    print("  Initial guess : '" + guess.upper() + "'")
    for i in range(5):
        green = input("  Green letters : ").lower()
        if "." not in green:
            print("success")
            break
        yellow = input(" Yellow letters : ").lower()
        grey = input("   Gray letters : ").lower().replace(", ", "").replace(" ", "")
        wordlst = [word for word in wordlst if knownFilter(word, green, yellow, grey)]
        guess = bestGuess(wordlst)
        if guess == "":
            print("No possible solutions")
            break
        print("\nBest next guess : '" + guess.upper() + "'")
