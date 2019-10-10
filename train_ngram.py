import nltk
import utility as ut

def tranFile(file, n):
    content = file.read()
    contentWords = content.split()
    newNgram = ut.ngramDict()

    # generate N-gram dictionary
    for j in contentWords:
        cNgram = nltk.ngrams(j, n, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>')
        for i in cNgram:
            hashRes = ut.inHashTable(newNgram.dictionary, i)
            if hashRes[0]:
                newNgram.dictionary[i] = hashRes[1] + 1
            else:
                newNgram.dictionary[i] = 1
            newNgram.count = newNgram.count + 1
    newNgram.countVoca()
    print(newNgram.dictionary)

    # generate N-gram dictionaries for smaller n, that will be used in linear interpolation smoothing
    for k in range(1, n):
        newDict = {}
        for j in contentWords:
            cNgram = nltk.ngrams(j, k, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>')
            for i in cNgram:
                hashRes = ut.inHashTable(newDict, i)
                if hashRes[0]:
                    newDict[i] = hashRes[1] + 1
                else:
                    newDict[i] = 1
        newNgram.subDict.append(newDict)
    newNgram.setCoefficient(n)
    print(newNgram.coefficient)

    return newNgram