import os
import train_ngram as tn
import test_ngram as testn

if __name__ == '__main__':

    n = 5
    smoothing = 1
    # no smoothing

    trainPath = "811_a1_train"
    fileList = os.listdir(trainPath)
    dictArray = []
    for i in fileList:
        #print(i)
        language_example = open(trainPath+"/"+i, encoding="utf-8")
        iNgram = tn.tranFile(language_example, n)
        iNgram.name = i
        dictArray.append(iNgram)
        #print(iNgram.dictionary)
        break


    devPath = "811_a1_dev"
    fileList = os.listdir(devPath)
    for i in fileList:
        devSet = open(devPath+"/"+i, encoding="utf-8")
        (probability, name) = testn.get_probability(devSet, dictArray, smoothing, n)
        print(i)
        print(probability)
        print(name)
        break




