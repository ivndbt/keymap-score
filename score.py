from collections import defaultdict
import numpy as np
import random
import matplotlib.pyplot as plt
import time
import datetime


###################
### DEFINITIONS ###
###################

# Keyboard layout
# traditional ISO (x, y, row, finger, home)
# ,---------------------------------------------------.
# | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13|
# `---+---+---+---+---+---+---+---+---+---+---+---+-----.
#       | 14| 15| 16| 17| 18| 19| 20| 21| 22| 23| 24| 25|
#       `---+---+---+---+---+---+---+---+---+---+---+----.
#        | 26| 27| 28| 29| 30| 31| 32| 33| 34| 35| 36| 37|
#      ,-----+---+---+---+---+---+---+---+---+---+---'---'
#      | 38| 39| 40| 41| 42| 43| 44| 45| 46| 47| 48|
#      `-------------------------------------------'
traditionalLayoutMap = {
    1: (0.5, 4.5, 1, 1, 0),
    2: (1.5, 4.5, 1, 1, 0),
    3: (2.5, 4.5, 1, 1, 0),
    4: (3.5, 4.5, 1, 2, 0),
    5: (4.5, 4.5, 1, 3, 0),
    6: (5.5, 4.5, 1, 4, 0),
    7: (6.5, 4.5, 1, 4, 0),
    8: (7.5, 4.5, 1, 5, 0),
    9: (8.5, 4.5, 1, 6, 0),
    10: (9.5, 4.5, 1, 7, 0),
    11: (10.5, 4.5, 1, 8, 0),
    12: (11.5, 4.5, 1, 8, 0),
    13: (12.5, 4.5, 1, 8, 0),

    14: (2, 3.5, 2, 1, 0),
    15: (3, 3.5, 2, 2, 0),
    16: (4, 3.5, 2, 3, 0),
    17: (5, 3.5, 2, 4, 0),
    18: (6, 3.5, 2, 4, 0),
    19: (7, 3.5, 2, 5, 0),
    20: (8, 3.5, 2, 5, 0),
    21: (9, 3.5, 2, 6, 0),
    22: (10, 3.5, 2, 7, 0),
    23: (11, 3.5, 2, 8, 0),
    24: (12, 3.5, 2, 8, 0),
    25: (13, 3.5, 2, 8, 0),

    26: (2.25, 2.5, 3, 1, 1),
    27: (3.25, 2.5, 3, 2, 1),
    28: (4.25, 2.5, 3, 3, 1),
    29: (5.25, 2.5, 3, 4, 1),
    30: (6.25, 2.5, 3, 4, 0),
    31: (7.25, 2.5, 3, 5, 0),
    32: (8.25, 2.5, 3, 5, 1),
    33: (9.25, 2.5, 3, 6, 1),
    34: (10.25, 2.5, 3, 7, 1),
    35: (11.25, 2.5, 3, 8, 1),
    36: (12.25, 2.5, 3, 8, 0),
    37: (13.25, 2.5, 3, 8, 0),

    38: (1.75, 1.5, 4, 1, 0),
    39: (2.75, 1.5, 4, 1, 0),
    40: (3.75, 1.5, 4, 2, 0),
    41: (4.75, 1.5, 4, 3, 0),
    42: (5.75, 1.5, 4, 4, 0),
    43: (6.75, 1.5, 4, 4, 0),
    44: (7.75, 1.5, 4, 5, 0),
    45: (8.75, 1.5, 4, 5, 0),
    46: (9.75, 1.5, 4, 6, 0),
    47: (10.75, 1.5, 4, 7, 0),
    48: (11.75, 1.5, 4, 8, 0)
}

# traditional ANSI (x, y, row, finger, home)
# ,---------------------------------------------------.
# | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13|
# `---+---+---+---+---+---+---+---+---+---+---+---+---'
#       | 14| 15| 16| 17| 18| 19| 20| 21| 22| 23| 24| 25|
#       `---+---+---+---+---+---+---+---+---+---+---+---'
#        | 26| 27| 28| 29| 30| 31| 32| 33| 34| 35| 36|
#        `---+---+---+---+---+---+---+---+---+---+---'
#          | 37| 38| 39| 40| 41| 42| 43| 44| 45| 46|
#          `---------------------------------------'
traditionalLayoutMap_ANSI = {
    1: (0.5, 4.5, 1, 1, 0),
    2: (1.5, 4.5, 1, 1, 0),
    3: (2.5, 4.5, 1, 1, 0),
    4: (3.5, 4.5, 1, 2, 0),
    5: (4.5, 4.5, 1, 3, 0),
    6: (5.5, 4.5, 1, 4, 0),
    7: (6.5, 4.5, 1, 4, 0),
    8: (7.5, 4.5, 1, 5, 0),
    9: (8.5, 4.5, 1, 6, 0),
    10: (9.5, 4.5, 1, 7, 0),
    11: (10.5, 4.5, 1, 8, 0),
    12: (11.5, 4.5, 1, 8, 0),
    13: (12.5, 4.5, 1, 8, 0),

    14: (2, 3.5, 2, 1, 0),
    15: (3, 3.5, 2, 2, 0),
    16: (4, 3.5, 2, 3, 0),
    17: (5, 3.5, 2, 4, 0),
    18: (6, 3.5, 2, 4, 0),
    19: (7, 3.5, 2, 5, 0),
    20: (8, 3.5, 2, 5, 0),
    21: (9, 3.5, 2, 6, 0),
    22: (10, 3.5, 2, 7, 0),
    23: (11, 3.5, 2, 8, 0),
    24: (12, 3.5, 2, 8, 0),
    25: (13, 3.5, 2, 8, 0),

    26: (2.25, 2.5, 3, 1, 1),
    27: (3.25, 2.5, 3, 2, 1),
    28: (4.25, 2.5, 3, 3, 1),
    29: (5.25, 2.5, 3, 4, 1),
    30: (6.25, 2.5, 3, 4, 0),
    31: (7.25, 2.5, 3, 5, 0),
    32: (8.25, 2.5, 3, 5, 1),
    33: (9.25, 2.5, 3, 6, 1),
    34: (10.25, 2.5, 3, 7, 1),
    35: (11.25, 2.5, 3, 8, 1),
    36: (12.25, 2.5, 3, 8, 0),

    37: (2.75, 1.5, 4, 1, 0),
    38: (3.75, 1.5, 4, 2, 0),
    39: (4.75, 1.5, 4, 3, 0),
    40: (5.75, 1.5, 4, 4, 0),
    41: (6.75, 1.5, 4, 4, 0),
    42: (7.75, 1.5, 4, 5, 0),
    43: (8.75, 1.5, 4, 5, 0),
    44: (9.75, 1.5, 4, 6, 0),
    45: (10.75, 1.5, 4, 7, 0),
    46: (11.75, 1.5, 4, 8, 0)
}

# linear ISO
# ,---------------------------------------------------.
# | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13|
# `---+---+---+---+---+---+---+---+---+---+---+---+---|
#     | 14| 15| 16| 17| 18| 19| 20| 21| 22| 23| 24| 25|
#     |---+---+---+---+---+---+---+---+---+---+---+---'
#     | 26| 27| 28| 29| 30| 31| 32| 33| 34| 35| 36| 37|
#     |---+---+---+---+---+---+---+---+---+---+---+---'
#     | 38| 39| 40| 41| 42| 43| 44| 45| 46| 47| 48|
#     `-------------------------------------------'
linearLayoutMap = {
    1:  (0.5, 4.5, 1, 1, 0),
    2:  (1.5, 4.5, 1, 1, 0),
    3:  (2.5, 4.5, 1, 1, 0),
    4:  (3.5, 4.5, 1, 2, 0),
    5:  (4.5, 4.5, 1, 3, 0),
    6:  (5.5, 4.5, 1, 4, 0),
    7:  (6.5, 4.5, 1, 4, 0),
    8:  (7.5, 4.5, 1, 5, 0),
    9:  (8.5, 4.5, 1, 5, 0),
    10: (9.5, 4.5, 1, 6, 0),
    11: (10.5, 4.5, 1, 7, 0),
    12: (11.5, 4.5, 1, 8, 0),
    13: (12.5, 4.5, 1, 8, 0),

    14: (1.5, 3.5, 2, 1, 0),
    15: (2.5, 3.5, 2, 2, 0),
    16: (3.5, 3.5, 2, 3, 0),
    17: (4.5, 3.5, 2, 4, 0),
    18: (5.5, 3.5, 2, 4, 0),
    19: (6.5, 3.5, 2, 5, 0),
    20: (7.5, 3.5, 2, 5, 0),
    21: (8.5, 3.5, 2, 6, 0),
    22: (9.5, 3.5, 2, 7, 0),
    23: (10.5, 3.5, 2, 8, 0),
    24: (11.5, 3.5, 2, 8, 0),
    25: (12.5, 3.5, 2, 8, 0),

    26: (1.5, 2.5, 3, 1, 1),
    27: (2.5, 2.5, 3, 2, 1),
    28: (3.5, 2.5, 3, 3, 1),
    29: (4.5, 2.5, 3, 4, 1),
    30: (5.5, 2.5, 3, 4, 0),
    31: (6.5, 2.5, 3, 5, 0),
    32: (7.5, 2.5, 3, 5, 1),
    33: (8.5, 2.5, 3, 6, 1),
    34: (9.5, 2.5, 3, 7, 1),
    35: (10.5, 2.5, 3, 8, 1),
    36: (11.5, 2.5, 3, 8, 0),
    37: (12.5, 2.5, 3, 8, 0),

    38: (1.5, 1.5, 4, 1, 0),
    39: (2.5, 1.5, 4, 2, 0),
    40: (3.5, 1.5, 4, 3, 0),
    41: (4.5, 1.5, 4, 4, 0),
    42: (5.5, 1.5, 4, 4, 0),
    43: (6.5, 1.5, 4, 5, 0),
    44: (7.5, 1.5, 4, 5, 0),
    45: (8.5, 1.5, 4, 6, 0),
    46: (9.5, 1.5, 4, 7, 0),
    47: (10.5, 1.5, 4, 8, 0),
    48: (11.5, 1.5, 4, 8, 0),
}


# Ordered keymap list from ISO layout
QWERTYgenome = [
    '\\', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "'", 'ì', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'è',
    '+', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'ò', 'à', 'ù', '<', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '-'
]

# All letters and symbol in ISO keymap
letterList = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
    'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\\', "'", 'ì', 'è', '+', 'ò', 'à', 'ù', '<', ',', '.', '-'
]

# Ordered keymap list from ANSI layout
QWERTYgenome_ANSI = [
    '~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '+', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    '[', ']', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?'
]

# All letters and symbol in ANSI keymap
letterList_ANSI = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
    'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '~', '-', '+', '[', ']', ';', "'", '<', '>', '?'
]


# Standard and shifted chars for each key in ISO
keyMapDict = {
    'a': [0,0], 'A': [0,1],
    'b': [1,0], 'B': [1,1],
    'c': [2,0], 'C': [2,1],
    'd': [3,0], 'D': [3,1],
    'e': [4,0], 'E': [4,1],
    'f': [5,0], 'F': [5,1],
    'g': [6,0], 'G': [6,1],
    'h': [7,0], 'H': [7,1],
    'i': [8,0], 'I': [8,1],
    'j': [9,0], 'J': [9,1],
    'k': [10,0], 'K': [10,1],
    'l': [11,0], 'L': [11,1],
    'm': [12,0], 'M': [12,1],
    'n': [13,0], 'N': [13,1],
    'o': [14,0], 'O': [14,1],
    'p': [15,0], 'P': [15,1],
    'q': [16,0], 'Q': [16,1],
    'r': [17,0], 'R': [17,1],
    's': [18,0], 'S': [18,1],
    't': [19,0], 'T': [19,1],
    'u': [20,0], 'U': [20,1],
    'v': [21,0], 'V': [21,1],
    'w': [22,0], 'W': [22,1],
    'x': [23,0], 'X': [23,1],
    'y': [24,0], 'Y': [24,1],
    'z': [25,0], 'Z': [25,1],
    '0': [26,0], '=': [26,1],
    '1': [27,0], '!': [27,1],
    '2': [28,0], '"': [28,1],
    '3': [29,0], '£': [29,1],
    '4': [30,0], '$': [30,1],
    '5': [31,0], '%': [31,1],
    '6': [32,0], '&': [32,1],
    '7': [33,0], '/': [33,1],
    '8': [34,0], '(': [34,1],
    '9': [35,0], ')': [35,1],
    '\\': [36,0], '|': [36,1],
    "'": [37,0], '?': [37,1],
    'ì': [38,0], '^': [38,1],
    'è': [39,0], 'é': [39,1],
    '+': [40,0], '*': [40,1],
    'ò': [41,0], 'ç': [41,1],
    'à': [42,0], '°': [42,1],
    'ù': [43,0], '§': [43,1],
    '<': [44,0], '>': [44,1],
    ',': [45,0], ';': [45,1],
    '.': [46,0], ':': [46,1],
    '-': [47,0], '_': [47,1]
}

# Standard and shifted chars for each key in ANSI
keyMapDict_ANSI = {
    'a': [0,0],  'A': [0,1],
    'b': [1,0],  'B': [1,1],
    'c': [2,0],  'C': [2,1],
    'd': [3,0],  'D': [3,1],
    'e': [4,0],  'E': [4,1],
    'f': [5,0],  'F': [5,1],
    'g': [6,0],  'G': [6,1],
    'h': [7,0],  'H': [7,1],
    'i': [8,0],  'I': [8,1],
    'j': [9,0], 'J': [9,1],
    'k': [10,0], 'K': [10,1],
    'l': [11,0], 'L': [11,1],
    'm': [12,0], 'M': [12,1],
    'n': [13,0], 'N': [13,1],
    'o': [14,0], 'O': [14,1],
    'p': [15,0], 'P': [15,1],
    'q': [16,0], 'Q': [16,1],
    'r': [17,0], 'R': [17,1],
    's': [18,0], 'S': [18,1],
    't': [19,0], 'T': [19,1],
    'u': [20,0], 'U': [20,1],
    'v': [21,0], 'V': [21,1],
    'w': [22,0], 'W': [22,1],
    'x': [23,0], 'X': [23,1],
    'y': [24,0], 'Y': [24,1],
    'z': [25,0], 'Z': [25,1],
    '0': [26,0], ')': [26,1],
    '1': [27,0], '!': [27,1],
    '2': [28,0], '@': [28,1],
    '3': [29,0], '#': [29,1],
    '4': [30,0], '$': [30,1],
    '5': [31,0], '%': [31,1],
    '6': [32,0], '^': [32,1],
    '7': [33,0], '&': [33,1],
    '8': [34,0], '*': [34,1],
    '9': [35,0], '(': [35,1],
    '`': [36,0], '~': [36,1],
    '-': [37,0], '_': [37,1],
    '=': [38,0], '+': [38,1],
    '[': [39,0], '{': [39,1],
    ']': [40,0], '}': [40,1],
    ';': [41,0], ':': [41,1],
    "'": [42,0], '"': [42,1],
    ',': [43,0], '<': [43,1],
    '.': [44,0], '>': [44,1],
    '/': [45,0], '?': [45,1]
}

# Left and right hand definition
handList = [1, 1, 1, 1, 2, 2, 2, 2]


################
### COSTANTS ###
################

# Sample .txt file
text_file = 'books.txt'

# True to print stuff in the console, false to quiet mode
debugMode = False

# Setting the seed for genome shuffling
seed = 777
np.random.seed(seed)

# Notation
# Fingers are numbered from left pinky (1) to right pinky (8), excluding thumbs
# Hands are numbered 1->left, 2->right
# Enter and space keys are not counted because they are constant in layouts

# Penalties
distanceEffort = 1      # if set to 2 -> distance penality is squared
doubleFingerEffort = 1  # if I use the same finger consecutively I add an extra effort
doubleHandEffort = 1    # if I use the same hand consectively I add an extra effort

# Some fingers are less efficient than others, higher values for less efficient fingers, values close to zero for the best fingers
# To calculate them, test how many clicks per minute I can do with each finger on the home row
fingerCPM = np.array([239, 236, 292, 321, 328, 303, 297, 228])  # how many clicks can you do in a minute
meanCPM = np.mean(fingerCPM)
stdCPM = np.std(fingerCPM, ddof=1)
zScoreCPM = -(fingerCPM - meanCPM) / stdCPM  # negative since higher is better
fingerEffort = zScoreCPM - np.min(zScoreCPM)

# Keys on the top row are less comfortable than those on the home row
# To calculate them, test how many clicks per minute I can do on each row starting with finger on the home row
rowCPM = np.array([79, 115, 222, 107])
meanCPM = np.mean(rowCPM)
stdCPM = np.std(rowCPM, ddof=1)
zScoreCPM = -(rowCPM - meanCPM) / stdCPM # negative since higher is better
rowEffort = zScoreCPM - np.min(zScoreCPM)

# Define the weight of each penality
# (distancePenalty, doubleFingerPenalty, doubleHandPenalty, fingerPenalty, rowPenalty)
effortWeighting = (0.8, 1, 0.2, 0.5, 0.3)

# Initialize the nested lists and arrays for Pareto's analysis
matrix_rows = len(QWERTYgenome)
matrix_cols = len(QWERTYgenome)
swappedMatrix = [[0 for _ in range(matrix_cols)] for _ in range(matrix_rows)]
paretoSwaps = [[0 for _ in range(matrix_cols)] for _ in range(matrix_rows+1)]

list_length = len(QWERTYgenome)
swappedObjective = [0] * list_length
paretoImprovements = [0] * (list_length+1)


#################
### FUNCTIONS ###
#################

# Assign to the variable keyPress the value at index zero of keyMapDict of the selected char
# If the selected char is not in keyMapDict, skip to the next char
def determineKeypress(currentCharacter):
    debugMode and print('determineKeypress is running...')
    keyPress = None
    if currentCharacter in keyMapDict:
        keyPress, _ = keyMapDict[currentCharacter]
        debugMode and print(currentCharacter, ' is in dict! Chord: ',keyPress,_)
    return keyPress


# Simulate key press by moving fingers to the coordinates of the selected char
# Calculate the distance, any penalties, and update the objective
def doKeypress(myFingerList, myGenome, keyPress, oldFinger, oldHand, currentLayoutMap):
    debugMode and print('doKeyPress is running...')
    namedKey = letterList[keyPress]
    actualKey = myGenome.index(namedKey) + 1
    debugMode and print(namedKey,' -> ',actualKey)

    x, y, row, finger, home = currentLayoutMap[actualKey]
    currentHand = handList[finger - 1]
    if debugMode:
        print('coordinate: ',x,y)
        print('row: ',row)
        print('finger, hand: ',finger,currentHand)
        print('1 for home, 0 not home: ', home)

    # Update fingers positions after key press
    for fingerID in range(1, 9):
        homeX, homeY, currentX, currentY, distanceCounter, objectiveCounter = myFingerList[fingerID - 1]

        if fingerID == finger:
            debugMode and print('the selected finger is: ',fingerID)
            
            # Calculate travel distance from previous finger position
            distance = np.sqrt((x - currentX) ** 2 + (y - currentY) ** 2)
            newDistance = distanceCounter + distance

            # Penalties
            # Distance
            distancePenalty = distance ** distanceEffort # ** means it's raised to the power of distanceEffort

            # Double finger
            doubleFingerPenalty = 0
            if finger == oldFinger and oldFinger != 0 and distance != 0:
                doubleFingerPenalty = doubleFingerEffort
            oldFinger = finger
            
            # Double hand
            doubleHandPenalty = 0
            if currentHand == oldHand and oldHand != 0:
                doubleHandPenalty = doubleHandEffort
            oldHand = currentHand
            
            # Fingers
            fingerPenalty = fingerEffort[fingerID - 1]
            
            # Rows
            rowPenalty = rowEffort[row - 1]
            
            # Combined weighting for penalties
            penalties = (distancePenalty, doubleFingerPenalty, doubleHandPenalty, fingerPenalty, rowPenalty)
            penalty = sum(np.multiply(penalties, effortWeighting))
            debugMode and print('distance, dubFinger, dubHand, finger, row penalty: ', penalties)

            # Calculate new objective
            newObjective = objectiveCounter + penalty
            debugMode and print(fingerID,'finger newdistance and newobjective: ', newDistance, newObjective)

            # Update the coordinates of used finger position
            myFingerList[fingerID - 1] = [homeX, homeY, x, y, newDistance, newObjective]
            debugMode and print('coordinates fingerID',fingerID,': ',myFingerList[fingerID-1])

        else:
            # re-home unused fingers
            myFingerList[fingerID - 1][2] = homeX
            myFingerList[fingerID - 1][3] = homeY
            debugMode and print('coordinates fingerID',fingerID,': ',myFingerList[fingerID-1])

    return myFingerList, oldFinger, oldHand


# Check if the random generated genome is better than the previous best
def objectiveFunction(file, myGenome, currentLayoutMap, QWERTYscore):
    debugMode and print('ObjectiveFunction is running...')

    # Define myFingerList as a matrix with a number of rows equal to the number of fingers (8) 
    # and a number of columns (6) as [homeX, homeY, x of FingerPress, y of FingerPress, newDistance, newObjective]
    myFingerList = np.zeros((8, 6))
    objective = 0
    oldFinger = 0
    oldHand = 0

    for i in range(1, len(myGenome)+1):
        x, y, _, finger, home = currentLayoutMap[i]

        # Place finger on their home key
        if home == 1:
            myFingerList[finger - 1][0:4] = [x, y, x, y]

    # Execute determineKeypress for the selected char
    for currentCharacter in file:
        keyPress = determineKeypress(currentCharacter)

        if keyPress is not None:
            myFingerList, oldFinger, oldHand = doKeypress(myFingerList, myGenome, keyPress, oldFinger, oldHand, currentLayoutMap)

    # Sum the sixth column of myFingerList matrix to get the total objective of all fingers
    #distance = np.sum(myFingerList[:, 4])      # distance is included in the penalties
    objective = np.sum(myFingerList[:, 5])

    # Normalize objective to the QWERTY one
    objective = (objective / QWERTYscore - 1) * 100

    return objective


# Same as objectiveFunction but with specified reference genome and without QWERTYscore normalization
def baselineObjectiveFunction(file, myGenome, currentLayoutMap):
    debugMode and print('baselineObjectiveFunction is running')
    myFingerList = np.zeros((8, 6))
    objective = 0
    oldFinger = 0
    oldHand = 0
    
    for i in range(1, len(myGenome)+1):
        x, y, _, finger, home = currentLayoutMap[i]

        if home == 1:
            myFingerList[finger - 1][0:4] = [x, y, x, y]

    for currentCharacter in file:
        debugMode and print(currentCharacter, '<- is the clicked char')
        keyPress = determineKeypress(currentCharacter)

        # Here is the difference where I specify to use reference genome on invoke
        if keyPress is not None:
            myFingerList, oldFinger, oldHand = doKeypress(myFingerList, myGenome, keyPress, oldFinger, oldHand, currentLayoutMap)

    #distance = np.sum(myFingerList[:, 4])      # distance is included in the penalties
    objective = np.sum(myFingerList[:, 5])

    debugMode and print('objective: ',objective)

    return objective


# Random genome generator
def createGenome():
    myGenome = np.random.permutation(letterList)
    myGenome = myGenome.tolist()

    debugMode and print(myGenome)

    return myGenome


# Random genome mixer
def shuffleGenome(currentGenome, temperature):
    # Determine how many switch there will be
    # When T is high there will be more (cap at len(letterlist)), in the end only 2 at the same time
    no_switches = int(max(2, min(temperature // 100, len(currentGenome))))

    # Positions of switched chars
    switched_positions = random.sample(range(0, len(currentGenome)), no_switches)
    debugMode and print(switched_positions)
    new_positions = random.sample(switched_positions, no_switches)
    debugMode and print(new_positions)

    # Create new genome by shuffling
    newGenome = currentGenome.copy()
    for og, ne in zip(switched_positions, new_positions):
        newGenome[og - 1] = currentGenome[ne - 1]
    
    debugMode and print(newGenome)

    return newGenome


# Write updates in file
def appendUpdates(updateLine):
    with open('outputs/score/iterationScores.txt', 'a') as file:
        file.write(updateLine + '\n')


# Plot the keyboard layout for easy comparison
# The most and the least used letters are highlighted in different colors
# To get your language (or you notes) ones check the README on github
def drawKeyboard(myGenome, id, currentLayoutMap):
    plt.figure()

    for i in range(1, len(myGenome)+1):
        letter = myGenome[i - 1]
        x, y, row, finger, home = currentLayoutMap[i]

        myColour = 'darkgray'
        if letter in ['A', 'E']:
            myColour = 'lime'       # most used letters are this color
        elif letter in ['I', 'O', 'N', 'R', 'T', 'L', 'S', 'C']:
            myColour = 'yellow'     # next most used letters are this color
        elif letter in ['\\', '+', '7', '5', '3', '4', '6', '8', 'X', '9']:
            myColour = 'maroon'     # least used letters are this color

        # Draw a little square in the homerow keys
        if home == 1:
            plt.plot(x, y, marker='s', markersize=16.5, color=myColour, alpha=0.2)
        
        # Draw keys
        plt.fill([x - 0.45, x + 0.45, x + 0.45, x - 0.45, x - 0.45],
                 [y - 0.45, y - 0.45, y + 0.45, y + 0.45, y - 0.45],
                 color=myColour, alpha=0.2)

        # Draw letters
        plt.text(x, y, letter, color='black', ha='center', va='center', fontsize=10)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    # Save png in the selected subfolder naming equals the iteration cicle
    # Remember to delete them before running multiple times the script or you will find mixed iteration solution
    plt.savefig(f'outputs/score/plot-layouts/{id}.png')

    #debugMode and plt.show()
    plt.close()


# Simulated annealing approach
def runSA(layoutMap, baselineLayout, temperature, epoch, coolingRate, num_iterations, plot_current_best, verbose):
    
    currentLayoutMap = layoutMap

    # Create lists to store iteration data just for the graph
    newObjective_values = []
    bestObjective_values = []

    # Header is used to clear the file, otherwise it continues to append at the end, merging consecutive runs
    with open(f'outputs/score/iterationScores.txt', 'w', encoding='utf-8') as saveState:
        saveState.write(f'Temp \t Iteration \t BestScore \t NewScore \n')

    with open(f'outputs/score/bestGenomes.txt', 'w', encoding='utf-8') as io:
        io.write(f'Iteration: Best genomes \n')

    # Open sample file
    with open(text_file, 'r', encoding='utf-8') as text:
        file = text.read().lower()

        if verbose:
            print('Running simulated annealing code...')
            print('Calculating raw baseline... ', end='')

        # Taking timestamp to show in the console info about how much it will take
        start_time = time.time()    # timestap
        # Calculate QWERTYscore using baselineLayout as reference
        QWERTYscore = baselineObjectiveFunction(file, baselineLayout, currentLayoutMap)
        end_time =time.time()   # timestamp
        print('QWERTYscore: ', QWERTYscore)
        execTimeObjectiveFunction = end_time - start_time
        estimatedTime = str(datetime.timedelta(seconds=execTimeObjectiveFunction*num_iterations))
        
        if verbose:
            print('From here everything is relative with +% worse and -% better than this baseline')
            print('Note that the best layout is being saved as a png at each step. Kill program when satisfied.')
            print('This may take several minutes depending on the arguments.')
            print('1 x ObjectiveFunction execution time: ', round(execTimeObjectiveFunction,3),' s')
            print('Worst case scenario is: ', estimatedTime)
            print('Temp \t BestScore \t NewScore \t IterTime')

        # Inizialize the variables with the first randomically generated genome
        # This one doesn't have timestamp
        currentGenome = createGenome()
        currentObjective = objectiveFunction(file, currentGenome, currentLayoutMap, QWERTYscore)
        bestGenome = currentGenome
        bestObjective = currentObjective

        drawKeyboard(bestGenome, 0, currentLayoutMap)

        # Inizialize counters
        staticCount = 0
        iteration = 0
        while iteration <= num_iterations and temperature > 1.0:
            iteration += 1
            newGenome = shuffleGenome(currentGenome, 2)
            start_time = time.time()    # timestamp
            newObjective = objectiveFunction(file, newGenome, currentLayoutMap, QWERTYscore)
            end_time =time.time()   # timestamp
            execTimeObjectiveFunction = end_time - start_time
            delta = newObjective - currentObjective

            # Append newObjective and bestObjective to lists
            newObjective_values.append(newObjective)
            bestObjective_values.append(bestObjective)

            verbose and print(f'{temperature:.2f} \t {bestObjective:.5f} \t {newObjective:.5f} \t {execTimeObjectiveFunction:.3f}')

            # If delta < 0 this genome is better than the previous one
            if delta < 0:
                currentGenome = newGenome
                currentObjective = newObjective

                updateLine = f'{round(temperature, 1)}, \t {iteration}, \t\t {round(bestObjective, 5)}, \t {round(newObjective, 5)}'
                appendUpdates(updateLine)

                # < to get the best keyboard layout
                # > to get the worst one
                # If newObjective < bestObjective this genome is the best one so far
                if newObjective < bestObjective:
                    bestGenome = newGenome
                    bestObjective = newObjective

                    if plot_current_best:
                        verbose and print('(new best, png being saved)')
                        drawKeyboard(bestGenome, iteration, currentLayoutMap)

                    if verbose:
                        print('(new best, text being saved)')
                        with open('outputs/score/bestGenomes.txt', 'a') as io:
                            io.write(f"{iteration}: {''.join(bestGenome)}\n")
            
            # Sometimes randomically, even if this genome is not better than the previous one, it survives and substitute the prev
            # This is simulated annealing
            elif np.exp(-delta / temperature) > np.random.random():
                currentGenome = newGenome
                currentObjective = newObjective

            staticCount += 1
            # When staticCount is greater than epoch it resets and temperature get lower
            if staticCount > epoch:
                staticCount = 0
                temperature = temperature * coolingRate

                # When T gets cooler if this random if is true the current genome became the best one
                if np.random.random() < 0.5:
                    currentGenome = bestGenome
                    currentObjective = bestObjective
            
        # Redraw the last layout even if plot is False and name it final
        drawKeyboard(bestGenome, 'final', currentLayoutMap)

        # Print QWERTYscore in log file
        appendUpdates(f'QWERTYscore: {QWERTYscore}')

        # Plotting newObjective and bestObjective values
        plt.figure(1)  # Create a new figure
        plt.plot(newObjective_values, color='green', label='New Objective', linewidth=0.5)
        plt.plot(bestObjective_values, color='blue', label='Best Objective')
        plt.axhline(y=0, color='red', linestyle='--', label='QWERTY Score')     # QWERTYscore is the reference

        plt.xlabel('Iteration')
        plt.gca().invert_yaxis()
        plt.ylabel('Objective Score [%]')
        plt.title('Objective Scores vs Iteration')
        plt.legend()
        plt.savefig(f'outputs/score/plot-layouts/objective.png', dpi=300)
        plt.show()

        plt.close()

        return bestGenome, QWERTYscore


# This function will test with objectiveFunction each swap of pairs of keys
# starting from QWERTYgenome (original) towards the bestGenome (ideal) found with simulated annealing
def paretoEfficiency(original, ideal, verbose):
    newOriginal = original.copy()
    debugMode and print('newOriginal: ',newOriginal)

    if verbose:
        print('Running Pareto analysis code...')
        # Header is used to clear the file, otherwise it continues to append at the end, merging consecutive runs
        with open(f'outputs/score/paretoSwaps.txt', 'w', encoding='utf-8') as io:
            io.write(f'n°\t keys \t score \t genome \n')
    
    # t is the counter for saving the best swap of each set
    for t in range(len(original)):
        # I need this variable to compile the txt log. More on this later
        beforeSwap = newOriginal

        # i is the counter to swap every char of the bestGenome in the same position but inside the QWERTYgenome
        # it test one swap at time
        for i in range(len(original)):
            # swapped is the genome with 2 letters swapped
            swapped = newOriginal.copy()
            indexKeySwap = newOriginal.index(ideal[i])
            swapped[i] = ideal[i]
            swapped[indexKeySwap] = newOriginal[i]
            debugMode and print('swapped: ',swapped)
            # swappedMatrix contains all the genome of the current set
            # These genomes are competing for the title of best performance and to assert themselves
            swappedMatrix[i] = swapped

            # Test the current genome and save his score in swappedObjective
            with open(text_file, 'r', encoding='utf-8') as text:
                file = text.read().lower()
                currentLayoutMap = traditionalLayoutMap
                swappedObjective[i] = objectiveFunction(file, swapped, currentLayoutMap, QWERTYscore)
                debugMode and print('swapped objectives: ',swappedObjective)
        
        # Search for the best genome (= the one with the lower objective because it measures the % of less effort)
        bestObjective = min(swappedObjective)
        verbose and print('Found best swap n° ', t+1)

        # Assign the best genome to the newOriginal variable
        # The next cycle starts from this one to search for the second best swaps and so on
        indexBestObjective = swappedObjective.index(bestObjective)
        newOriginal = swappedMatrix[indexBestObjective]

        # I start pooling these lists from index 1 since I want the first one to be 0 as it represents 0 swaps (the QWERTY keyboard)
        paretoSwaps[t+1] = newOriginal
        paretoImprovements[t+1] = bestObjective
        debugMode and print(paretoSwaps)
        debugMode and print(paretoImprovements)
        debugMode and input('press enter to continue...')

        # I save a log file with all the usefull infos
        if verbose:
            with open('outputs/score/paretoSwaps.txt', 'a') as io:
                # difference is a list where i highlight the current swapped pair           
                afterSwap = newOriginal
                difference = [beforeSwap[i] for i in range(len(beforeSwap)) if beforeSwap[i] != afterSwap[i]]
                io.write(f"{t+1} \t {'-'.join(difference)} \t {round(bestObjective,1)} \t {''.join(newOriginal)}\n")
        
        # Draw the best layout
        namePlot = str(f'pareto_{t+1}')
        drawKeyboard(newOriginal, namePlot, currentLayoutMap)
        
        # Break the loop if there is more than one occurrence of the minimum value
        # Usually this happen only at the end where there are almost useless swaps
        occurrences = swappedObjective.count(bestObjective)
        if occurrences > 1:
            print('More than one objective results the same. Arresting...')
            break
    
    # Plotting the Pareto frontier
    # Find the index of the first zero value (starting from index 1 because the first one is QWERTY)
    # I use this beacuse if you test this on a small txt file with only few letters you will get a better views of the scores
    first_zero_index = next((i for i, x in enumerate(paretoImprovements[1:], start=1) if x == 0), len(paretoImprovements))

    plt.figure(2)  # Create a new figure
    plt.plot(paretoImprovements[:first_zero_index], 'mo-')
    plt.xlabel('Number of swaps')
    plt.xticks(range(first_zero_index))     # Show only integers on x axis
    plt.gca().invert_yaxis()
    plt.ylabel('Objective Score [%]')
    plt.title('Pareto frontier')
    plt.savefig(f'outputs/score/plot-layouts/pareto.png', dpi=300)
    plt.show()
    
    plt.close()

    return paretoSwaps, paretoImprovements


###########
### RUN ###
###########
    
### FIND THE BEST LAYOUT ###

bestGenome, QWERTYscore = runSA(layoutMap=traditionalLayoutMap,     # define layout used
                                baselineLayout=QWERTYgenome,        # define baseline genome to make the comparison
                                temperature=500,                    # starting T, at T=1 the cycle stops
                                epoch=20,                           # number of times that the algorithm will work through the same dataset
                                coolingRate=0.99,                   # decrease of temperature (0.99)
                                num_iterations=20000,               # max number of iteration (25000)
                                plot_current_best=True,             # set False to not plot layouts
                                verbose=True)                       # set False to silence terminal outputs)
print('bestGenome: ',bestGenome)
print('QWERTYscore: ',QWERTYscore)

### PARETO EFFICIENCY ANALYSIS ###

# Ask the user if they want to continue
answer = input('Do you want to continue and run Pareto analysis with the obtained results? (yes/no): ').lower()
if answer == 'yes' or answer == 'y':
    print('Continuing...')
else:
    print('Arresting...')
    exit()  # Exit the program

# Let this variables comment if you run in a single time after the runSA function
# Or paste from the output of runSA, comment the 'find the best layout' section and uncomment these variables
#bestGenome = ['5', '2', 'F', '7', 'ù', 'ì', 'B', '3', '\\', 'Z', 'ò', '6', '0', "'", 'V', '+', 'W', 'J', 'Q', 'T', '.', '8', 'è', 'X', '9', 'E', 'K', 'O', 'A', 'C', 'L', 'N', 'M', 'I', 'S', '<', 'Y', '-', 'R', ',', 'H', 'G', '4', 'D', 'P', 'U', 'à', '1']
#QWERTYscore = 6847.612377658692

paretoSwaps, paretoImprovements = paretoEfficiency(QWERTYgenome, bestGenome, verbose=True)
#print(paretoSwaps)
print('paretoImprovements: ',paretoImprovements)



