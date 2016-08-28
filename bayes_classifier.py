# bayes classifier is one of the simplest and most effective ways
# to define the class of the document
import os
import json
import pprint


class BayesClassifier:
    # dictionaries consist of key : dictionary
    # each inner dictionary has values such as word : amount of these words + 1
    # + 1 helps to avoid zero probability if there is no such word in dictionary
    dictionaries = {}
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
        dictionary = self.dictionaries.setdefault(key, {})
        messages = json.load(file)
        for message in messages:
            for word in message:
                count = dictionary.setdefault(word, 1)
                count += 1
                dictionary.update([[word, count]])


# example the class usage
b = BayesClassifier('data_examples/', '_')