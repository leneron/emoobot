# simple input data filter
# first stage of the data processing
import re


class Filter:
    # constants are defined beforehand
    # these constants are based on common features of the posts on vk.com
    # they can be redefined if it is necessary
    MIN_LENGTH = 40
    MAX_LENGTH = 400
    # regular expression is compiled in the byte code
    # which is executed by the special engine written on C
    SPAM_RE = re.compile('руб|грн|цен[аы]?|акц|скид|зниж|курс|'
                         'брон(ь|(ир(овать|уйте|уем)))|запис(ь|ывайтесь)|'
                         ' лс |личк[ауи]?|'
                         'п[оі]дпис|лайк|репост|'
                         'голос(у([єе]м||йте))?|'
                         'vk\.c(c|om)|askfm',
                         re.I)

    # the filter passes the text in case of the acceptable text length
    @staticmethod
    def lengthFilter(text):
        return Filter.MIN_LENGTH <= len(text) <= Filter.MAX_LENGTH

    # the filter passes the text if it doesn't include any spam-words from the list
    @staticmethod
    def spamFilter(text):
        # if the result of the search is not None
        return Filter.SPAM_RE.search(text) is None