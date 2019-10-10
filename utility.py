class ngramDict:
    def __init__(self):
        self.dictionary = {}
        self.name = ""
        self.count = 0
        self.vocabularyC = 0
        # vocabulary count for laplace smoothing
        self.subDict = []
        # N-gram dictionaries with smaller n. Used for linear interpolation smoothing
        # subDict[0] is unigram, subDict[1] is bigram, etc.
        self.coefficient = []
        # coefficient for linear interpolation smoothing
        # self.coefficient[0] refers to unigram, self.coefficient[4] refers to 5-gram
        self.tokenSum = 0
        # total number of characters in the training text, space is excluded
        # SO, linear interpolation's coefficient depends on the frequency of different ngram

    def countVoca(self):
        count = 0
        for i in self.dictionary:
            count = count + 1
        self.vocabularyC = count

    def counttoken(self):
        self.tokenSum = sum(self.subDict[0].values())
        # subDict[0] is unigram

    def setCoefficient(self, n):
        # n is the n in N-gram
        # initialize coefficient array
        for i in range(n):
            self.coefficient.append(0)
        print(len(self.coefficient))

        self.counttoken()

        # get coefficient (no normalization)
        for i in self.dictionary:
            # first iteration
            currentTuple = i
            nextTuple = currentTuple[1:n]
            dominator = currentTuple[0:n-1]
            hashRes = inHashTable(self.subDict[n-2], dominator)
            if hashRes[1] > 1:
                freq = (self.dictionary[currentTuple]-1)/(hashRes[1]-1)
            else:
                freq = 0
            print(i)
            print(freq)
            highFrep = freq
            highNgram = n

            # middle iterations
            for j in range(n - 1, 1, -1):
                currentTuple = nextTuple
                nextTuple = currentTuple[1:j]
                dominator = currentTuple[0:j - 1]
                hashRes = inHashTable(self.subDict[j - 2], dominator)
                if hashRes[1] > 1:
                    freq = (self.subDict[j - 1][currentTuple] - 1) / (hashRes[1] - 1)
                else:
                    freq = 0
                print(freq)
                if freq > highFrep:
                    highFrep = freq
                    highNgram = j

            # last iteration
            # currentTuple = nextTuple
            hashRes = inHashTable(self.subDict[j - 2], nextTuple)
            if hashRes[0] and hashRes[1] > 1:
                freq = (hashRes[1] - 1) / (self.tokenSum - 1)
            else:
                freq = 0
            print(freq)
            if freq > highFrep:
                highNgram = 1
            # do adding after find the highest freq for current ngram
            # if highFrep == 0:
            #    continue
            self.coefficient[highNgram - 1] = self.coefficient[highNgram - 1] + self.dictionary[i]

        # normalization
        coeSum = sum(self.coefficient)
        coeLen = len(self.coefficient)
        for i in range(coeLen):
            self.coefficient[i] = self.coefficient[i]/coeSum


def inHashTable(hashtable, key):
    try:
        a = hashtable[key]
    except KeyError:
        return False, 0
    else:
        return True, a