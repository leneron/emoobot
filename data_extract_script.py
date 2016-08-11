# data extractor module for the training dataset
import vk
import datetime
from time import sleep
from data_filter import Filter
from data_editor import Editor
import json
import os


class Extracter:
    # standart constant for max amount of returned posts
    MAX_COUNT = 200
    # it is allowed to make 3 requests/second to avoid being banned
    REQUESTS_PER_SECOND = 3

    DEFAULT_PATH = 'data_examples/'
    SPLIT_SYMBOL = '_'

    def __init__(self):
        session = vk.Session()
        self.api = vk.API(session, v = '5.53')

    def saveToFile(self, data, key, path = DEFAULT_PATH):
        index = self.findStartFileNumber(key, path)
        fileName = path + key + self.SPLIT_SYMBOL + str(index)
        # dataset will be saved as json array
        with open(fileName, 'w') as file:
            json.dump(data, fp = file, ensure_ascii = False)

    def findStartFileNumber(self, key, path = DEFAULT_PATH):
        fileNames = os.listdir(path)
        index = -1
        for fileName in fileNames:
            # fileName has a structure like this: <key><SPLIT_SYMBOL><number>
            # e.g. ☺_3
            name = os.path.basename(fileName)
            if (name.find(key)) != -1:
                tempIndex = int(name.split(self.SPLIT_SYMBOL)[-1])
                if tempIndex > index:
                    index = tempIndex

        return index + 1

    # extracts data by the key passed as the paramether
    # fileSize is a number that shows how many posts will be saved into one file at least
    def extractNewsfeed(self, key, datasetSize = 20000, fileSize = 2000):
        # we need to set the delay between the requests
        # variable requestCounter shows how many requests were already made during this current second
        # variable requestStartTime helps to define the duration of the delay
        # first request is done
        requestCounter = 1
        requestStartTime = datetime.datetime.now()

        timestamp = None

        # number of files (blocks of data), that will be saved to the disk
        filesAmount = max(1, int(datasetSize / fileSize))
        # i is used for naming the files
        for i in range(filesAmount):
            # dataset is a list of strings, that were found int the search
            # each of the strings contains a key, passed as the parameter of the function
            dataset = []

            # we don't save all the data in memory
            # we save the data to the disk simultaneously with the extracting the data
            while len(dataset) < fileSize:
                # get new values
                response = self.api.newsfeed.search(q = key,
                                                    count = self.MAX_COUNT,
                                                    end_time = timestamp)

                # search until the last viewed post is reached
                # "- 1" is prevention of reduplication posts
                timestamp = response['items'][-1]['date'] - 1

                # put all results in the dataset
                for item in response['items']:
                    # input data filter
                    # length filter is used to avoid too short or too long posts
                    # simple spam-filter  the most used keywords
                    text = item['text']
                    if Filter.lengthFilter(text)\
                            and Filter.spamFilter(text):
                        text = Editor.clean(text)
                        if text:
                            dataset.append(text)

                # there's a delay after the last request
                # if it is necessary
                requestCounter += 1
                requestCounter %= self.REQUESTS_PER_SECOND
                if requestCounter == 0:
                    requestEndTime = datetime.datetime.now()
                    delay = datetime.timedelta(seconds = 1) - (requestEndTime - requestStartTime)
                    if delay >= datetime.timedelta.resolution:
                        sleep(datetime.timedelta(milliseconds = 1).total_seconds())
                    requestStartTime = requestEndTime

            # save result
            self.saveToFile(data = dataset, key = key)


# code example
vkApi = Extracter()
# this is an example method call, that extracts 1200 posts with the keyword '☺️'
vkApi.extractNewsfeed('☺️', 200, 200)