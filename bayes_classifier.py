# bayes classifier is one of the simplest and most effective ways
# to define the class of the document
import os
import json
import math
import collections

class BayesClassifier:
    # dictionaries consist of key : dictionary
    # each inner dictionary has values such as word : amount of these words + 1
    # + 1 helps to avoid zero probability if there is no such word in dictionary
    dictionaries = {}
    # number of documents for each class
    messageDistribution = collections.Counter()
    def __init__(self, path, splitSymbol):
        fileNames = os.listdir(path)
        for fileName in fileNames:
            # fileName has a structure like this: <key><SPLIT_SYMBOL><number>
            # e.g. ☺_3
            name = os.path.basename(fileName)
            # extract key
            key = name.split(splitSymbol)[0]

            with open(path+fileName, 'r') as file:
                BayesClassifier.addData(self, key, file)

    # add data to some class
    def addData(self, key, file):
        # file consists of list of object
        # each object is a parsed message, it's a list, too
        dictionary = self.dictionaries.setdefault(key, collections.Counter())
        messages = json.load(file)

        for message in messages:
            self.messageDistribution[key] += 1

            for word in message:
                dictionary[word] += 1

        self.dictionaries.update([[key, dictionary]])

    # MAIN FUNCTION FOR DEFINING THE CLASS OF MESSAGE

    # MULTINOMIAL BAYES MODEL
    # suppose that:
    # P(w[i]|c) = wc[i] / wtotal
    # where wc[i] is amount of word w repetitions in class c
    # wtotal is total amount of words
    # in all documents of this class


    def getClass(self, message):
        # c -- class we want to define text
        # d -- document
        # P(c|d) = P(d|c) * P(c) / P(d)
        # c = arg max P(c|d) = arg max (P(d|c) * P(c) / P(d))
        # P(d) is a probability to encounter document in all documents
        # it means that we can ease formula in a way:
        # c = arg max (P(d|c) * P(c))
        # where P(d|c) is a probability that document d is in class c
        # and P(c) is a probability of this class

        # UNIGRAM LANGUAGE MODEL
        # P(d|c) = multiplication(P(w[i]|c)) for i=1 to n
        # where P(w[i]|c) is a probability to that word w with index i belongs to c

        # however, we can get arithmetic underflow
        # because we multiply many small numbers
        # to avoid this, we will use logarithm:
        # c = arg max (log(P(c)) + sum(log(P(w[i]|c)))) for i = 1 to n

        c = max(self.dictionaries.keys(), key = lambda x: (math.log(self.getProbabilityClass(x))
                                + sum([math.log(self.getProbabilityMessageGivenClass(x, word)) for word in message])))
        return c

    def getProbabilityClass(self, key):
        # P(c) = Dc \ D,
        # where Dc is amount of documents, that belongs to c
        # and D is total amount of documents
        totalMessages = sum(map(int, self.messageDistribution.values()))
        return self.messageDistribution.setdefault(key, 0) / totalMessages

    def getProbabilityMessageGivenClass(self, key, word):
        # to avoid zero probability in case of absense word in any dictionaries,
        # use ADDITIVE SMOOTHING:
        # P(w[i]|c) = (wc[i] + 1) / (wtotal + v)
        # v is a number of unique words in class c

        totalWords = sum(self.messageDistribution.values())
        v = len(self.dictionaries[key].values())

        if word in self.dictionaries[key]:
            wordInClass = 0
        else:
            wordInClass = self.dictionaries[key][word]

        return (wordInClass + 1) / (totalWords + v)


# example the class usage
b = BayesClassifier('data_examples/', '_')
print(b.getClass(['завтра', 'читаю', 'книга']))