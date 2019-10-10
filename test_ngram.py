import nltk
import utility as ut


def get_probability(text, dicts, smoothing=0, n=2):
# dicts is a 2 dimension array, the second dimension have 0 and 1, and maybe 2.
# 0 for a dictionary, 1 for the total count of the dict, 2 for the name of dict
# for smoothing, 0 means no smoothing, 1 means laplace
    content = text.read()
    contentWords = content.split()
    lowPerplexity = float('inf')
    dictName = "default"

    testNgram = []
    for j in contentWords:
        cNgram = nltk.ngrams(j, n, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>')
        for i in cNgram:
            testNgram.append(i)
    lenTestNgram = len(testNgram)
    # get all ngram of test here and count number, when calculating the perplexity, directly do square

    for i in dicts:
        #print(i)
        totalPerplexity = 1

        for j in testNgram:
            hashRes = ut.inHashTable(i.dictionary, j)
            if smoothing == 0:
                # no smoothing
                if hashRes[0]:
                    ngramPerplexity = i.count / hashRes[1]
                    # hashRes[1] is the ngram count of the current ngram in the dict
                    # i.count is the total number of ngram in the dict
                else:
                    ngramPerplexity = float('inf')
            elif smoothing == 1:
                # laplace smoothing
                if hashRes[0]:
                    ngramPerplexity = (i.count + i.vocabularyC) / (hashRes[1] + 1)
                    # i.vocabularyC is the total number of ngram in the dict
                else:
                    ngramPerplexity = (i.count + i.vocabularyC) / 1
            elif smoothing == 2:
                ngramProbability = 0
                currentTuple = j
                nextTuple = currentTuple[1:n]
                hashResC = hashRes
                hashResN = ut.inHashTable(i.subDict[n - 2], nextTuple)
                if hashResC[1] > 1 and hashResN[1] > 1:
                    freq = (hashResC[1] - 1) / (hashResN[1] - 1)
                else:
                    freq = 0
                ngramProbability = ngramProbability + freq * i.coefficient[n-1]
                for k in range(n-1, 1, -1):
                    currentTuple = nextTuple
                    nextTuple = currentTuple[1:k]
                    hashResC = hashResN
                    hashResN = ut.inHashTable(i.subDict[k - 2], nextTuple)
                    if hashResC[1] > 1 and hashResN[1] > 1:
                        freq = (hashResC[1] - 1) / (hashResN[1] - 1)
                    else:
                        freq = 0
                    ngramProbability = ngramProbability + freq * i.coefficient[k-1]
                if hashResN[1] > 1:
                    freq = (hashResN[1] - 1) / (i.tokenSum - 1)
                else:
                    freq = 0
                ngramProbability = ngramProbability + freq * i.coefficient[n-1]
                ngramPerplexity = 1/ngramProbability
                # what should I do in the end of the word???
            else:
                print("wrong smoothing method indicator!!")
                return

            #print(ngramPerplexity ** (1/lenTestNgram))
            totalPerplexity = (ngramPerplexity ** (1/lenTestNgram)) * totalPerplexity

        if totalPerplexity < lowPerplexity:
            lowPerplexity = totalPerplexity
            dictName = i.name

    return lowPerplexity, dictName
