# data extractor module for the training dataset
import vk
import datetime
from time import sleep

class Extracter:
    # standart constant for max amount of returned posts
    MAX_COUNT = 200
    # it is allowed to make 3 requests/second to avoid being banned
    REQUESTS_PER_SECOND = 3

    def __init__(self):
        session = vk.Session()
        self.api = vk.API(session, v='5.53')

    # extracts data by the key passed as the paramether
    def extractNewsfeed(self, key, datasetSize):
        # dataset is a list of strings, that were found int the search
        # each of the strings contains a key, passed as the parameter of the function
        dataset = []
        countSize = datasetSize if datasetSize < self.MAX_COUNT else self.MAX_COUNT

        # we need to set the delay between the requests
        # variable requestCounter shows how many requests were already made during this current second
        # variable requestStartTime helps to define the duration of the delay
        # first request is done
        requestCounter = 1
        requestStartTime = datetime.datetime.now()

        timestamp = None

        while len(dataset) < datasetSize:
            # get new values
            response = self.api.newsfeed.search(q = key, count = countSize, end_time = timestamp)

            # search until the last viewed post is reached
            # "- 1" is prevention of reduplication posts
            timestamp = response['items'][-1]['date'] - 1

            # put all results in the dataset
            for item in response['items']:
                # TODO data filter
                # TODO distribution and saving the data to the disk
                dataset.append(item['text'])

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


# code example
vkApi = Extracter()
# this is an example method call, that extracts 1200 posts with the keyword '☺️'
vkApi.extractNewsfeed('☺️', 1200)