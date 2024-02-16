import matplotlib.pyplot as plt
from collections import defaultdict


#############
### SETUP ###
#############

# Sample .txt file
text_file = 'books.txt'


#################
### FUNCTIONS ###
#################

# Count accented characters and symbols too
# It could be worthy to sum ’ and ' (right single quotation mark and apostrophe)
def countCharNgram(file_path, n):
    # Open the file for reading
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()

    # Create a defaultdict to count n-grams
    ngramCount = defaultdict(int)

    # Count n-grams
    for i in range(len(text) - n + 1):
        ngram = ''.join(text[i:i+n])  # Concatenate characters to form the key
        ngramCount[ngram] += 1

    # Exclude keys containing spaces or newlines
    ngramCount = {k: v for k, v in ngramCount.items() if ' ' not in k and '\n' not in k}

    return ngramCount

def plotNgramDistribution(ngramDict, n, top_n):
    # Sort the dictionary in decreasing order
    ngramSorted = dict(sorted(ngramDict.items(), key=lambda item: item[1], reverse=True))

    # Horizontal histogram only for the top entries
    ngramSortedHead = list(ngramSorted.items())[:top_n]

    # Extract labels and values from the list of tuples
    labels, values = zip(*ngramSortedHead)

    # Create a horizontal histogram
    plt.barh(labels, values, height=0.8, left=None, align='center', linewidth=0, color="y")
    plt.gca().invert_yaxis()
    plt.ylabel(f"{n}-gram")
    plt.yticks(fontsize=6)
    plt.xlabel("Frequency")
    plt.title(f"Distribution of {n}-gram")
    plt.savefig(f"outputs/plot_{n}gram.png", dpi=300)
    plt.show()

def writeNgramCountToFile(ngramCount, n):
    # Sort dictionary in decreasing order
    ngramSorted = dict(sorted(ngramCount.items(), key=lambda item: item[1], reverse=True))

    # Write to file
    with open(f"outputs/count_{n}gram.txt", 'w', encoding='utf-8') as output_file:
        output_file.write(f"{n}-gram count:\n")
        for key, value in ngramSorted.items():
            output_file.write(f"{key}: {value}\n")


###########
### RUN ###
###########

# Usage example for counting single letters (n = 1)
output_letters = countCharNgram(text_file, 1)
plotNgramDistribution(output_letters, 1, 43)
writeNgramCountToFile(output_letters, 1)

# Usage example for counting bigrams (n = 2)
output_bigrams = countCharNgram(text_file, 2)
plotNgramDistribution(output_bigrams, 2, 50)
writeNgramCountToFile(output_bigrams, 2)

# Usage example for counting trigrams (n = 3)
output_trigrams = countCharNgram(text_file, 3)
plotNgramDistribution(output_trigrams, 3, 50)
writeNgramCountToFile(output_trigrams, 3)